"""

"""

import logging
import time
from typing import (
    List,
    Optional,
    Type,
)

from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints
from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import (
    AddressResponseData,
    BasicInfoResponseData,
    BiographyEntriesResponseData,
    CommitteeResponseData,
    ConstituencyResponseData,
    ExperiencesResponseData,
    HouseMembershipResponseData,
    InterestCategoryResponseData,
    MemberBiographyResponseData,
    PartyResponseData,
    PostResponseData,
    SpeechResponseData,
    update_members,
)
from repository.models import (
    Committee,
    CommitteeMember,
    Constituency,
    ConstituencyResult,
    Country,
    Election,
    InterestCategory,
    MaidenSpeech,
    Party,
    PartyAssociation,
    Interest,
)
from repository.models.address import (
    PhysicalAddress,
    WebAddress,
)
from repository.models.committees import CommitteeChair
from repository.models.geography import Town
from repository.models.houses import (
    HOUSE_OF_COMMONS,
    House,
    HouseMembership,
)
from repository.models.person import Person
from repository.models.posts import (
    BasePost,
    BasePostMember,
    GovernmentPost,
    GovernmentPostMember,
    OppositionPost,
    OppositionPostMember,
    ParliamentaryPost,
    ParliamentaryPostMember,
)

log = logging.getLogger(__name__)


def update_active_mps_details():
    active_mp_parliamentdotuk_ids = [
        person.parliamentdotuk for person
        in Person.objects.filter(
            active=True,
            house__name=HOUSE_OF_COMMONS,
        )
    ]

    for parliamentdotuk_id in active_mp_parliamentdotuk_ids:
        update_members(
            endpoints.member_biography(parliamentdotuk_id),
            update_member_func=_update_member_biography,
            report_func=None,
            response_class=MemberBiographyResponseData,
        )
        time.sleep(1)


def _update_member_biography(data: MemberBiographyResponseData) -> Optional[str]:
    parliamentdotuk: int = data.get_parliament_id()

    person = Person.objects.get(parliamentdotuk=parliamentdotuk)
    log.info(f'Updating detail for mp: {person}')

    _update_basic_details(person, data.get_basic_info())
    _update_house_membership(person, data.get_house_memberships())
    _update_historical_constituencies(person, data.get_constituencies())
    _update_party_associations(person, data.get_parties())
    _update_maiden_speeches(person, data.get_maiden_speeches())
    _update_committees(person, data.get_committees())
    _update_addresses(person, data.get_addresses())
    _update_interests(person, data.get_interest_categories())
    _update_experiences(person, data.get_experiences())
    _update_biography_entries(person, data.get_biography_entries())
    _update_government_posts(person, data.get_goverment_posts())
    _update_parliamentary_posts(person, data.get_parliament_posts())
    _update_opposition_posts(person, data.get_opposition_posts())


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
        person: Person,
        memberships: List[HouseMembershipResponseData]
) -> None:
    for hm in memberships:
        house, _ = House.objects.get_or_create(name=hm.get_house())
        HouseMembership.objects.update_or_create(
            person=person,
            house=house,
            start=hm.get_start_date(),
            defaults={
                'end': hm.get_end_date()
            }
        )


def _update_historical_constituencies(
        person: Person,
        historical_constituencies: List[ConstituencyResponseData]
) -> None:
    for c in historical_constituencies:
        constituency, _ = Constituency.objects.get_or_create(
            parliamentdotuk=c.get_constituency_id(),
            defaults={
                'name': c.get_constituency_name()
            }
        )
        election, _ = Election.objects.update_or_create(
            parliamentdotuk=c.get_election_id(),
            defaults={
                'name': c.get_election_name(),
                'date': c.get_election_date(),
            })

        result, _ = ConstituencyResult.objects.update_or_create(
            constituency=constituency,
            election=election,
            defaults={
                'start': c.get_start_date(),
                'end': c.get_end_date(),
                'mp': person,
            }
        )


def _update_party_associations(
        person: Person,
        historical_parties: List[PartyResponseData]
) -> None:
    for p in historical_parties:
        party, _ = Party.objects.get_or_create(name=p.get_party_name())
        PartyAssociation.objects.update_or_create(
            person=person,
            party=party,
            start=p.get_start_date(),
            defaults={
                'end': p.get_end_date(),
            }
        )


def _update_committees(
        person: Person,
        committees: List[CommitteeResponseData]
) -> None:
    for c in committees:
        committee, _ = Committee.objects.update_or_create(
            parliamentdotuk=c.get_committee_id(),
            defaults={
                'name': c.get_committee_name()
            },
        )

        committee_membership, _ = CommitteeMember.objects.update_or_create(
            person=person,
            committee=committee,
            start=c.get_start_date(),
            defaults={
                'end': c.get_end_date(),
            }
        )

        for chair in c.get_chair():
            CommitteeChair.objects.update_or_create(
                member=committee_membership,
                start=chair.get_start_date(),
                defaults={
                    'end': chair.get_end_date(),
                }
            )


def _update_posts(
        person: Person,
        posts: List[PostResponseData],
        post_class: Type[BasePost],
        membership_class: Type[BasePostMember]
) -> None:
    for p in posts:
        post, _ = post_class.objects.update_or_create(
            parliamentdotuk=p.get_post_id(),
            defaults={
                'name': p.get_post_name(),
                'hansard_name': p.get_post_hansard_name(),
            }
        )

        membership_class.objects.update_or_create(
            person=person,
            post=post,
            start=p.get_start_date(),
            defaults={
                'end': p.get_end_date(),
            }
        )


def _update_government_posts(
        person: Person,
        posts: List[PostResponseData]
) -> None:
    _update_posts(
        person,
        posts,
        GovernmentPost,
        GovernmentPostMember
    )


def _update_parliamentary_posts(
        person: Person,
        posts: List[PostResponseData]
) -> None:
    _update_posts(
        person,
        posts,
        ParliamentaryPost,
        ParliamentaryPostMember
    )


def _update_opposition_posts(
        person: Person,
        posts: List[PostResponseData]
) -> None:
    _update_posts(
        person,
        posts,
        OppositionPost,
        OppositionPostMember
    )


def _update_addresses(
        person: Person,
        addresses: List[AddressResponseData]
) -> None:
    for a in addresses:
        if a.get_is_physical():
            PhysicalAddress.objects.update_or_create(
                person=person,
                description=a.get_type(),
                defaults={
                    'address': a.get_address(),
                    'postcode': a.get_postcode(),
                    'phone': a.get_phone(),
                    'fax': a.get_fax(),
                }
            )
        else:
            WebAddress.objects.update_or_create(
                person=person,
                description=a.get_type(),
                defaults={
                    'url': a.get_address(),
                }
            )


def _update_maiden_speeches(
        person: Person,
        maiden_speeches: List[SpeechResponseData]
) -> None:
    for speech in maiden_speeches:
        house, _ = House.objects.get_or_create(name=speech.get_house())
        MaidenSpeech.objects.update_or_create(
            person=person,
            house=house,
            defaults={
                'date': speech.get_date(),
                'subject': speech.get_subject(),
                'hansard': speech.get_hansard(),
            }
        )


def _update_interests(
        person: Person,
        interest_categories: List[InterestCategoryResponseData]
) -> None:
    for c in interest_categories:
        category, _ = InterestCategory.objects.update_or_create(
            parliamentdotuk=c.get_category_id(),
            defaults={
                'name': c.get_category_name(),
            })

        interests = c.get_interests()
        for interest in interests:
            Interest.objects.update_or_create(
                person=person,
                parliamentdotuk=interest.get_interest_id(),
                defaults={
                    'category': category,
                    'description': interest.get_title(),
                    'created': interest.get_date_created(),
                    'amended': interest.get_date_amended(),
                    'deleted': interest.get_date_deleted(),
                    'registered_late': interest.get_registered_late(),
                }
            )


def _update_biography_entries(
        person: Person,
        interests: List[BiographyEntriesResponseData]
) -> None:
    # TODO Implement!
    pass


def _update_experiences(
        person: Person,
        interests: List[ExperiencesResponseData]
) -> None:
    # TODO Implement!
    pass
