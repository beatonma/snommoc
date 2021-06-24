"""
Tasks for updating details on active members.

Active members are of higher interest than historical ones so we maintain
more details data about them.
"""
import logging
from typing import Callable, List, Optional, Tuple, Type

from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException

from celery import shared_task
from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints
from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import (
    AddressResponseData,
    BasicInfoResponseData,
    CommitteeResponseData,
    ConstituencyResponseData,
    ContestedElectionResponseData,
    DeclaredInterestCategoryResponseData,
    ElectionResponseData,
    ExperiencesResponseData,
    HouseMembershipResponseData,
    MemberBiographyResponseData,
    PartyResponseData,
    PostResponseData,
    SpeechResponseData,
    SubjectsOfInterestResponseData,
    update_members,
)
from notifications.models.task_notification import task_notification
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
    GovernmentPost,
    GovernmentPostMember,
    House,
    HouseMembership,
    MaidenSpeech,
    OppositionPost,
    OppositionPostMember,
    ParliamentaryPost,
    ParliamentaryPostMember,
    PartyAssociation,
    Person,
    PhysicalAddress,
    SubjectOfInterest,
    SubjectOfInterestCategory,
    Town,
    UnlinkedConstituency,
    WebAddress,
)
from repository.models.address import PHONE_NUMBER_REGION
from repository.resolution.constituency import (
    get_constituency_for_date,
    get_current_constituency,
)
from repository.models.party import get_or_create_party
from repository.models.posts import (
    BasePost,
    BasePostMember,
    get_current_post_for_person,
)
from crawlers.network import json_cache

CACHE_NAME = "active-members"

log = logging.getLogger(__name__)


@shared_task
@task_notification(label="Update active member details")
@json_cache(name=CACHE_NAME)
def update_active_member_details(
    debug_max_updates: Optional[int] = None,
    **kwargs,
):
    """
    In development you may provide a value for debug_max_updates to avoid
    updating hundreds of profiles unnecessarily.
    """

    members = Person.objects.filter(active=True)

    if debug_max_updates:
        members = members[:debug_max_updates]

    _update_details_for_members(members, **kwargs)


@shared_task
@task_notification(label="Update all member details")
@json_cache(name=CACHE_NAME)
def update_all_member_details(**kwargs):
    _update_details_for_members(Person.objects.all(), **kwargs)


@json_cache(name=CACHE_NAME)
def _update_details_for_members(members, **kwargs):
    for member in members:
        update_details_for_member(member.parliamentdotuk, **kwargs)

        if kwargs["notification"].finished:
            log.warning("Exiting early - notification marked as finished")
            break


@shared_task
@task_notification(label="Update details for single member")
@json_cache(name=CACHE_NAME)
def update_details_for_member(member_id: int, **kwargs):
    update_members(
        endpoints.member_biography(member_id),
        update_member_func=_update_member_biography,
        response_class=MemberBiographyResponseData,
        **kwargs,
    )


def _update_member_biography(data: MemberBiographyResponseData):
    parliamentdotuk: int = data.get_parliament_id()

    person = Person.objects.get(parliamentdotuk=parliamentdotuk)
    log.info(f"Updating detail for member: {person}")

    _update_basic_details(person, data.get_basic_info())
    _update_house_membership(person, data.get_house_memberships())
    _update_historical_constituencies(person, data.get_constituencies())
    _update_party_associations(person, data.get_parties())
    _update_maiden_speeches(person, data.get_maiden_speeches())
    _update_committees(person, data.get_committees())
    _update_addresses(person, data.get_addresses())
    _update_declared_interests(person, data.get_declared_interest_categories())
    _update_experiences(person, data.get_experiences())
    _update_subjects_of_interest(person, data.get_subjects_of_interest())
    _update_government_posts(person, data.get_goverment_posts())
    _update_parliamentary_posts(person, data.get_parliament_posts())
    _update_opposition_posts(person, data.get_opposition_posts())
    _update_elections_contested(person, data.get_contested_elections())

    _postprocess_update(person)


def _postprocess_update(person: Person) -> None:
    """Update any values that need to be calculated after API data is stored."""
    _postprocess_update_current_post(person)


def _get_or_create_election(
    data: Optional[ElectionResponseData],
) -> Tuple[Election, bool]:
    """Convenience function as elections can be created via multiple routes
    including _update_historical_constituencies and _update_elections_contested."""
    election_type, _ = ElectionType.objects.get_or_create(name=data.get_election_type())
    election, created = Election.objects.get_or_create(
        parliamentdotuk=data.get_election_id(),
        defaults={
            "name": data.get_election_name(),
            "election_type": election_type,
            "date": data.get_election_date(),
        },
    )
    return election, created


def _catch_item_errors(person: Person, items: List, func: Callable) -> None:
    for item in items:
        func(item)


def _update_basic_details(person: Person, data: BasicInfoResponseData):
    person.given_name = data.get_first_name()
    person.additional_name = data.get_middle_names()
    person.family_name = data.get_family_name()

    town_name = data.get_town_of_birth()
    country_name = data.get_country_of_birth()
    if country_name:
        person.country_of_birth, _ = Country.objects.get_or_create(name=country_name)

        if town_name:
            person.town_of_birth, _ = Town.objects.get_or_create(
                name=town_name,
                country=person.country_of_birth,
            )

    person.save()


def _update_house_membership(
    person: Person, memberships: List[HouseMembershipResponseData]
) -> None:
    def _item_func(hm: HouseMembershipResponseData):
        house, _ = House.objects.get_or_create(name=hm.get_house())
        HouseMembership.objects.update_or_create(
            person=person,
            house=house,
            start=hm.get_start_date(),
            defaults={
                "end": hm.get_end_date(),
            },
        )

    _catch_item_errors(person, memberships, _item_func)


def _update_historical_constituencies(
    person: Person, historical_constituencies: List[ConstituencyResponseData]
) -> None:
    def _item_func(c: ConstituencyResponseData):
        constituency_name = c.get_constituency_name()
        election, _ = _get_or_create_election(c.get_election())

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
                    "start": c.get_start_date(),
                    "end": c.get_end_date(),
                },
            )

    _catch_item_errors(person, historical_constituencies, _item_func)


def _update_party_associations(
    person: Person, historical_parties: List[PartyResponseData]
) -> None:
    def _item_func(p):
        party = get_or_create_party(p.get_party_id(), p.get_party_name())

        PartyAssociation.objects.update_or_create(
            person=person,
            party=party,
            start=p.get_start_date(),
            defaults={
                "end": p.get_end_date(),
            },
        )

    _catch_item_errors(person, historical_parties, _item_func)


def _update_committees(person: Person, committees: List[CommitteeResponseData]) -> None:
    def _item_func(c):
        committee, _ = Committee.objects.update_or_create(
            parliamentdotuk=c.get_committee_id(),
            defaults={
                "name": c.get_committee_name(),
            },
        )

        committee_membership, _ = CommitteeMember.objects.update_or_create(
            person=person,
            committee=committee,
            start=c.get_start_date(),
            defaults={
                "end": c.get_end_date(),
            },
        )

        for chair in c.get_chair():
            CommitteeChair.objects.update_or_create(
                member=committee_membership,
                start=chair.get_start_date(),
                defaults={
                    "end": chair.get_end_date(),
                },
            )

    _catch_item_errors(person, committees, _item_func)


def _update_posts(
    person: Person,
    posts: List[PostResponseData],
    post_class: Type[BasePost],
    membership_class: Type[BasePostMember],
) -> None:
    def _item_func(p):
        post, _ = post_class.objects.update_or_create(
            parliamentdotuk=p.get_post_id(),
            defaults={
                "name": p.get_post_name(),
                "hansard_name": p.get_post_hansard_name(),
            },
        )

        membership_class.objects.update_or_create(
            person=person,
            post=post,
            start=p.get_start_date(),
            defaults={
                "end": p.get_end_date(),
            },
        )

    _catch_item_errors(person, posts, _item_func)


def _update_government_posts(person: Person, posts: List[PostResponseData]) -> None:
    _update_posts(person, posts, GovernmentPost, GovernmentPostMember)


def _update_parliamentary_posts(person: Person, posts: List[PostResponseData]) -> None:
    _update_posts(person, posts, ParliamentaryPost, ParliamentaryPostMember)


def _update_opposition_posts(person: Person, posts: List[PostResponseData]) -> None:
    _update_posts(person, posts, OppositionPost, OppositionPostMember)


def _update_addresses(person: Person, addresses: List[AddressResponseData]) -> None:
    def _str_to_phonenumber(number: str):
        try:
            return PhoneNumber.from_string(number, region=PHONE_NUMBER_REGION)
        except NumberParseException:
            return None

    def _item_func(a):
        if a.get_is_physical():

            PhysicalAddress.objects.update_or_create(
                person=person,
                description=a.get_type(),
                defaults={
                    "address": a.get_address(),
                    "postcode": a.get_postcode(),
                    "phone": _str_to_phonenumber(a.get_phone()),
                    "fax": _str_to_phonenumber(a.get_fax()),
                    "email": a.get_email(),
                },
            )
        else:
            WebAddress.objects.update_or_create(
                person=person,
                description=a.get_type(),
                defaults={
                    "url": a.get_address(),
                },
            )

    _catch_item_errors(person, addresses, _item_func)


def _update_maiden_speeches(
    person: Person, maiden_speeches: List[SpeechResponseData]
) -> None:
    def _item_func(speech):
        house, _ = House.objects.get_or_create(name=speech.get_house())
        MaidenSpeech.objects.update_or_create(
            person=person,
            house=house,
            defaults={
                "date": speech.get_date(),
                "subject": speech.get_subject(),
                "hansard": speech.get_hansard(),
            },
        )

    _catch_item_errors(person, maiden_speeches, _item_func)


def _update_declared_interests(
    person: Person, interest_categories: List[DeclaredInterestCategoryResponseData]
) -> None:
    def _item_func(c):
        category, _ = DeclaredInterestCategory.objects.update_or_create(
            parliamentdotuk=c.get_category_id(),
            defaults={
                "name": c.get_category_name(),
            },
        )

        interests = c.get_interests()
        for interest in interests:
            DeclaredInterest.objects.update_or_create(
                person=person,
                parliamentdotuk=interest.get_interest_id(),
                defaults={
                    "category": category,
                    "description": interest.get_title(),
                    "created": interest.get_date_created(),
                    "amended": interest.get_date_amended(),
                    "deleted": interest.get_date_deleted(),
                    "registered_late": interest.get_registered_late(),
                },
            )

    _catch_item_errors(person, interest_categories, _item_func)


def _update_subjects_of_interest(
    person: Person, subjects_of_interest: List[SubjectsOfInterestResponseData]
) -> None:
    def _item_func(interest):
        category, _ = SubjectOfInterestCategory.objects.get_or_create(
            title=interest.get_category()
        )
        SubjectOfInterest.objects.get_or_create(
            person=person, category=category, subject=interest.get_entry()
        )

    _catch_item_errors(person, subjects_of_interest, _item_func)


def _update_experiences(
    person: Person, experiences: List[ExperiencesResponseData]
) -> None:
    def _item_func(exp):
        category, _ = ExperienceCategory.objects.get_or_create(name=exp.get_type())
        Experience.objects.update_or_create(
            person=person,
            organisation=exp.get_organisation(),
            title=exp.get_title(),
            defaults={
                "category": category,
                "title": exp.get_title(),
                "start": exp.get_start_date(),
                "end": exp.get_end_date(),
            },
        )

    _catch_item_errors(person, experiences, _item_func)


def _update_elections_contested(
    person: Person, contested: List[ContestedElectionResponseData]
) -> None:
    def _item_func(c):
        election, _ = _get_or_create_election(c.get_election())

        constituency_name = c.get_constituency_name()

        # Find the constituency that was active at the date of the election
        # If we can't find one, use the most recent definition by that name.
        constituency = (
            get_constituency_for_date(
                constituency_name,
                election.date,
            )
            or get_current_constituency(constituency_name)
        )

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

    _catch_item_errors(person, contested, _item_func)


def _postprocess_update_current_post(person: Person) -> None:
    current_post_membership = get_current_post_for_person(person)

    if current_post_membership is None:
        person.current_post = None
    else:
        person.current_post = current_post_membership.post.name

    person.save()
