from dataclasses import dataclass
from typing import List, Optional


class DivisionSchema:
    """
    Schema definition: DivisionViewModel from https://lordsvotes-api.parliament.uk/index.html
    """

    def __init__(
        self,
        divisionId: int,
        date: str,
        number: int,
        notes: Optional[str],
        title: Optional[str],
        isWhipped: bool,
        isGovernmentContent: bool,
        authoritativeContentCount: int,
        authoritativeNotContentCount: int,
        divisionHadTellers: bool,
        tellerContentCount: int,
        tellerNotContentCount: int,
        memberContentCount: int,
        memberNotContentCount: int,
        sponsoringMemberId: Optional[int],
        isHouse: Optional[bool],
        amendmentMotionNotes: Optional[str],
        isGovernmentWin: Optional[bool],
        remoteVotingStart: Optional[str],
        remoteVotingEnd: Optional[str],
        divisionWasExclusivelyRemote: bool,
        contentTellers: Optional[List["DivisionMemberSchema"]],
        notContentTellers: Optional[List["DivisionMemberSchema"]],
        contents: Optional[List["DivisionMemberSchema"]],
        notContents: Optional[List["DivisionMemberSchema"]],
    ):
        """
        :param divisionId:
        :param date:
        :param number:
        :param notes:
        :param title:
        :param isWhipped:
        :param isGovernmentContent:
        :param authoritativeContentCount: Authoritative content count is the official count.
                                          This is the teller content count when tellers are present,
                                          but member content count when there are no tellers.
        :param authoritativeNotContentCount: Authoritative not content count is the official count.
                                          This is the teller not content count when tellers are present,
                                          but member not content count when there are no tellers.
        :param divisionHadTellers: Whether the division had tellers or not
        :param tellerContentCount: Content count is count recorded by the tellers
        :param tellerNotContentCount: Not Content count recorded by the tellers
        :param memberContentCount: Member content count is the total tally of all members that voted content
        :param memberNotContentCount: Member not content count is the total tally of all members that voted not content
        :param sponsoringMemberId:
        :param isHouse:
        :param amendmentMotionNotes:
        :param isGovernmentWin:
        :param remoteVotingStart:
        :param remoteVotingEnd:
        :param divisionWasExclusivelyRemote:
        :param contentTellers:
        :param notContentTellers:
        :param contents:
        :param notContents:
        """
        self.divisionId = divisionId
        self.date = date
        self.number = number
        self.notes = notes
        self.title = title
        self.isWhipped = isWhipped
        self.isGovernmentContent = isGovernmentContent
        self.authoritativeContentCount = authoritativeContentCount
        self.authoritativeNotContentCount = authoritativeNotContentCount
        self.divisionHadTellers = divisionHadTellers
        self.tellerContentCount = tellerContentCount
        self.tellerNotContentCount = tellerNotContentCount
        self.memberContentCount = memberContentCount
        self.memberNotContentCount = memberNotContentCount
        self.sponsoringMemberId = sponsoringMemberId
        self.isHouse = isHouse
        self.amendmentMotionNotes = amendmentMotionNotes
        self.isGovernmentWin = isGovernmentWin
        self.remoteVotingStart = remoteVotingStart
        self.remoteVotingEnd = remoteVotingEnd
        self.divisionWasExclusivelyRemote = divisionWasExclusivelyRemote

        self.contentTellers = [DivisionMemberSchema(**x) for x in contentTellers]
        self.notContentTellers = [DivisionMemberSchema(**x) for x in notContentTellers]
        self.contents = [DivisionMemberSchema(**x) for x in contents]
        self.notContents = [DivisionMemberSchema(**x) for x in notContents]


@dataclass
class DivisionMemberSchema:
    """
    Schema definition: MemberViewModel from https://lordsvotes-api.parliament.uk/index.html
    """

    memberId: int
    name: Optional[str]

    """
    Sortable name
    """
    listAs: Optional[str]

    """
    Type of Lord e.g. 'Life peer', 'Bishops'
    """
    memberFrom: Optional[str]
    party: Optional[str]
    partyColour: Optional[str]
    partyAbbreviation: Optional[str]
    partyIsMainParty: bool
