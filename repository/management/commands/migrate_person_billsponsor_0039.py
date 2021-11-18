from django.core.management import BaseCommand

from repository.models import BillSponsor, Person
from repository.resolution.members import get_member_by_name, normalize_name


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Apply name normalization to existing data after repository migration 0039."""
        _migrate_people_normalized_names()
        _migrate_billsponsor_normalized_names()


def _migrate_people_normalized_names():
    people = Person.objects.all()
    for p in people:
        normalized_name = normalize_name(p.name)
        if normalized_name != p.name:
            print(f" [{p.pk}] {p.name} -> {normalized_name}")
            p.name = normalized_name
            p.save()


def _migrate_billsponsor_normalized_names():
    sponsors = BillSponsor.objects.all()

    for sponsor in sponsors:
        try:
            name = sponsor.name or sponsor.person.name
        except AttributeError:
            print(f"[{sponsor.id}] No name!")
            continue

        normalized_name = normalize_name(name)

        person = get_member_by_name(normalized_name)
        if sponsor.person is not None and person != sponsor.person:
            print(
                f"Resolved person {person} != existing person {sponsor.person} (name={normalized_name}, id={sponsor.id})"
            )

        elif sponsor.person != person or name != normalized_name:
            print(f"Update {name} [{sponsor.person}] -> {normalized_name} [{person}]")

            existing = BillSponsor.objects.filter(
                bill_id=sponsor.bill_id,
                person=person,
            )
            pre_existing = existing.count()
            if pre_existing > 0:
                print(f"Clash detected {name} | {person} --- {existing}")

                if pre_existing == 1:
                    clash = existing.first()
                    print(f"Deleting duplicate {clash}")
                    clash.delete()

            sponsor.name = normalized_name
            sponsor.person = person
            sponsor.save()
