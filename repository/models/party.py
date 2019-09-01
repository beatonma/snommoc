from typing import Dict

from django.db import models

from api import contract


class Party(models.Model):
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=16, default=name)
    long_name = models.CharField(max_length=64, default=name)

    @classmethod
    def create(cls, name, short_name, long_name) -> 'Party':
        party = cls(name=name, short_name=short_name, long_name=long_name)
        party.save()
        return party

    def to_json(self) -> Dict:
        return {
            contract.PARTY: self.name,
            contract.PARTY_SHORT: self.short_name,
            contract.PARTY_LONG: self.long_name,
        }

    class Meta:
        verbose_name_plural = 'Parties'
