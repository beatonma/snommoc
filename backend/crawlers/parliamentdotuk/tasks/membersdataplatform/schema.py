from crawlers.parliamentdotuk.tasks.types import (
    CoercedBool,
    CoercedDate,
    CoercedList,
    CoercedPhoneNumber,
    CoercedStr,
    field,
)
from pydantic import BaseModel as Schema
from pydantic import model_validator


class Party(Schema):
    parliamentdotuk: int = field("@Id")
    name: CoercedStr = field("#text")


class Member(Schema):
    parliamentdotuk: int = field("@Member_Id")
    name: CoercedStr = field("DisplayAs")
    full_title: CoercedStr = field("FullTitle")
    gender: CoercedStr = field("Gender")
    constituency_name: CoercedStr = field("MemberFrom")  # Commons only
    lords_type: CoercedStr = field("MemberFrom")  # Lords only
    date_of_birth: CoercedDate = field("DateOfBirth")
    date_of_death: CoercedDate = field("DateOfDeath")
    house: CoercedStr = field("House")
    house_start_date: CoercedDate = field("HouseStartDate")
    house_end_date: CoercedDate = field("HouseEndDate")
    party: Party | None = field("Party")
    is_active: CoercedBool = field("CurrentStatus.@IsActive")


class BasicInfo(Schema):
    family_name: CoercedStr = field("GivenSurname")
    first_name: CoercedStr = field("GivenForename")
    middle_names: CoercedStr = field("GivenMiddleNames")
    town_of_birth: CoercedStr = field("TownOfBirth")
    country_of_birth: CoercedStr = field("CountryOfBirth")


class HouseMembership(Schema):
    house: CoercedStr = field("House")
    start_date: CoercedDate = field("StartDate")
    end_date: CoercedDate = field("EndDate")


class Election(Schema):
    parliamentdotuk: int = field("@Id")
    name: CoercedStr = field("Name")
    date: CoercedDate = field("Date")
    type: CoercedStr = field("Type")


class Constituency(Schema):
    parliamentdotuk: int = field("@Id")
    name: CoercedStr = field("Name")
    start_date: CoercedDate = field("StartDate")
    end_date: CoercedDate = field("EndDate")
    election: Election | None = field("Election")


class PartyMembership(Schema):
    parliamentdotuk: int = field("@Id")
    name: CoercedStr = field("Name")
    start_date: CoercedDate = field("StartDate")
    end_date: CoercedDate = field("EndDate")


class CommitteeChair(Schema):
    start_date: CoercedDate = field("StartDate")
    end_date: CoercedDate = field("EndDate")


class Committee(Schema):
    parliamentdotuk: int = field("@Id")
    name: CoercedStr = field("Name")
    start_date: CoercedDate = field("StartDate")
    end_date: CoercedDate = field("EndDate")
    chair: CoercedList[CommitteeChair] = field("ChairDates.ChairDate")


class MaidenSpeech(Schema):
    house: CoercedStr = field("House")
    date: CoercedDate = field("SpeechDate")
    subject: CoercedStr = field("Subject")
    hansard: CoercedStr = field("Hansard")


class Post(Schema):
    parliamentdotuk: int = field("@Id")
    name: CoercedStr = field("Name")
    hansard_name: CoercedStr = field("HansardName")
    start_date: CoercedDate = field("StartDate")
    end_date: CoercedDate = field("EndDate")


class Address(Schema):
    type: CoercedStr = field("Type")
    is_physical: CoercedBool = field("IsPhysical")
    address: CoercedStr  # see validate_address
    postcode: CoercedStr = field("Postcode", default=None)
    phone: CoercedPhoneNumber = field("Phone", default=None)
    fax: CoercedPhoneNumber = field("Fax", default=None)
    email: CoercedStr = field("Email", default=None)

    @model_validator(mode="before")
    def validate_address(cls, obj):
        """Combine address fields into single string."""
        address_lines = [
            obj.get(key)
            for key in [
                "Address1",
                "Address2",
                "Address3",
                "Address4",
                "Address5",
            ]
        ]
        address = ", ".join(x for x in address_lines if x)

        obj["address"] = address or None
        return obj


class SubjectOfInterest(Schema):
    category: CoercedStr = field("Category")
    entry: CoercedStr = field("Entry")


class _Interest(Schema):
    parliamentdotuk: int | None = field("@Id")
    title: CoercedStr = field("RegisteredInterest")
    is_registered_late: CoercedBool = field("RegisteredLate")
    date_created: CoercedDate = field("Created")
    date_amended: CoercedDate = field("Amended")
    date_deleted: CoercedDate = field("Deleted")


class DeclaredInterest(Schema):
    category_id: int = field("@Id")
    category_name: CoercedStr = field("@Name")
    interests: CoercedList[_Interest] = field("Interest")


class Experience(Schema):
    type: CoercedStr = field("Type")
    organisation: CoercedStr = field("Organisation")
    title: CoercedStr = field("Title")
    start_date: CoercedDate = field("StartDate")
    end_date: CoercedDate = field("EndDate")


class ContestedElection(Schema):
    election: Election = field("Election")
    constituency_name: CoercedStr = field("Constituency")


class MemberFullBiog(Member):
    basic_info: BasicInfo = field("BasicDetails")
    house_memberships: CoercedList[HouseMembership] = field(
        "HouseMemberships.HouseMembership"
    )
    constituencies: CoercedList[Constituency] = field("Constituencies.Constituency")
    parties: CoercedList[PartyMembership] = field("Parties.Party")
    committees: CoercedList[Committee] = field("Committees.Committee")
    maiden_speeches: CoercedList[MaidenSpeech] = field("MaidenSpeeches.MaidenSpeech")
    government_posts: CoercedList[Post] = field("GovernmentPosts.GovernmentPost")
    parliament_posts: CoercedList[Post] = field("ParliamentaryPosts.ParliamentaryPost")
    opposition_posts: CoercedList[Post] = field("OppositionPosts.OppositionPost")
    addresses: CoercedList[Address] = field("Addresses.Address")
    subjects: CoercedList[SubjectOfInterest] = field("BiographyEntries.BiographyEntry")
    declared_interests: CoercedList[DeclaredInterest] = field("Interests.Category")
    experiences: CoercedList[Experience] = field("Experiences.Experience")
    contested_elections: CoercedList[ContestedElection] = field(
        "ElectionsContested.ElectionContested"
    )


class MemberResponse(Schema):
    """An individual member biography"""

    member: MemberFullBiog = field("Members.Member")


class MemberListResponse(Schema):
    """A list of members."""

    members: CoercedList[Member] = field("Members.Member")
