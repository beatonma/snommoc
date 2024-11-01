from django.core.management import BaseCommand
from repository.models import CommonsDivisionVote, DivisionVoteType

cache = {}


class Command(BaseCommand):
    def handle(self, *args, **options):
        votes = CommonsDivisionVote.objects.filter(vote_type__isnull=True)

        print(f"Migrating {votes.count()} votes")
        for n, vote in enumerate(votes):
            if n % 1000 == 0:
                print(n)
            _type = vote.depr__vote_type

            if _type in cache:
                vote_type = cache[_type]
            else:
                vote_type, _ = DivisionVoteType.objects.get_or_create(
                    name=vote.depr__vote_type
                )
                cache[_type] = vote_type

            vote.vote_type = vote_type
            vote.save()

        print(f"{votes.count()} votes migrated")
