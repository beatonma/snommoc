from functools import partial

from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi import schema as common_schema
from crawlers.parliamentdotuk.tasks.openapi.members import schema
from crawlers.parliamentdotuk.tasks.openapi.parties.update import update_party
from repository.models import (
    AddressType,
    Committee,
    CommitteeMember,
    Constituency,
    ConstituencyRepresentative,
    ContestedElection,
    Experience,
    ExperienceCategory,
    House,
    HouseMembership,
    LordsType,
    Organisation,
    Party,
    PartyAffiliation,
    Person,
    PhysicalAddress,
    RegisteredInterest,
    RegisteredInterestCategory,
    SubjectOfInterest,
    SubjectOfInterestCategory,
    WebAddress,
)
from repository.models.person import PersonStatus
from repository.models.posts import Post, PostHolder


@task_context(cache_name=caches.MEMBERS)
def update_members(context: TaskContext) -> None:
    client_func = openapi_client.foreach
    if context.item_id:
        endpoint_url = endpoints.member_basic(context.item_id)
        client_func = openapi_client.get
    elif context.historic:
        endpoint_url = endpoints.MEMBERS_HISTORICAL
    else:
        endpoint_url = endpoints.MEMBERS_CURRENT

    client_func(
        endpoint_url=endpoint_url,
        item_func=_update_member_detail,
        context=context,
    )
    finalize_members_update()


def _update_member_detail(response_data: dict, context: TaskContext):
    basic_info = (
        common_schema.ResponseItem[schema.MemberBasic]
        .model_validate(response_data)
        .value
    )
    member_id = basic_info.parliamentdotuk
    person = _update_member_basic(basic_info)

    fetch = partial(openapi_client.get, context=context, func_kwargs={"person": person})

    fetch(
        endpoint_url=endpoints.member_biography(member_id),
        item_func=_update_member_biography,
    )

    fetch(
        endpoint_url=endpoints.member_contact(member_id),
        item_func=_update_member_contact,
    )

    fetch(
        endpoint_url=endpoints.member_experience(member_id),
        item_func=_update_experiences,
    )

    fetch(
        endpoint_url=endpoints.member_registered_interests(member_id),
        item_func=_update_registered_interests,
    )

    fetch(
        endpoint_url=endpoints.member_subjects_of_interest(member_id),
        item_func=_update_subjects_of_interest,
    )


def _update_member_basic(basic_info: schema.MemberBasic) -> Person:
    lords_type = None
    if _type := basic_info.status.lords_type:
        lords_type, _ = LordsType.objects.get_or_create(name=_type)

    house = None
    if _house := basic_info.status.house:
        house, _ = House.objects.get_or_create(name=_house)

    person, _ = Person.objects.update_or_create(
        parliamentdotuk=basic_info.parliamentdotuk,
        defaults={
            "name": basic_info.name,
            "sort_name": basic_info.list_as,
            "full_title": basic_info.full_title,
            "gender": basic_info.gender,
            "party": update_party(basic_info.party) if basic_info.party else None,
            "house": house,
            "lords_type": lords_type,
        },
    )
    status_data = basic_info.status
    person_status, _ = PersonStatus.objects.update_or_create(
        person=person,
        defaults={
            "is_current": status_data.is_current,
            "is_active": status_data.is_active,
            "description": status_data.description,
            "notes": status_data.notes,
            "start": status_data.since,
        },
    )

    return person


def _update_member_biography(
    response_data: dict, context: TaskContext, func_kwargs: dict
):
    biography = (
        common_schema.ResponseItem[schema.MemberBiography]
        .model_validate(response_data)
        .value
    )
    person = func_kwargs["person"]

    _update_posts(person, biography.government_posts, "government")
    _update_posts(person, biography.opposition_posts, "opposition")
    _update_posts(person, biography.other_posts, "other")

    _update_historical_constituencies(person, biography.representations)
    _update_historical_houses(person, biography.house_memberships)
    _update_historical_parties(person, biography.party_affiliations)
    _update_contested_elections(person, biography.elections_contested)
    _update_committee_memberships(person, biography.committees)


def _update_member_contact(
    response_data: dict,
    context: TaskContext,
    func_kwargs: dict,
):
    contact = (
        common_schema.ResponseItem[list[schema.ContactInfo]]
        .model_validate(response_data)
        .value
    )
    person = func_kwargs["person"]

    for item in contact:
        item_type, _ = AddressType.objects.get_or_create(
            parliamentdotuk=item.type_id,
            defaults={
                "name": item.type_name,
                "description": item.type_description,
            },
        )

        if item.is_web_address:
            WebAddress.objects.update_or_create(
                person=person,
                type=item_type,
                defaults={"url": item.address, "is_preferred": item.is_preferred},
            )
        else:
            PhysicalAddress.objects.update_or_create(
                person=person,
                type=item_type,
                defaults={
                    "is_preferred": item.is_preferred,
                    "address": item.address,
                    "postcode": item.postcode,
                    "phone": item.phone,
                    "fax": item.fax,
                    "email": item.email,
                },
            )


def _update_posts(
    person: Person,
    posts: list[schema.Post],
    post_type: str,
) -> None:
    for item in posts:
        post, _ = Post.objects.update_or_create(
            parliamentdotuk=item.parliamentdotuk,
            type=post_type,
            defaults={
                "name": item.name,
                "additional_info": item.additional_info,
                "additional_info_link": item.additional_info_link,
            },
        )

        PostHolder.objects.update_or_create(
            person=person,
            post=post,
            start=item.start,
            defaults={
                "end": item.end,
            },
        )


def _update_historical_constituencies(
    person: Person,
    data: list[schema.ConstituencyRepresentation],
):
    for item in data:
        constituency, _ = Constituency.objects.update_or_create(
            parliamentdotuk=item.constituency_id,
            defaults={
                "start": item.constituency_start,
                "end": item.constituency_end,
            },
            create_defaults={
                "name": item.constituency_name,
                "start": item.constituency_start,
                "end": item.constituency_end,
            },
        )

        ConstituencyRepresentative.objects.update_or_create(
            constituency=constituency,
            person=person,
            start=item.representation_start,
            defaults={
                "end": item.representation_end,
            },
        )


def _update_historical_houses(person: Person, data: list[schema.HouseMembership]):
    for item in data:
        house, _ = House.objects.get_or_create(name=item.house_name)
        HouseMembership.objects.update_or_create(
            person=person,
            house=house,
            start=item.start,
            defaults={
                "end": item.end,
            },
        )


def _update_contested_elections(person: Person, data: list[schema.ContestedElection]):
    for item in data:
        constituency, _ = Constituency.objects.get_or_create(
            parliamentdotuk=item.constituency_id,
            defaults={
                "name": item.constituency_name,
            },
        )

        ContestedElection.objects.update_or_create(
            person=person,
            date=item.date,
            constituency=constituency,
        )


def _update_historical_parties(person: Person, data: list[schema.PartyAffiliation]):
    for item in data:
        party, _ = Party.objects.resolve(
            parliamentdotuk=item.party_id,
            name=item.party_name,
        )

        PartyAffiliation.objects.update_or_create(
            party=party,
            person=person,
            start=item.start,
            defaults={
                "end": item.end,
            },
        )


def _update_committee_memberships(
    person: Person, data: list[schema.CommitteeMembership]
):
    for item in data:
        committee, _ = Committee.objects.get_or_create(
            parliamentdotuk=item.committee_id, defaults={"name": item.committee_name}
        )

        CommitteeMember.objects.update_or_create(
            person=person,
            committee=committee,
            start=item.start,
            defaults={"end": item.end},
        )


def _update_registered_interests(
    response_data: dict, context: TaskContext, func_kwargs: dict
):
    categories = (
        common_schema.ResponseItem[list[schema.RegisteredInterestCategory]]
        .model_validate(response_data)
        .value
    )
    person = func_kwargs["person"]
    house = person.house

    for item in categories:
        category = _get_registered_interest_category(house, item)

        for index, interest in enumerate(item.interests):
            parent, _ = RegisteredInterest.objects.update_or_create(
                parliamentdotuk=interest.interest_id,
                category=category,
                person=person,
                defaults={
                    "description": interest.description,
                    "description_data": interest.description_data,
                    "created": interest.created_at,
                    "amended": interest.last_amended_at,
                    "deleted": interest.deleted_at,
                    "is_correction": interest.is_correction,
                },
            )

            for child in interest.child_interests:
                RegisteredInterest.objects.update_or_create(
                    parliamentdotuk=child.interest_id,
                    category=category,
                    person=person,
                    parent=parent,
                    defaults={
                        "description": child.description,
                        "description_data": child.description_data,
                        "created": child.created_at,
                        "amended": child.last_amended_at,
                        "deleted": child.deleted_at,
                        "is_correction": child.is_correction,
                    },
                )


def _get_registered_interest_category(
    house: House, item: schema.RegisteredInterestCategory
):
    category, _ = RegisteredInterestCategory.objects.update_or_create(
        codename_major=item.codename_major,
        codename_minor=item.codename_minor,
        house=house,
        defaults={"name": item.name, "sort_order": item.sort_order},
    )
    return category


def _update_subjects_of_interest(
    response_data: dict, context: TaskContext, func_kwargs: dict
):
    subjects = (
        common_schema.ResponseItem[list[schema.SubjectOfInterest]]
        .model_validate(response_data)
        .value
    )
    person = func_kwargs["person"]

    for item in subjects:
        category, _ = SubjectOfInterestCategory.objects.get_or_create(
            title=item.category
        )

        for subject in item.descriptions:
            SubjectOfInterest.objects.get_or_create(
                person=person,
                category=category,
                description=subject,
            )


def _update_experiences(response_data: dict, context: TaskContext, func_kwargs: dict):
    experiences = (
        common_schema.ResponseItem[list[schema.Experience]]
        .model_validate(response_data)
        .value
    )
    person = func_kwargs["person"]

    for item in experiences:
        category, _ = ExperienceCategory.objects.get_or_create(
            parliamentdotuk=item.type_id,
            defaults={"name": item.type},
        )
        organisation = None
        if item.organisation:
            organisation, _ = Organisation.objects.get_or_create(name=item.organisation)

        Experience.objects.update_or_create(
            parliamentdotuk=item.experience_id,
            person=person,
            category=category,
            start=item.start,
            defaults={
                "title": item.title,
                "organisation": organisation,
                "end": item.end,
            },
        )


def finalize_members_update():
    """Apply any post-processing required after updating member data"""
    _finalize_registered_interest_category_order()
    pass


def _finalize_registered_interest_category_order():
    """RegisteredInterestCategory data from the API provides a sort_order
    field but its values for the HoC are not usable (Lords values are fine).

    Here we use the parsed values (codename_major, codename_minor) to sort
    the complete set of categories, then persist that order via sort_order."""
    categories = RegisteredInterestCategory.objects.filter(
        house=House.objects.commons()
    ).order_by("codename_major", "codename_minor")

    for order, category in enumerate(categories):
        category.sort_order = order
        category.save(update_fields=("sort_order",))
