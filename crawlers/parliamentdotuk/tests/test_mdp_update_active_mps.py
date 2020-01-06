"""

"""
import datetime
import logging
from unittest import mock

import requests

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.membersdataplatform import active_mps
from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import (
    HouseMembershipResponseData,
    ConstituencyResponseData,
    BasicInfoResponseData,
    CommitteeResponseData,
    InterestCategoryResponseData,
    PostResponseData,
    AddressResponseData,
    SpeechResponseData,
)
from repository.models import (
    House,
    HouseMembership,
    Person,
    ConstituencyResult,
    Constituency,
    Country,
    MaidenSpeech,
    Committee,
    Election,
    InterestCategory,
    Interest,
    OppositionPost,
    OppositionPostMember,
    ParliamentaryPost,
    ParliamentaryPostMember,
    PhysicalAddress,
    WebAddress,
)
from repository.models.committees import (
    CommitteeChair,
    CommitteeMember,
)
from repository.models.election import ContestedElection
from repository.models.geography import Town
from repository.models.houses import (
    HOUSE_OF_LORDS,
    HOUSE_OF_COMMONS,
)
from repository.tests import values

log = logging.getLogger(__name__)


# Sample data taken from a few members who happen to have fields that are
# populated in ways that are useful for testing. Some values may have been
# edited for the purpose of making them more useful for testing against.
# i.e. Do not consider this data to be accurate - it only matters that it is
# internally consistent.
SAMPLE_BIOGRAPHY_RESPONSE = {"Members":{"Member":{"@Member_Id":"965","@Dods_Id":"95847","@Pims_Id":"4680","@Clerks_Id":"","DisplayAs":"Lord Wrigglesworth","ListAs":"Wrigglesworth, L.","FullTitle":"The Lord Wrigglesworth","LayingMinisterName":None,"DateOfBirth":"1939-12-08T00:00:00","DateOfDeath":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Gender":"M","Party":{"@Id":"17","#text":"Liberal Democrat"},"House":"Lords","MemberFrom":"Life peer","HouseStartDate":"2013-09-05T00:00:00","HouseEndDate":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"CurrentStatus":{"@Id":"0","@IsActive":"True","Name":"Current Member","Reason":None,"StartDate":"2013-09-05T00:00:00"},"BasicDetails":{"GivenSurname":"Wrigglesworth","GivenMiddleNames":None,"GivenForename":"Ian","TownOfBirth":None,"CountryOfBirth":None,"Gender":"M","DateOfBirth":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"DateOfRetirement":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"DateOfDeath":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"LordsDetails":{"DateOfAnnouncement":"2013-08-01T00:00:00","DateOfIntroduction":"2013-10-10T00:00:00","DateOfWrit":"2013-09-05T00:00:00","MembershipTypes":{"MembershipType":{"Type":"Life peer","StartDate":"2013-09-05T00:00:00","EndDate":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}}},"Oaths":{"Oath":[{"Date":"2019-12-17T00:00:00"},{"Date":"2017-06-14T00:00:00"},{"Date":"2015-05-19T00:00:00"},{"Date":"2013-10-10T00:00:00"}]}}},"PreferredNames":{"PreferredName":[{"Title":None,"Surname":"Wrigglesworth","MiddleNames":"William","Forename":"Ian","Suffix":None,"AddressAs":None,"Note":None,"StartDate":"2013-09-05T00:00:00","EndDate":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"ListAs":"Wrigglesworth, L.","DisplayAs":"Lord Wrigglesworth","FullTitle":"The Lord Wrigglesworth","HonouraryPrefixes":None,"LordsName":{"Rank":"Lord","Title":"Wrigglesworth","Prenominal":"The","IsPrimaryTitle":"True","IsKnownAs":"False","IsByVirtue":"True","SitsByVirtue":None,"Cardinality":None,"UseOf":"False","UseThe":"False","OtherTitle":None,"IsOtherTitle":"False"}},{"Title":"Sir","Surname":"Wrigglesworth","MiddleNames":None,"Forename":"Ian","Suffix":None,"AddressAs":"Sir Ian","Note":None,"StartDate":"1939-12-08T00:00:00","EndDate":"2013-09-05T00:00:00","ListAs":"Wrigglesworth, Sir Ian","DisplayAs":"Sir Ian Wrigglesworth","FullTitle":"Sir Ian Wrigglesworth","HonouraryPrefixes":None}]},"HouseMemberships":{"HouseMembership":[{"House":"Lords","StartDate":"2013-09-05T00:00:00","EndDate":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"EndReason":None,"EndNotes":None},{"House":"Commons","StartDate":"1974-02-28T00:00:00","EndDate":"1987-06-11T00:00:00","EndReason":None,"EndNotes":None}]},"Constituencies":{"Constituency":[{"@Id":"2800","Name":"Stockton South","StartDate":"1983-06-09T00:00:00","EndDate":"1987-06-11T00:00:00","Election":{"@Id":"12","Name":"1983 General Election","Date":"1983-06-09T00:00:00","Type":"General Election"},"EndReason":"Defeated","EntryType":"Continuation","Notes":"","SwearInOrder":"0","SwornInForename":None,"SwornInMiddleNames":None,"SwornInSurname":None,"SwornInTitle":None},{"@Id":"2920","Name":"Thornaby","StartDate":"1979-05-03T00:00:00","EndDate":"1983-06-09T00:00:00","Election":{"@Id":"11","Name":"1979 General Election","Date":"1979-05-03T00:00:00","Type":"General Election"},"EndReason":"General Election","EntryType":"Continuation","Notes":None,"SwearInOrder":"0","SwornInForename":None,"SwornInMiddleNames":None,"SwornInSurname":None,"SwornInTitle":None},{"@Id":"2920","Name":"Thornaby","StartDate":"1974-10-10T00:00:00","EndDate":"1979-05-03T00:00:00","Election":{"@Id":"10","Name":"1974 (Oct) General Election","Date":"1974-10-10T00:00:00","Type":"General Election"},"EndReason":"General Election","EntryType":"Continuation","Notes":None,"SwearInOrder":"0","SwornInForename":None,"SwornInMiddleNames":None,"SwornInSurname":None,"SwornInTitle":None},{"@Id":"2920","Name":"Thornaby","StartDate":"1974-02-28T00:00:00","EndDate":"1974-10-10T00:00:00","Election":{"@Id":"9","Name":"1974 (Feb) General Election","Date":"1974-02-28T00:00:00","Type":"General Election"},"EndReason":"General Election","EntryType":"First entry","Notes":None,"SwearInOrder":"0","SwornInForename":None,"SwornInMiddleNames":None,"SwornInSurname":None,"SwornInTitle":None}]},"ElectionsContested":{"ElectionContested":{"Election":{"@Id":"13","Name":"1987 General Election","Date":"1987-06-11T00:00:00","Type":"General Election"},"Constituency":"Stockton South"}},"MaidenSpeeches":{"MaidenSpeech":[{"House":"Lords","SpeechDate":"2013-10-24T00:00:00","Hansard":None,"Subject":None},{"House":"Commons","SpeechDate":"1974-03-25T00:00:00","Hansard":"871 c77-9","Subject":None}]},"Committees":{"Committee":[{"@Id":"354","Name":"Trade Union Political Funds and Political Party Funding Committee","StartDate":"2016-01-28T00:00:00","EndDate":"2016-02-29T00:00:00","EndNote":None,"IsExOfficio":"False","IsAlternate":"False","IsCoOpted":"False","ChairDates":None},{"@Id":"230","Name":"Finance Bill Sub-Committee","StartDate":"2014-01-08T00:00:00","EndDate":"2014-03-11T00:00:00","EndNote":None,"IsExOfficio":"False","IsAlternate":"False","IsCoOpted":"False","ChairDates":None},{"@Id":"230","Name":"Finance Bill Sub-Committee","StartDate":"2017-01-10T00:00:00","EndDate":"2017-03-17T00:00:00","EndNote":None,"IsExOfficio":"False","IsAlternate":"False","IsCoOpted":"False","ChairDates":None},{"@Id":"67","Name":"European Legislation Sub-Committee II","StartDate":"1978-11-01T00:00:00","EndDate":"1979-04-04T00:00:00","EndNote":None,"IsExOfficio":"False","IsAlternate":"False","IsCoOpted":"False","ChairDates":None},{"@Id":"64","Name":"European Legislation","StartDate":"1978-11-01T00:00:00","EndDate":"1983-06-09T00:00:00","EndNote":None,"IsExOfficio":"False","IsAlternate":"False","IsCoOpted":"False","ChairDates":None}]},"GovernmentPosts":None,"OppositionPosts":None,"ParliamentaryPosts":{"ParliamentaryPost":{"@Id":"1098","Name":"Party Chair, Liberal Democrats","HansardName":"Party Chair, Liberal Democrats","StartDate":"1989-01-01T00:00:00","EndDate":"1990-12-31T00:00:00","Note":None,"EndNote":None,"IsJoint":"False","IsUnpaid":"False","Email":None,"LayingMinisterName":None}},"Statuses":{"Status":[{"@Id":"0","Name":"Current Member","StartDate":"2013-09-05T00:00:00","EndDate":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}},{"@Id":"0","Name":"Current Member","StartDate":"1974-02-28T00:00:00","EndDate":"1987-06-11T00:00:00"}]},"Parties":{"Party":[{"@Id":"17","Name":"Liberal Democrat","SubType":None,"StartDate":"1988-03-03T00:00:00","EndDate":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Note":None,"SitsOppositeSideToParty":"False"},{"@Id":"32","Name":"Social Democratic Party","SubType":None,"StartDate":"1981-03-02T00:00:00","EndDate":"2013-09-05T00:00:00","Note":None,"SitsOppositeSideToParty":"False"},{"@Id":"15","Name":"Labour","SubType":"Co-op","StartDate":"1974-02-28T00:00:00","EndDate":"1981-03-02T00:00:00","Note":None,"SitsOppositeSideToParty":"False"}]},"Honours":{"Honour":{"@Id":"31","Name":"Kt","HonourList":None,"StartDate":"1991-01-01T00:00:00","EndDate":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Note":None}},"OtherParliaments":None,"Interests":{"Category":[{"@Id":"1","@Name":"Category 1: Directorships","Interest":[{"@Id":"12485","@ParentId":"","@LastAmendment":"2013-12-02T16:54:20","@LastAmendmentType":"C","RegisteredInterest":"Director, Durham Group Estates Ltd","RegisteredLate":"False","Created":"2013-12-02T16:54:20","Amended":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Deleted":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}},{"@Id":"12486","@ParentId":"","@LastAmendment":"2013-12-02T16:54:36","@LastAmendmentType":"C","RegisteredInterest":"Director, Durham Group Investments Ltd","RegisteredLate":"False","Created":"2013-12-02T16:54:36","Amended":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Deleted":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}},{"@Id":"12487","@ParentId":"","@LastAmendment":"2013-12-02T16:55:00","@LastAmendmentType":"C","RegisteredInterest":"Director, Rudchester Estates Ltd (non-trading)","RegisteredLate":"False","Created":"2013-12-02T16:55:00","Amended":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Deleted":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}},{"@Id":"12488","@ParentId":"","@LastAmendment":"2013-12-02T16:55:33","@LastAmendmentType":"C","RegisteredInterest":"Director, Northern Corporate Finance Ltd (non-trading)","RegisteredLate":"False","Created":"2013-12-02T16:55:33","Amended":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Deleted":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}}]},{"@Id":"4","@Name":"Category 4: Shareholdings (a)","Interest":[{"@Id":"12489","@ParentId":"","@LastAmendment":"2013-12-02T16:56:24","@LastAmendmentType":"C","RegisteredInterest":"Durham Group Estates Ltd (commercial property company)","RegisteredLate":"False","Created":"2013-12-02T16:56:24","Amended":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Deleted":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}},{"@Id":"12490","@ParentId":"","@LastAmendment":"2013-12-02T16:56:49","@LastAmendmentType":"C","RegisteredInterest":"Durham Group Investments Ltd (commercial property company)","RegisteredLate":"False","Created":"2013-12-02T16:56:49","Amended":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Deleted":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}},{"@Id":"12491","@ParentId":"","@LastAmendment":"2013-12-02T16:57:08","@LastAmendmentType":"C","RegisteredInterest":"Rudchester Estates Ltd (non-trading)","RegisteredLate":"False","Created":"2013-12-02T16:57:08","Amended":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Deleted":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}},{"@Id":"12492","@ParentId":"","@LastAmendment":"2013-12-02T16:57:27","@LastAmendmentType":"C","RegisteredInterest":"Northern Corporate Finance Ltd (non-trading)","RegisteredLate":"False","Created":"2013-12-02T16:57:27","Amended":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Deleted":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}}]},{"@Id":"12","@Name":"Category 4: Shareholdings (b)","Interest":{"@Id":"24419","@ParentId":"","@LastAmendment":"2018-06-21T16:02:35","@LastAmendmentType":"U","RegisteredInterest":"Machine Delta (a division of Caspian Learning Ltd providing intelligent quality assurance using artificial intelligence)","RegisteredLate":"False","Created":"2015-12-31T21:08:44","Amended":"2018-06-21T16:02:35","Deleted":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}}}]},"Staffing":{"Staff":{"Title":"Ms","Surname":"Norris-Copson","MiddleNames":None,"Forename":"Sian","Note":"Office Manager, The Times, Parliamentary Press Gallery"}},"Addresses":{"Address":{"@Type_Id":"1","Type":"Parliamentary","IsPreferred":"False","IsPhysical":"True","Note":None,"Address1":"House of Lords","Address2":"London","Address3":None,"Address4":None,"Address5":None,"Postcode":"SW1A 0PW","Phone":"020 7219 8743","Fax":None,"Email":"wrigglesworthi@parliament.uk","OtherAddress":None}},"KnownAs":None,"BiographyEntries":{"BiographyEntry":[{"@Category_Id":"6","Category":"Concerns: Policy Interests","Entry":"Business, industry and consumers; Economy and finance; European Union; Parliament, government and politics; UK Regional Policy"},{"@Category_Id":"8","Category":"Concerns: World Areas","Entry":"India; Poland; South East Asia; Turkey; USA"},{"@Category_Id":"7","Category":"Concerns: UK Areas","Entry":"North East England"}]},"Experiences":{"Experience":[{"@Type_Id":"3","Type":"Political","Organisation":"Liberal Democrats","Title":"National Treasurer","StartDate":{"Day":None,"Month":None,"Year":"2012"},"EndDate":{"Day":None,"Month":None,"Year":"2015"}},{"@Type_Id":"2","Type":"Public life","Organisation":"Regional Growth Fund Advisory Board","Title":"Deputy Chairman","StartDate":{"Day":None,"Month":None,"Year":"2012"},"EndDate":{"Day":None,"Month":None,"Year":"2015"}},{"@Type_Id":"1","Type":"Non political","Organisation":"Port of Tyne","Title":"Chairman","StartDate":{"Day":None,"Month":None,"Year":"2005"},"EndDate":{"Day":None,"Month":None,"Year":"2012"}},{"@Type_Id":"2","Type":"Public life","Organisation":"Baltic Centre for Contemporary Art","Title":"Chairman","StartDate":{"Day":None,"Month":None,"Year":"2005"},"EndDate":{"Day":None,"Month":None,"Year":"2009"}},{"@Type_Id":"3","Type":"Political","Organisation":None,"Title":"Liberal Democrats Trustees","StartDate":{"Day":None,"Month":None,"Year":"2002"},"EndDate":{"Day":None,"Month":None,"Year":"2012"}},{"@Type_Id":"2","Type":"Public life","Organisation":"Tyne Tees Television","Title":"Director","StartDate":{"Day":None,"Month":None,"Year":"2002"},"EndDate":{"Day":None,"Month":None,"Year":"2005"}},{"@Type_Id":"2","Type":"Public life","Organisation":"Newcastle Gateshead Initiative","Title":"Chairman","StartDate":{"Day":None,"Month":None,"Year":"1999"},"EndDate":{"Day":None,"Month":None,"Year":"2004"}},{"@Type_Id":"1","Type":"Non political","Organisation":"Prima Europe and GPC","Title":"Chairman","StartDate":{"Day":None,"Month":None,"Year":"1996"},"EndDate":{"Day":None,"Month":None,"Year":"2000"}},{"@Type_Id":"1","Type":"Non political","Organisation":"UK Land Estates","Title":"Founding Chairman","StartDate":{"Day":None,"Month":None,"Year":"1995"},"EndDate":{"Day":None,"Month":None,"Year":"2009"}},{"@Type_Id":"2","Type":"Public life","Organisation":"Teeside University Board of Governors","Title":"Member & Deputy Chairman","StartDate":{"Day":None,"Month":None,"Year":"1993"},"EndDate":{"Day":None,"Month":None,"Year":"2002"}},{"@Type_Id":"3","Type":"Political","Organisation":"Liberal Democrats","Title":"President","StartDate":{"Day":None,"Month":None,"Year":"1988"},"EndDate":{"Day":None,"Month":None,"Year":"1990"}},{"@Type_Id":"1","Type":"Non political","Organisation":"John Lilvingston and Sons and Fairfield Industries","Title":"Deputy Chairman and Director","StartDate":{"Day":None,"Month":None,"Year":"1988"},"EndDate":{"Day":None,"Month":None,"Year":"1995"}}]}}}}
SAMPLE_BASIC_INFO = {"GivenSurname": "Abbott", "GivenMiddleNames": "Julie", "GivenForename": "Diane ", "TownOfBirth": "London", "CountryOfBirth": "England", "Gender": "F", "DateOfBirth": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "DateOfRetirement": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "DateOfDeath": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "LordsDetails": None}
SAMPLE_HISTORICAL_CONSTITUENCIES = [{"@Id": "2800", "Name": "Stockton South", "StartDate": "1983-06-09T00:00:00", "EndDate": "1987-06-11T00:00:00", "Election": {"@Id": "12", "Name": "1983 General Election", "Date": "1983-06-09T00:00:00", "Type": "General Election"}, "EndReason": "Defeated", "EntryType": "Continuation", "Notes": "", "SwearInOrder": "0", "SwornInForename": None, "SwornInMiddleNames": None, "SwornInSurname": None, "SwornInTitle": None}, {"@Id": "2920", "Name": "Thornaby", "StartDate": "1979-05-03T00:00:00", "EndDate": "1983-06-09T00:00:00", "Election": {"@Id": "11", "Name": "1979 General Election", "Date": "1979-05-03T00:00:00", "Type": "General Election"}, "EndReason": "General Election", "EntryType": "Continuation", "Notes": None, "SwearInOrder": "0", "SwornInForename": None, "SwornInMiddleNames": None, "SwornInSurname": None, "SwornInTitle": None}, {"@Id": "2920", "Name": "Thornaby", "StartDate": "1974-10-10T00:00:00", "EndDate": "1979-05-03T00:00:00", "Election": {"@Id": "10", "Name": "1974 (Oct) General Election", "Date": "1974-10-10T00:00:00", "Type": "General Election"}, "EndReason": "General Election", "EntryType": "Continuation", "Notes": None, "SwearInOrder": "0", "SwornInForename": None, "SwornInMiddleNames": None, "SwornInSurname": None, "SwornInTitle": None}, {"@Id": "2920", "Name": "Thornaby", "StartDate": "1974-02-28T00:00:00", "EndDate": "1974-10-10T00:00:00", "Election": {"@Id": "9", "Name": "1974 (Feb) General Election", "Date": "1974-02-28T00:00:00", "Type": "General Election"}, "EndReason": "General Election", "EntryType": "First entry", "Notes": None, "SwearInOrder": "0", "SwornInForename": None, "SwornInMiddleNames": None, "SwornInSurname": None, "SwornInTitle": None}]
SAMPLE_HOUSE_MEMBERSHIP = [{"House": "Lords", "StartDate": "2013-09-05T00:00:00", "EndDate": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "EndReason": None, "EndNotes": None}, {"House": "Commons", "StartDate": "1974-02-28T00:00:00", "EndDate": "1987-06-11T00:00:00", "EndReason": None, "EndNotes": None}]
SAMPLE_MAIDEN_SPEECHES = [{"House": "Lords", "SpeechDate": "2013-10-24T00:00:00", "Hansard": None, "Subject": None}, {"House": "Commons", "SpeechDate": "1974-03-25T00:00:00", "Hansard": "871 c77-9", "Subject": "Some subject"}]
SAMPLE_COMMITTEES = [{"@Id": "156", "Name": "Urban Affairs Sub-Committee", "StartDate": "2001-07-16T00:00:00", "EndDate": "2002-07-22T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "155", "Name": "Transport, Local Government & The Regions", "StartDate": "2001-07-16T00:00:00", "EndDate": "2002-07-22T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "61", "Name": "Transport Sub-committee", "StartDate": "2000-12-19T00:00:00", "EndDate": "2001-06-01T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "145", "Name": "Standards and Privileges ", "StartDate": "2010-07-26T00:00:00", "EndDate": "2013-01-07T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "126", "Name": "Procedure Committee", "StartDate": "1997-07-31T00:00:00", "EndDate": "2001-05-11T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "121", "Name": "Office of the Deputy Prime Minister: Housing, Planning, Local Government and the Regions Committee", "StartDate": "2002-07-22T00:00:00", "EndDate": "2005-07-11T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "121", "Name": "Office of the Deputy Prime Minister: Housing, Planning, Local Government and the Regions Committee", "StartDate": "2005-07-12T00:00:00", "EndDate": "2006-06-27T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "107", "Name": "Members Estimate", "StartDate": "2015-07-09T00:00:00", "EndDate": "2017-05-03T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "True", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "398", "Name": "Liaison Committee Sub-committee on the effectiveness and influence of the select committee system", "StartDate": "2019-02-13T00:00:00", "EndDate": "2019-11-06T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "True", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "103", "Name": "Liaison Committee (Commons)", "StartDate": "2015-09-10T00:00:00", "EndDate": "2017-05-03T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "True", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "103", "Name": "Liaison Committee (Commons)", "StartDate": "2017-11-06T00:00:00", "EndDate": "2019-11-06T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "True", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "17", "Name": "Housing, Communities and Local Government Committee", "StartDate": "2006-06-27T00:00:00", "EndDate": "2010-05-06T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "348", "Name": "House of Commons Commission", "StartDate": "2015-07-09T00:00:00", "EndDate": "2019-11-06T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "True", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "77", "Name": "Finance and Services Committee", "StartDate": "2010-07-26T00:00:00", "EndDate": "2015-03-30T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "59", "Name": "Environment, Transport & Regional Affairs", "StartDate": "2000-12-13T00:00:00", "EndDate": "2001-06-01T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "60", "Name": "Environment Sub-committee", "StartDate": "2000-12-13T00:00:00", "EndDate": "2001-06-01T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "42", "Name": "Education", "StartDate": "1992-04-27T00:00:00", "EndDate": "1994-10-27T00:00:00", "EndNote": None, "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "290", "Name": "Committee on Standards", "StartDate": "2013-01-07T00:00:00", "EndDate": "2015-03-30T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "290", "Name": "Committee on Standards", "StartDate": "2015-09-09T00:00:00", "EndDate": "2017-05-03T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "289", "Name": "Committee on Privileges", "StartDate": "2013-01-07T00:00:00", "EndDate": "2015-03-30T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "289", "Name": "Committee on Privileges", "StartDate": "2015-10-28T00:00:00", "EndDate": "2017-05-03T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": None}, {"@Id": "2", "Name": "Administration Committee", "StartDate": "2015-07-20T00:00:00", "EndDate": "2017-05-03T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": {"ChairDate": {"StartDate": "2015-07-21T00:00:00", "EndDate": "2017-05-03T00:00:00"}}}, {"@Id": "2", "Name": "Administration Committee", "StartDate": "2017-10-30T00:00:00", "EndDate": "2019-11-06T00:00:00", "EndNote": "Dissolution of Parliament", "IsExOfficio": "False", "IsAlternate": "False", "IsCoOpted": "False", "ChairDates": {"ChairDate": {"StartDate": "2017-11-06T00:00:00", "EndDate": "2019-11-06T00:00:00"}}}]
SAMPLE_GOVERNMENT_POSTS = []
SAMPLE_OPPOSITION_POSTS = [{"@Id": "1171", "Name": "Shadow Home Secretary", "HansardName": "Shadow Home Secretary", "StartDate": "2016-10-06T00:00:00", "EndDate": None, "Note": None, "EndNote": "Dissolution of Parliament", "IsJoint": "False", "IsUnpaid": "False", "Email": None}, {"@Id": "863", "Name": "Shadow Secretary of State for Health", "HansardName": "Shadow Secretary of State for Health", "StartDate": "2016-06-27T00:00:00", "EndDate": "2016-10-06T00:00:00", "Note": None, "EndNote": None, "IsJoint": "False", "IsUnpaid": "False", "Email": None}, {"@Id": "870", "Name": "Shadow Secretary of State for International Development", "HansardName": "Shadow Secretary of State for International Development", "StartDate": "2015-09-14T00:00:00", "EndDate": "2016-06-27T00:00:00", "Note": None, "EndNote": None, "IsJoint": "False", "IsUnpaid": "False", "Email": None}, {"@Id": "1003", "Name": "Shadow Minister (Public Health)", "HansardName": "Shadow Minister (Public Health)", "StartDate": "2010-10-08T00:00:00", "EndDate": "2013-10-07T00:00:00", "Note": None, "EndNote": None, "IsJoint": "False", "IsUnpaid": "False", "Email": None}]
SAMPLE_PARLIAMENTARY_POSTS = [{"@Id": "803", "Name": "Member, Labour Party National Executive Committee", "HansardName": None, "StartDate": "1994-01-01T00:00:00", "EndDate": "1997-01-01T00:00:00", "Note": None, "EndNote": None, "IsJoint": "False", "IsUnpaid": "False", "Email": None, "LayingMinisterName": None}]
SAMPLE_INTERESTS = [{"@Id": "1", "@Name": "Category 1: Directorships", "Interest": [{"@Id": "12485", "@ParentId": "", "@LastAmendment": "2013-12-02T16:54:20", "@LastAmendmentType": "C", "RegisteredInterest": "Director, Durham Group Estates Ltd", "RegisteredLate": "False", "Created": "2013-12-02T16:54:20", "Amended": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Deleted": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}, {"@Id": "12486", "@ParentId": "", "@LastAmendment": "2013-12-02T16:54:36", "@LastAmendmentType": "C", "RegisteredInterest": "Director, Durham Group Investments Ltd", "RegisteredLate": "False", "Created": "2013-12-02T16:54:36", "Amended": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Deleted": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}, {"@Id": "12487", "@ParentId": "", "@LastAmendment": "2013-12-02T16:55:00", "@LastAmendmentType": "C", "RegisteredInterest": "Director, Rudchester Estates Ltd (non-trading)", "RegisteredLate": "False", "Created": "2013-12-02T16:55:00", "Amended": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Deleted": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}, {"@Id": "12488", "@ParentId": "", "@LastAmendment": "2013-12-02T16:55:33", "@LastAmendmentType": "C", "RegisteredInterest": "Director, Northern Corporate Finance Ltd (non-trading)", "RegisteredLate": "False", "Created": "2013-12-02T16:55:33", "Amended": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Deleted": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}]}, {"@Id": "4", "@Name": "Category 4: Shareholdings (a)", "Interest": [{"@Id": "12489", "@ParentId": "", "@LastAmendment": "2013-12-02T16:56:24", "@LastAmendmentType": "C", "RegisteredInterest": "Durham Group Estates Ltd (commercial property company)", "RegisteredLate": "False", "Created": "2013-12-02T16:56:24", "Amended": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Deleted": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}, {"@Id": "12490", "@ParentId": "", "@LastAmendment": "2013-12-02T16:56:49", "@LastAmendmentType": "C", "RegisteredInterest": "Durham Group Investments Ltd (commercial property company)", "RegisteredLate": "False", "Created": "2013-12-02T16:56:49", "Amended": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Deleted": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}, {"@Id": "12491", "@ParentId": "", "@LastAmendment": "2013-12-02T16:57:08", "@LastAmendmentType": "C", "RegisteredInterest": "Rudchester Estates Ltd (non-trading)", "RegisteredLate": "False", "Created": "2013-12-02T16:57:08", "Amended": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Deleted": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}, {"@Id": "12492", "@ParentId": "", "@LastAmendment": "2013-12-02T16:57:27", "@LastAmendmentType": "C", "RegisteredInterest": "Northern Corporate Finance Ltd (non-trading)", "RegisteredLate": "False", "Created": "2013-12-02T16:57:27", "Amended": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Deleted": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}]}, {"@Id": "12", "@Name": "Category 4: Shareholdings (b)", "Interest": {"@Id": "24419", "@ParentId": "", "@LastAmendment": "2018-06-21T16:02:35", "@LastAmendmentType": "U", "RegisteredInterest": "Machine Delta (a division of Caspian Learning Ltd providing intelligent quality assurance using artificial intelligence)", "RegisteredLate": "False", "Created": "2015-12-31T21:08:44", "Amended": "2018-06-21T16:02:35", "Deleted": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}}]
SAMPLE_ADDRESSES = [{"@Type_Id": "6", "Type": "Website", "IsPreferred": "False", "IsPhysical": "False", "Note": None, "Address1": "http://www.molevalleyconservatives.org.uk/"}, {"@Type_Id": "4", "Type": "Constituency", "IsPreferred": "False", "IsPhysical": "True", "Note": None, "Address1": "Mole Valley Conservative Association", "Address2": "212 Barnett Wood Lane", "Address3": "Ashtead", "Address4": None, "Address5": None, "Postcode": "KT21 2DB", "Phone": "01306 883312", "Fax": None, "Email": "office@molevalleyconservatives.org.uk", "OtherAddress": None}, {"@Type_Id": "1", "Type": "Parliamentary", "IsPreferred": "False", "IsPhysical": "True", "Note": None, "Address1": "House of Commons", "Address2": None, "Address3": None, "Address4": None, "Address5": "London", "Postcode": "SW1A 0AA", "Phone": "020 7219 5018", "Fax": None, "Email": "annie.winsbury@parliament.uk", "OtherAddress": None}]
SAMPLE_BIOGRAPHY_ENTRIES = []
SAMPLE_EXPERIENCES = [{"@Type_Id": "3", "Type": "Political", "Organisation": "Liberal Democrats", "Title": "National Treasurer", "StartDate": {"Day": None, "Month": None, "Year": "2012"}, "EndDate": {"Day": None, "Month": None, "Year": "2015"}}, {"@Type_Id": "2", "Type": "Public life", "Organisation": "Regional Growth Fund Advisory Board", "Title": "Deputy Chairman", "StartDate": {"Day": None, "Month": None, "Year": "2012"}, "EndDate": {"Day": None, "Month": None, "Year": "2015"}}, {"@Type_Id": "1", "Type": "Non political", "Organisation": "Port of Tyne", "Title": "Chairman", "StartDate": {"Day": None, "Month": None, "Year": "2005"}, "EndDate": {"Day": None, "Month": None, "Year": "2012"}}, {"@Type_Id": "2", "Type": "Public life", "Organisation": "Baltic Centre for Contemporary Art", "Title": "Chairman", "StartDate": {"Day": None, "Month": None, "Year": "2005"}, "EndDate": {"Day": None, "Month": None, "Year": "2009"}}, {"@Type_Id": "3", "Type": "Political", "Organisation": None, "Title": "Liberal Democrats Trustees", "StartDate": {"Day": None, "Month": None, "Year": "2002"}, "EndDate": {"Day": None, "Month": None, "Year": "2012"}}, {"@Type_Id": "2", "Type": "Public life", "Organisation": "Tyne Tees Television", "Title": "Director", "StartDate": {"Day": None, "Month": None, "Year": "2002"}, "EndDate": {"Day": None, "Month": None, "Year": "2005"}}, {"@Type_Id": "2", "Type": "Public life", "Organisation": "Newcastle Gateshead Initiative", "Title": "Chairman", "StartDate": {"Day": None, "Month": None, "Year": "1999"}, "EndDate": {"Day": None, "Month": None, "Year": "2004"}}, {"@Type_Id": "1", "Type": "Non political", "Organisation": "Prima Europe and GPC", "Title": "Chairman", "StartDate": {"Day": None, "Month": None, "Year": "1996"}, "EndDate": {"Day": None, "Month": None, "Year": "2000"}}, {"@Type_Id": "1", "Type": "Non political", "Organisation": "UK Land Estates", "Title": "Founding Chairman", "StartDate": {"Day": None, "Month": None, "Year": "1995"}, "EndDate": {"Day": None, "Month": None, "Year": "2009"}}, {"@Type_Id": "2", "Type": "Public life", "Organisation": "Teeside University Board of Governors", "Title": "Member & Deputy Chairman", "StartDate": {"Day": None, "Month": None, "Year": "1993"}, "EndDate": {"Day": None, "Month": None, "Year": "2002"}}, {"@Type_Id": "3", "Type": "Political", "Organisation": "Liberal Democrats", "Title": "President", "StartDate": {"Day": None, "Month": None, "Year": "1988"}, "EndDate": {"Day": None, "Month": None, "Year": "1990"}}, {"@Type_Id": "1", "Type": "Non political", "Organisation": "John Lilvingston and Sons and Fairfield Industries", "Title": "Deputy Chairman and Director", "StartDate": {"Day": None, "Month": None, "Year": "1988"}, "EndDate": {"Day": None, "Month": None, "Year": "1995"}}]
SAMPLE_ELECTIONS_CONTESTED = [{"Election": {"@Id": "15", "Name": "1997 General Election", "Date": "1997-05-01T00:00:00", "Type": "General Election"}, "Constituency": "Clwyd South"}]


def get_mock_biography_response(*args, **kwargs):
    class MockJsonResponse:
        def __init__(self, url, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            print(f'MOCK RESPONSE: {url}')

        def json(self):
            return self.json_data

    return MockJsonResponse(args[0], SAMPLE_BIOGRAPHY_RESPONSE, 200)


class MdpUpdateActiveMpsTest(LocalTestCase):
    def setUp(self) -> None:
        commons, _ = House.objects.update_or_create(name=HOUSE_OF_COMMONS)
        House.objects.update_or_create(name=HOUSE_OF_LORDS)
        self.person = Person.objects.create(
            parliamentdotuk=965,  # ID for Lord Wrigglesworth, used in SAMPLE_BIOGRAPHY_RESPONSE
            name=values.EXAMPLE_NAME,
            active=True,
            house=commons,
        )
        self.person.save()

    def test__update_house_membership(self):
        house_memberships = [HouseMembershipResponseData(hm) for hm in SAMPLE_HOUSE_MEMBERSHIP]

        active_mps._update_house_membership(self.person, house_memberships)

        lords_membership = HouseMembership.objects.get(person=self.person, house=House.objects.get(name=HOUSE_OF_LORDS))
        self.assertEqual(lords_membership.start, datetime.date(year=2013, month=9, day=5))
        self.assertIsNone(lords_membership.end)

        commons_membership = HouseMembership.objects.get(person=self.person, house=House.objects.get(name=HOUSE_OF_COMMONS))
        self.assertEqual(commons_membership.start, datetime.date(year=1974, month=2, day=28))
        self.assertEqual(commons_membership.end, datetime.date(year=1987, month=6, day=11))

    def test__update_historical_constituencies(self):
        historical_constituencies = [ConstituencyResponseData(c) for c in SAMPLE_HISTORICAL_CONSTITUENCIES]

        active_mps._update_historical_constituencies(self.person, historical_constituencies)

        stockton_south = Constituency.objects.get(parliamentdotuk=2800)
        result = ConstituencyResult.objects.get(
            constituency=stockton_south,
            start=datetime.date(year=1983, month=6, day=9)
        )
        self.assertEqual(result.election.name, '1983 General Election')
        self.assertEqual(result.election.date, datetime.date(year=1983, month=6, day=9))
        self.assertEqual(result.end, datetime.date(year=1987, month=6, day=11))

        self.assertEqual(
            len(ConstituencyResult.objects.filter(
                constituency__name='Thornaby'
            )),
            3)

    def test__update_basic_details(self):
        basic_info = BasicInfoResponseData(SAMPLE_BASIC_INFO)
        active_mps._update_basic_details(self.person, basic_info)

        self.assertEqualIgnoreCase(self.person.additional_name, 'Julie')
        self.assertEqualIgnoreCase(self.person.given_name, 'Diane')
        self.assertEqualIgnoreCase(self.person.family_name, 'Abbott')
        self.assertEqualIgnoreCase(self.person.town_of_birth.name, 'London')
        self.assertEqualIgnoreCase(self.person.country_of_birth.name, 'England')

    def test__update_committees(self):
        committees = [CommitteeResponseData(c) for c in SAMPLE_COMMITTEES]
        active_mps._update_committees(self.person, committees)

        self.assertEqual(len(Committee.objects.all()), 18)
        self.assertEqual(
            len(CommitteeMember.objects.filter(person=self.person)),
            23)
        self.assertEqual(
            len(CommitteeChair.objects.filter(member__person=self.person)),
            2)

        admin_committee = Committee.objects.get(parliamentdotuk=2)
        admin_committee_chair = CommitteeChair.objects.get(
            member__committee=admin_committee,
            start=datetime.date(year=2017, month=11, day=6)
        )
        self.assertEqual(admin_committee_chair.end, datetime.date(year=2019, month=11, day=6))

    def test__update_interests(self):
        interest_categories = [InterestCategoryResponseData(c) for c in SAMPLE_INTERESTS]
        active_mps._update_interests(self.person, interest_categories)

        self.assertLengthEquals(InterestCategory.objects.all(), 3)

        directorships = InterestCategory.objects.get(parliamentdotuk=1)
        self.assertLengthEquals(Interest.objects.filter(category=directorships), 4)

        durham_group_estates = Interest.objects.get(parliamentdotuk=12485)
        self.assertEqual(durham_group_estates.person, self.person)
        self.assertEqual(durham_group_estates.description, 'Director, Durham Group Estates Ltd')
        self.assertEqual(durham_group_estates.created, datetime.date(year=2013, month=12, day=2))
        self.assertFalse(durham_group_estates.registered_late)
        self.assertIsNone(durham_group_estates.amended)
        self.assertIsNone(durham_group_estates.deleted)

        machine_delta = Interest.objects.get(parliamentdotuk=24419)
        self.assertEqual(machine_delta.description, 'Machine Delta (a division of Caspian Learning Ltd providing intelligent quality assurance using artificial intelligence)')
        self.assertEqual(machine_delta.created, datetime.date(year=2015, month=12, day=31))
        self.assertEqual(machine_delta.amended, datetime.date(year=2018, month=6, day=21))

    def test__update_opposition_posts(self):
        opposition_posts = [PostResponseData(p) for p in SAMPLE_OPPOSITION_POSTS]
        active_mps._update_opposition_posts(self.person, opposition_posts)

        self.assertLengthEquals(OppositionPost.objects.all(), 4)
        self.assertLengthEquals(OppositionPostMember.objects.filter(person=self.person), 4)

        shadow_home_secretary = OppositionPost.objects.get(parliamentdotuk=1171)
        self.assertEqual(shadow_home_secretary.name, 'Shadow Home Secretary')
        self.assertEqual(shadow_home_secretary.hansard_name, 'Shadow Home Secretary')

        membership = OppositionPostMember.objects.get(post=shadow_home_secretary)
        self.assertEqual(membership.person, self.person)
        self.assertEqual(membership.start, datetime.date(year=2016, month=10, day=6))
        self.assertIsNone(membership.end)

    def test__update_parliamentary_posts(self):
        parliamentary_posts = [PostResponseData(p) for p in SAMPLE_PARLIAMENTARY_POSTS]
        active_mps._update_parliamentary_posts(self.person, parliamentary_posts)

        self.assertLengthEquals(ParliamentaryPost.objects.all(), 1)
        self.assertLengthEquals(ParliamentaryPostMember.objects.filter(person=self.person), 1)

        labour_nec = ParliamentaryPost.objects.get(parliamentdotuk=803)
        self.assertEqual(labour_nec.name, 'Member, Labour Party National Executive Committee')
        self.assertIsNone(labour_nec.hansard_name)

        member = ParliamentaryPostMember.objects.get(post=labour_nec)
        self.assertEqual(member.person, self.person)
        self.assertEqual(member.start, datetime.date(year=1994, month=1, day=1))
        self.assertEqual(member.end, datetime.date(year=1997, month=1, day=1))

    def test__update_addresses(self):
        addresses = [AddressResponseData(a) for a in SAMPLE_ADDRESSES]
        active_mps._update_addresses(self.person, addresses)

        self.assertLengthEquals(PhysicalAddress.objects.all(), 2)
        self.assertLengthEquals(WebAddress.objects.all(), 1)

        parliamentary_address = PhysicalAddress.objects.get(postcode='SW1A 0AA')
        self.assertEqual(
            parliamentary_address.address,
            'House of Commons, London'
        )
        self.assertEqual(parliamentary_address.description, 'Parliamentary')
        self.assertEqual(parliamentary_address.phone.as_national, '020 7219 5018')
        self.assertIsNone(parliamentary_address.fax)
        self.assertEqual(parliamentary_address.email, 'annie.winsbury@parliament.uk')

        constituency_address = PhysicalAddress.objects.get(postcode='KT21 2DB')
        self.assertEqual(constituency_address.description, 'Constituency')
        self.assertEqual(
            constituency_address.address,
            'Mole Valley Conservative Association, 212 Barnett Wood Lane, Ashtead'
        )
        self.assertEqual(constituency_address.email, 'office@molevalleyconservatives.org.uk')
        self.assertEqual(constituency_address.phone.as_national, '01306 883312')

        website = WebAddress.objects.get(description='Website')
        self.assertEqual(website.url, "http://www.molevalleyconservatives.org.uk/")

    def test__update_maiden_speeches(self):
        speeches = [SpeechResponseData(s) for s in SAMPLE_MAIDEN_SPEECHES]
        active_mps._update_maiden_speeches(self.person, speeches)

        lords = MaidenSpeech.objects.get(house__name='Lords')
        self.assertEqual(lords.date, datetime.date(year=2013, month=10, day=24))
        self.assertIsNone(lords.hansard)
        self.assertIsNone(lords.subject)

        commons = MaidenSpeech.objects.get(house__name='Commons')
        self.assertEqual(commons.date, datetime.date(year=1974, month=3, day=25))
        self.assertEqual(commons.hansard, '871 c77-9')
        self.assertEqual(commons.subject, 'Some subject')

    def test__update_party_associations(self):
        # TODO
        raise NotImplementedError()

    def test__update_government_posts(self):
        # TODO
        raise NotImplementedError()

    def test__update_biography_entries(self):
        # TODO
        raise NotImplementedError()

    def test__update_experiences(self):
        # TODO
        raise NotImplementedError()

    @mock.patch.object(
        requests, 'get',
        mock.Mock(side_effect=get_mock_biography_response),
    )
    def test_update_active_mps_details(self):
        puk = 965

        active_mps.update_active_mps_details()

        person = Person.objects.get(parliamentdotuk=puk)

        self.assertEqualIgnoreCase(person.given_name, 'Ian')
        self.assertEqualIgnoreCase(person.family_name, 'Wrigglesworth')
        self.assertIsNone(person.town_of_birth)
        self.assertIsNone(person.country_of_birth)

        memberships = HouseMembership.objects.filter(person__parliamentdotuk=puk)
        self.assertLengthEquals(memberships, 2)

        constituencies = ConstituencyResult.objects.filter(mp__parliamentdotuk=puk)
        self.assertLengthEquals(constituencies, 4)

    def tearDown(self) -> None:
        self.delete_instances_of(
            Person,
            House,
            HouseMembership,
            Town,
            Country,
            MaidenSpeech,
            Committee,
            CommitteeChair,
            CommitteeMember,
            Election,
            ContestedElection,
        )
