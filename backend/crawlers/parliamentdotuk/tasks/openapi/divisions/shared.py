from crawlers.parliamentdotuk.tasks.openapi.common import resolve_person
from crawlers.parliamentdotuk.tasks.openapi.divisions import schema
from repository.models import DivisionVoteType
from repository.models.divisions import Division, DivisionVote


def create_votes[T: Division](
    division: T,
    votes: list[schema.Member],
    vote_type_name: str,
    is_teller: bool = False,
):
    vote_type, _ = DivisionVoteType.objects.get_or_create(name=vote_type_name)
    for vote in votes:
        person = resolve_person(vote.member_id, vote.name, party_name=vote.party)

        _, created = DivisionVote.objects.update_or_create(
            person=person,
            division=division,
            defaults={
                "vote_type": vote_type,
                "is_teller": is_teller,
            },
        )
