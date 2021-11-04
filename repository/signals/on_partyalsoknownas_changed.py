from django.db.models.signals import post_save
from django.dispatch import receiver

from repository.models import ConstituencyCandidate, PartyAlsoKnownAs


@receiver(
    post_save,
    sender=PartyAlsoKnownAs,
    dispatch_uid="update_constituencycandidate_party_when_partyaka_canonical_changed",
)
def update_constituencycandidate_party_when_partyaka_canonical_changed(
    sender,
    instance: PartyAlsoKnownAs,
    **kwargs,
):
    candidates = ConstituencyCandidate.objects.filter(party_name=instance.alias)
    for x in candidates:
        x.party = instance.canonical

    ConstituencyCandidate.objects.bulk_update(
        list(candidates),
        ["party"],
        batch_size=50,
    )
