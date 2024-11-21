"""
Tasks for updating details on active members.

Active members are of higher interest than historical ones so we maintain
more details data about them.
"""

import logging
from typing import Type

from celery import shared_task
from crawlers import caches
from crawlers.context import TaskContext
from crawlers.network import JsonCache, json_cache
from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints, mdp_client
from notifications.models.task_notification import TaskNotification, task_notification
from repository.models import (
    Committee,
    CommitteeChair,
    CommitteeMember,
    ConstituencyResult,
    ContestedElection,
    Country,
    DeclaredInterest,
    DeclaredInterestCategory,
    Election,
    ElectionType,
    Experience,
    ExperienceCategory,
    House,
    HouseMembership,
    MaidenSpeech,
    PartyAssociation,
    Person,
    PhysicalAddress,
    SubjectOfInterest,
    SubjectOfInterestCategory,
    Town,
    UnlinkedConstituency,
    WebAddress,
)
from repository.models.party import get_or_create_party
from repository.models.posts import Post, PostHolder
from repository.resolution.constituency import (
    get_constituency_for_date,
    get_current_constituency,
)

from . import schema

log = logging.getLogger(__name__)


@shared_task
@task_notification(label="Update active member details")
@json_cache(caches.MEMBERS)
def update_active_member_details(
    notification: TaskNotification,
    cache: JsonCache | None = None,
    debug_max_updates: int | None = None,
):
    """
    In development you may provide a value for debug_max_updates to avoid
    updating hundreds of profiles unnecessarily.
    """

    members = Person.objects.filter(is_active=True)

    if debug_max_updates:
        members = members[:debug_max_updates]

    _update_details_for_members(members, notification=notification, cache=cache)


@shared_task
@task_notification(label="Update all member details")
@json_cache(caches.MEMBERS)
def update_all_member_details(
    notification: TaskNotification,
    cache: JsonCache | None = None,
):
    _update_details_for_members(
        Person.objects.all(), notification=notification, cache=cache
    )


@json_cache(caches.MEMBERS)
def _update_details_for_members(
    members,
    notification: TaskNotification,
    cache: JsonCache | None = None,
):
    for member in members:
        update_details_for_member(
            member.parliamentdotuk, notification=notification, cache=cache
        )

        if notification.finished:
            log.warning("Exiting early - notification marked as finished")
            break


@shared_task
@task_notification(label="Update details for single member")
@json_cache(caches.MEMBERS)
def update_details_for_member(
    member_id: int,
    notification: TaskNotification,
    cache: JsonCache | None = None,
):
    context = TaskContext(cache=cache, notification=notification)
    mdp_client.once(
        url=endpoints.member_biography(member_id),
        item_func=_update_member_biography,
        context=context,
    )


def _update_member_biography(data: schema.MemberFullBiog, context: TaskContext):
    person = Person.objects.get(parliamentdotuk=data.parliamentdotuk)
    log.info(f"Updating detail for member: {person}")

    _update_basic_details(person, data.basic_info)
    _update_house_membership(person, data.house_memberships)
    _update_historical_constituencies(person, data.constituencies)
    _update_party_associations(person, data.parties)
    _update_maiden_speeches(person, data.maiden_speeches)
    _update_committees(person, data.committees)
    _update_addresses(person, data.addresses)
    _update_declared_interests(person, data.declared_interests)
    _update_experiences(person, data.experiences)
    _update_subjects_of_interest(person, data.subjects)
    _update_posts(person, data.government_posts, "government")
    _update_posts(person, data.parliament_posts, "parliament")
    _update_posts(person, data.opposition_posts, "other")
    _update_elections_contested(person, data.contested_elections)


def _get_or_create_election(
    data: schema.Election,
) -> tuple[Election, bool]:
    """Convenience function as elections can be created via multiple routes
    including _update_historical_constituencies and _update_elections_contested."""

    election_type, _ = ElectionType.objects.get_or_create(name=data.type)
    election, created = Election.objects.get_or_create(
        parliamentdotuk=data.parliamentdotuk,
        defaults={
            "name": data.name,
            "election_type": election_type,
            "date": data.date,
        },
    )
    return election, created


def _update_basic_details(person: Person, data: schema.BasicInfo):
    person.given_name = data.first_name
    person.additional_name = data.middle_names
    person.family_name = data.family_name

    town_name = data.town_of_birth
    country_name = data.country_of_birth
    if country_name:
        person.country_of_birth, _ = Country.objects.get_or_create(name=country_name)

        if town_name:
            person.town_of_birth, _ = Town.objects.get_or_create(
                name=town_name,
                country=person.country_of_birth,
            )

    person.save()


def _update_house_membership(
    person: Person,
    memberships: list[schema.HouseMembership],
) -> None:
    for hm in memberships:
        house, _ = House.objects.get_or_create(name=hm.house)
        HouseMembership.objects.update_or_create(
            person=person,
            house=house,
            start=hm.start_date,
            defaults={
                "end": hm.end_date,
            },
        )


def _update_historical_constituencies(
    person: Person,
    historical_constituencies: list[schema.Constituency],
) -> None:
    for c in historical_constituencies:
        constituency_name = c.name
        election, _ = _get_or_create_election(c.election)

        constituency = get_constituency_for_date(constituency_name, election.date)

        if constituency is None:
            log.warning(
                f"Unknown constituency={constituency_name} for election={election} ({election.date})"
            )

            UnlinkedConstituency.objects.get_or_create(
                name=constituency_name,
                election=election,
                defaults={
                    "person": person,
                    "person_won": True,
                },
            )

        else:
            ConstituencyResult.objects.update_or_create(
                constituency=constituency,
                election=election,
                defaults={
                    "mp": person,
                    "start": c.start_date,
                    "end": c.end_date,
                },
            )


def _update_party_associations(
    person: Person, historical_parties: list[schema.PartyMembership]
) -> None:
    for p in historical_parties:
        party = get_or_create_party(p.parliamentdotuk, p.name)

        PartyAssociation.objects.update_or_create(
            person=person,
            party=party,
            start=p.start_date,
            defaults={
                "end": p.end_date,
            },
        )


def _update_committees(person: Person, committees: list[schema.Committee]) -> None:
    for c in committees:
        committee, _ = Committee.objects.update_or_create(
            parliamentdotuk=c.parliamentdotuk,
            defaults={
                "name": c.name,
            },
        )

        committee_membership, _ = CommitteeMember.objects.update_or_create(
            person=person,
            committee=committee,
            start=c.start_date,
            defaults={
                "end": c.end_date,
            },
        )

        for chair in c.chair:
            CommitteeChair.objects.update_or_create(
                member=committee_membership,
                start=chair.start_date,
                defaults={
                    "end": chair.end_date,
                },
            )


def _update_posts(
    person: Person,
    posts: list[schema.Post],
    post_type: str,
) -> None:
    for p in posts:
        post, _ = Post.objects.update_or_create(
            parliamentdotuk=p.parliamentdotuk,
            defaults={
                "type": post_type,
                "name": p.name,
                "hansard_name": p.hansard_name,
            },
        )

        PostHolder.objects.update_or_create(
            person=person,
            post=post,
            start=p.start_date,
            defaults={
                "end": p.end_date,
            },
        )


def _update_addresses(person: Person, addresses: list[schema.Address]) -> None:
    for a in addresses:
        if a.is_physical:
            PhysicalAddress.objects.update_or_create(
                person=person,
                description=a.type,
                defaults={
                    "address": a.address,
                    "postcode": a.postcode,
                    "phone": a.phone,
                    "fax": a.fax,
                    "email": a.email,
                },
            )
        else:
            WebAddress.objects.update_or_create(
                person=person,
                description=a.type,
                defaults={
                    "url": a.address,
                },
            )


def _update_maiden_speeches(
    person: Person, maiden_speeches: list[schema.MaidenSpeech]
) -> None:
    for speech in maiden_speeches:
        house, _ = House.objects.get_or_create(name=speech.house)
        MaidenSpeech.objects.update_or_create(
            person=person,
            house=house,
            defaults={
                "date": speech.date,
                "subject": speech.subject,
                "hansard": speech.hansard,
            },
        )


def _update_declared_interests(
    person: Person,
    interest_categories: list[schema.DeclaredInterest],
) -> None:
    for c in interest_categories:
        category, _ = DeclaredInterestCategory.objects.update_or_create(
            parliamentdotuk=c.category_id,
            defaults={
                "name": c.category_name,
            },
        )

        interests = c.interests
        for interest in interests:
            DeclaredInterest.objects.update_or_create(
                person=person,
                parliamentdotuk=interest.parliamentdotuk,
                defaults={
                    "category": category,
                    "description": interest.title,
                    "created": interest.date_created,
                    "amended": interest.date_amended,
                    "deleted": interest.date_deleted,
                    "registered_late": interest.is_registered_late,
                },
            )


def _update_subjects_of_interest(
    person: Person,
    subjects_of_interest: list[schema.SubjectOfInterest],
) -> None:
    for interest in subjects_of_interest:
        category, _ = SubjectOfInterestCategory.objects.get_or_create(
            title=interest.category
        )
        SubjectOfInterest.objects.get_or_create(
            person=person,
            category=category,
            subject=interest.entry,
        )


def _update_experiences(person: Person, experiences: list[schema.Experience]) -> None:
    for exp in experiences:
        category, _ = ExperienceCategory.objects.get_or_create(name=exp.type)
        Experience.objects.update_or_create(
            person=person,
            organisation=exp.organisation,
            title=exp.title,
            defaults={
                "category": category,
                "title": exp.title,
                "start": exp.start_date,
                "end": exp.end_date,
            },
        )


def _update_elections_contested(
    person: Person, contested: list[schema.ContestedElection]
) -> None:
    for c in contested:
        election, _ = _get_or_create_election(c.election)

        constituency_name = c.constituency_name

        # Find the constituency that was active at the date of the election
        # If we can't find one, use the most recent definition by that name.
        constituency = get_constituency_for_date(
            constituency_name,
            election.date,
        ) or get_current_constituency(constituency_name)

        if constituency is None:
            UnlinkedConstituency.objects.get_or_create(
                name=constituency_name,
                election=election,
                defaults={
                    "person": person,
                    "person_won": False,
                },
            )
        else:
            ContestedElection.objects.update_or_create(
                person=person,
                election=election,
                defaults={
                    "constituency": constituency,
                },
            )
