from typing import Dict

from django.db import models

from api import contract


class Party(models.Model):
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=16)
    long_name = models.CharField(max_length=64)

    @classmethod
    def create(cls, name, shortname, longname) -> 'Party':
        party = cls(name=name, short_name=shortname, long_name=longname)
        party.save()
        return party

    def to_json(self) -> Dict:
        return {
            contract.PARTY: self.name,
            contract.PARTY_SHORT: self.short_name,
            contract.PARTY_LONG: self.long_name,
        }
