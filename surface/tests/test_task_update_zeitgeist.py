from basetest.test_util import create_sample_dates
from basetest.testcase import LocalTestCase
from repository.models import (
    Bill,
    Person,
)
from repository.tests.data.create import create_sample_person
from social.models import (
    Comment,
    Vote,
    VoteType,
)
from social.models.token import UserToken
from social.tests.util import (
    create_sample_comment,
    create_sample_usertoken,
    create_sample_vote,
)
from surface.models import (
    FeaturedPerson,
    ZeitgeistItem,
)
from surface.tasks import update_zeitgeist


def _create_featured_person(person: Person):
    return FeaturedPerson.objects.create(target=person)


class UpdateZeitgeistTaskTest(LocalTestCase):
    """"""

    def setUp(self):
        dates = create_sample_dates(count=10)

        user1 = create_sample_usertoken()
        user2 = create_sample_usertoken()

        boris = create_sample_person(11, "Boris Johnson")
        keir = create_sample_person(23, "Keir Starmer")
        anna = create_sample_person(37, "Anna McMorrin")

        create_sample_vote(boris, user1, "aye", created_on=dates[0])
        create_sample_vote(keir, user1, "no", created_on=dates[1])
        create_sample_vote(boris, user2, "no", created_on=dates[2])
        create_sample_vote(keir, user2, "aye", created_on=dates[3])

        create_sample_comment(boris, user1, created_on=dates[4])
        create_sample_comment(keir, user2, created_on=dates[5])
        create_sample_comment(keir, user1, created_on=dates[6])

        _create_featured_person(anna)

    def test_zeitgeist_is_correct(self):
        update_zeitgeist()

        zeitgeist = ZeitgeistItem.objects.all()
        self.assertEqual(zeitgeist.count(), 3)

        anna = zeitgeist.get(target_id=37)
        self.assertEqual(anna.reason, ZeitgeistItem.REASON_FEATURE)
        self.assertEqual(anna.target.name, "Anna McMorrin")

        boris = zeitgeist.get(target_id=11)
        self.assertEqual(boris.reason, ZeitgeistItem.REASON_SOCIAL)
        self.assertEqual(boris.target.name, "Boris Johnson")

    def tearDown(self) -> None:
        self.delete_instances_of(
            Bill,
            Comment,
            Comment,
            FeaturedPerson,
            Person,
            UserToken,
            Vote,
            VoteType,
            ZeitgeistItem,
        )
