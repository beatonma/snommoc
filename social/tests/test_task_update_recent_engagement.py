"""

"""

import logging

from basetest.test_util import create_sample_dates
from basetest.testcase import LocalTestCase
from repository.models import (
    Bill,
    CommonsDivision,
    LordsDivision,
    Person,
)
from repository.tests.util import create_sample_person
from social.models import (
    Comment,
    Vote,
)
from social.models.engagement import (
    RecentBillEngagement,
    RecentCommonsDivisionEngagement,
    RecentLordsDivisionEngagement,
    RecentPersonEngagement,
)
from social.tasks.update_recent_engagement import update_recent_engagement
from social.tests.util import (
    create_sample_comment,
    create_sample_usertoken,
    create_sample_vote,
)

log = logging.getLogger(__name__)


class UpdateRecentEngagementTaskTest(LocalTestCase):
    def setUp(self) -> None:
        dates = create_sample_dates(count=10)

        user1 = create_sample_usertoken()
        user2 = create_sample_usertoken()

        boris = create_sample_person(11, 'Boris Johnson')
        keir = create_sample_person(23, 'Keir Starmer')

        create_sample_vote(boris, user1, 'aye', created_on=dates[0])
        create_sample_vote(keir, user1, 'no', created_on=dates[1])
        create_sample_vote(boris, user2, 'no', created_on=dates[2])
        create_sample_vote(keir, user2, 'aye', created_on=dates[3])

        create_sample_comment(boris, user1, created_on=dates[4])
        create_sample_comment(keir, user2, created_on=dates[5])
        create_sample_comment(keir, user1, created_on=dates[6])

    def test_recent_person_engagement(self):
        update_recent_engagement()

        recent = RecentPersonEngagement.objects.all()
        self.assertEqual(recent.count(), 7)
        self.assertEqual(recent.filter(person_id=23).count(), 4)
        self.assertEqual(recent.filter(person_id=11).count(), 3)

        self.assertEqual(recent.order_by('-created_on').first().person_id, 23)

    def tearDown(self) -> None:
        self.delete_instances_of(
            Vote,
            Comment,
            Person,
            CommonsDivision,
            LordsDivision,
            Bill,
            RecentPersonEngagement,
            RecentCommonsDivisionEngagement,
            RecentLordsDivisionEngagement,
            RecentBillEngagement,
        )
