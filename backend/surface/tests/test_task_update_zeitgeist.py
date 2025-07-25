from basetest.test_util import create_sample_dates
from basetest.testcase import DatabaseTestCase
from repository.models import Person
from repository.tests.data.create import (
    create_sample_bill,
    create_sample_commons_division,
    create_sample_lords_division,
    create_sample_person,
)
from social.tests.util import (
    create_sample_comment,
    create_sample_usertoken,
    create_sample_vote,
)
from surface.models import FeaturedPerson, ZeitgeistItem
from surface.tasks import update_zeitgeist


def _create_featured_person(person: Person):
    return FeaturedPerson.objects.create(target=person)


class UpdateZeitgeistTaskTest(DatabaseTestCase):
    def setUp(self):
        dates = create_sample_dates(count=10)

        user1 = create_sample_usertoken()
        user2 = create_sample_usertoken()

        boris = create_sample_person(11, "Boris Johnson")
        keir = create_sample_person(23, "Keir Starmer")
        anna = create_sample_person(37, "Anna McMorrin")

        create_sample_vote(boris, user1, "aye", created_at=dates[0])
        create_sample_vote(keir, user1, "no", created_at=dates[1])
        create_sample_vote(boris, user2, "no", created_at=dates[2])
        create_sample_vote(keir, user2, "aye", created_at=dates[3])

        create_sample_comment(boris, user1, created_at=dates[4])
        create_sample_comment(keir, user2, created_at=dates[5])
        create_sample_comment(keir, user1, created_at=dates[6])

        _create_featured_person(anna)

        bill = create_sample_bill(175, title="A voted-on bill title")
        create_sample_vote(bill, user1, "aye")

        commons_div = create_sample_commons_division(
            pk=984, title="A commented-on commons division"
        )
        create_sample_comment(commons_div, user2)

        lords_div = create_sample_lords_division(
            pk=840, title="A voted-on lords division"
        )
        create_sample_vote(lords_div, user2, "no")

    def test_zeitgeist_is_correct(self):
        update_zeitgeist()

        zeitgeist = ZeitgeistItem.objects.all()

        # 6 items =  3 people + 1 bill + 1 commons division + 1 lords division
        self.assertEqual(zeitgeist.count(), 6)

        anna = zeitgeist.get(target_id=37)
        self.assertEqual(anna.reason, ZeitgeistItem.Reason.FEATURE)
        self.assertEqual(anna.target.name, "Anna McMorrin")

        boris = zeitgeist.get(target_id=11)
        self.assertEqual(boris.reason, ZeitgeistItem.Reason.SOCIAL)
        self.assertEqual(boris.target.name, "Boris Johnson")

        bill = zeitgeist.get(target_id=175)
        self.assertEqual(bill.target.title, "A voted-on bill title")

        commons_div = zeitgeist.get(target_id=984)
        self.assertEqual(commons_div.target.title, "A commented-on commons division")

        lords_div = zeitgeist.get(target_id=840)
        self.assertEqual(lords_div.target.title, "A voted-on lords division")
