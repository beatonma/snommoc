from dataclasses import dataclass

from repository.tests.data.sample import any_sample_of


@dataclass
class SampleBillStageType:
    id: int
    name: str
    house: str


@dataclass
class SampleBillType:
    id: int
    category: str
    name: str
    description: str


def any_sample_bill_stage_type() -> SampleBillStageType:
    return any_sample_of(SAMPLE_BILL_STAGE_TYPES)


def any_sample_bill_type() -> SampleBillType:
    return any_sample_of(SAMPLE_BILL_TYPES)


SAMPLE_BILL_STAGE_TYPES = [
    SampleBillStageType(6, "1st reading", "Commons"),
    SampleBillStageType(7, "2nd reading", "Commons"),
    SampleBillStageType(28, "Guillotine motion", "Commons"),
    SampleBillStageType(44, "Second House Examination", "Commons"),
    SampleBillStageType(25, "Second reading committee", "Commons"),
    SampleBillStageType(14, "Programme motion", "Commons"),
    SampleBillStageType(15, "Money resolution", "Commons"),
    SampleBillStageType(29, "Allocation of time motion", "Commons"),
    SampleBillStageType(26, "Order of Commitment discharged", "Commons"),
    SampleBillStageType(8, "Committee stage", "Commons"),
    SampleBillStageType(43, "Select Committee stage", "Commons"),
    SampleBillStageType(36, "Ways and Means resolution", "Commons"),
    SampleBillStageType(9, "Report stage", "Commons"),
    SampleBillStageType(10, "3rd reading", "Commons"),
    SampleBillStageType(38, "Legislative Grand Committee", "Commons"),
    SampleBillStageType(39, "Reconsideration", "Commons"),
    SampleBillStageType(12, "Consideration of Lords amendments", "Commons"),
    SampleBillStageType(40, "Consequential consideration", "Commons"),
    SampleBillStageType(18, "Carry-over motion", "Commons"),
    SampleBillStageType(42, "Consideration of Lords message", "Commons"),
]

SAMPLE_BILL_TYPES = [
    SampleBillType(
        4,
        "Hybrid",
        "Hybrid Bill",
        "Hybrid Bills mix the characteristics of Public and Private Bills. The changes"
        " to the law proposed by a Hybrid Bill would affect the general public but"
        " would also have a significant impact for specific individuals or groups."
        " <div><a href='https://www.parliament.uk/about/how/laws/bills/hybrid/'>Find"
        " out more about Hybrid Bills</a></div>",
    ),
    SampleBillType(
        6,
        "Private",
        "Private Bill",
        "Private bills are bills for the particular interest or benefit of any person"
        " or persons, public company or corporation, or local authority, and thus are"
        " applicable to, or have a differentiated effect on, only a particular section"
        " of the population. Private bills are promoted by the interested parties"
        " themselves.<div><a"
        " href='https://www.parliament.uk/about/how/laws/bills/private/'>Find out more"
        " about Private bills</a></div>",
    ),
    SampleBillType(
        9,
        "Public",
        "Draft Bill",
        "A Draft Bill is published to enable consultation and pre-legislative scrutiny."
        " After consultation and pre-legislative scrutiny has taken place, the Draft"
        " Bill may be introduced formally in the House of Commons or the House of"
        " Lords.<div><a"
        " href='https://www.parliament.uk/business/bills-and-legislation/draft-bills/'>Find"
        " out more about Draft Bills</a></div>",
    ),
]
