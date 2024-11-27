from typing import Type

from crawlers.parliamentdotuk.tasks.openapi.divisions import schema
from repository.models import DivisionVoteType, Party, Person
from repository.models.divisions import (
    DivisionSharedProperties,
    DivisionVoteSharedProperties,
)


def create_votes[
    T: DivisionSharedProperties
](
    division: T,
    division_vote_class: Type[DivisionVoteSharedProperties],
    votes: list[schema.Member],
    vote_type_name: str,
    is_teller: bool = False,
):
    vote_type, _ = DivisionVoteType.objects.get_or_create(name=vote_type_name)
    for vote in votes:
        party = Party.objects.get_or_none(name=vote.party)
        person = Person.objects.get_member(
            vote.member_id,
            name=vote.name,
            defaults={"party": party},
        )
        _, created = division_vote_class.objects.update_or_create(
            person=person,
            division=division,
            defaults={
                "vote_type": vote_type,
                "is_teller": is_teller,
            },
        )
