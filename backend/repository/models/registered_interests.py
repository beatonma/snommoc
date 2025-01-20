from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from repository.models.mixins import ParliamentDotUkMixin, PersonMixin


class RegisteredInterestCategory(BaseModel):
    codename_major = models.PositiveSmallIntegerField()
    codename_minor = models.CharField(max_length=5, null=True, blank=True)
    name = models.CharField(max_length=512)
    house = models.ForeignKey("House", on_delete=models.CASCADE)
    sort_order = models.PositiveSmallIntegerField(default=0)

    def codename(self):
        return "".join(
            [str(x) for x in (self.codename_major, self.codename_minor) if x]
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Registered interest categories")
        constraints = (
            models.UniqueConstraint(
                fields=("codename_major", "codename_minor", "house"),
                name="unique_codename_per_house",
            ),
        )
        ordering = (
            "house",
            "sort_order",
        )


class RegisteredInterest(
    ParliamentDotUkMixin,
    PersonMixin,
    BaseModel,
):
    """Declared investments/involvements/relationships that a person has with
    organisations that could potentially influence their work in Parliament."""

    parliamentdotuk = models.PositiveIntegerField(
        help_text=_("ID used on parliament.uk website - unique per person")
    )  # *Not* unique globally or even per category. Not clear what the intended scope is!
    category = models.ForeignKey("RegisteredInterestCategory", on_delete=models.CASCADE)
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="registered_interests",
    )
    description = models.TextField()
    description_data = models.JSONField(default=dict)

    created = models.DateField(blank=True, null=True)
    amended = models.DateField(blank=True, null=True)
    deleted = models.DateField(blank=True, null=True)
    is_correction = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "RegisteredInterest",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.person}: {self.description}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("parliamentdotuk", "person"), name="unique_id_per_person"
            )
        ]
        ordering = ("-amended", "-created")


"""
TODO

Complete investigation of potential fields to use instead of/as well as monolithic `description`.
Notes being kept in SublimeText

import os
def show(name: str):
    os.system("clear")
    keys = set()
    for x in RegisteredInterest.objects.filter(category__name__istartswith=name):
        print(x.description)
        print("")
        if "\n" not in x.description and ":" not in x.description:
            continue
        for line in x.description.split("\n"):
            if ":" in line:
                keys.add(line.split(":")[0] + ":")
            else:
                keys.add(line)
    print("Unique keys:")
    for x in sorted(keys):
        print(f"  - {x}")
 

NOTES:


Common:
(Registered date; updated date)
(Registered date)
(Updated date)


1. Employment and earnings

Role, work or services: str
Payer: str
Payment: str
Received on data. Hours:
Remuneration: str
Hours:
Until: date
Received on
ACOBA consulted
Additional information
Completed or provided on
Donated to: str
From
Paid directly to
Payment expected
Ultimate payer
Work or services


2. (a) Support linked to an MP but received by a local party organisation or indirectly via a central party organisation
Name of donor: str
Address of donor: str
Amount of donation or nature and value if donation in kind: str
Donor status: str


2. (b) Any other support not included in Category 2(a)
Name of donor: str
Address of donor: "private" | str
Amount of donation or nature and value if donation in kind: str
Date received: date / str "$date to $date"
Date accepted: date
Donor status: str


3. Gifts, benefits and hospitality from UK sources
Name of donor: str
Address of donor: str
Amount of donation or nature and value if donation in kind: str
Date received: date
Date accepted: date
Donor status: str


4. Visits outside the UK
Name of donor: str
Address of donor: str
Estimate of the probable value (or amount of any donation): str
Destination of visit: str
Dates of visit: str
Purpose of visit: str


5. Gifts and benefits from sources outside the UK
Name of donor: str
Address of donor: str
Amount of donation or nature and value if donation in kind: str
Date received: date
Date accepted: date
Donor status: str


6. Land and property portfolio with a value over £100,000 and where indicated, the portfolio provides a rental income of over £10,000 a year
Type of land/property: str
Number of properties: int
Location: str
Interest held: str
Ownership details: str
Rental income: str
Rental income details: str


7. (i) Shareholdings: over 15% of issued share capital
Name of company or organisation: str
Nature of business: str



7. (ii) Other shareholdings, valued at more than £70,000
Name of company or organisation: str (Organisation model?)
Held jointly with or on behalf of: str
Nature of business: str
Interest held: str
Additional information: str


8. Miscellaneous
str
- Unpaid Directorship (at|of) str
Date interest arose: date
Date interest ended: date
Additional information: str


9. Family members employed and paid from parliamentary expenses
Additional information:
End date: date
Name: str
Relationship: str
Role: str
Working pattern: str


10. Family members engaged in lobbying the public sector on behalf of a third party or client
End date: date
Name of employer: str
Name: str
Relationship: str
Role: str


# Lords
Nil
str


1: Directorships
str


2: Remunerated employment, office, profession etc.
str


3: Person with significant control of a company (PSC)
str

4: Shareholdings (a)
str

4: Shareholdings (b)
str

4: Shareholdings (c)
str

5: Land and property
str

6: Sponsorship
str

7: Overseas visits
str

8: Gifts, benefits and hospitality
str

9: Miscellaneous financial interests
str

10: Non-financial interests (a)
str

10: Non-financial interests (b)
str

10: Non-financial interests (c)
str

10: Non-financial interests (d)
str

10: Non-financial interests (e)
str



"""
