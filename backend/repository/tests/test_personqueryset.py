from functools import partial

from basetest.testcase import LocalTestCase
from repository.models import Person
from repository.tests.data.create import (
    create_sample_constituency,
    create_sample_person,
    create_sample_representative,
)


class PersonQuerySetTests(LocalTestCase):
    def test_get_for_constituency__by_constituency(self):
        create_sample_constituency()
        mp = create_sample_person()
        create_sample_constituency()

        create_sample_constituency(name="0123456789", mp=mp)

        get = partial(
            Person.objects.get_for_constituency,
            mp.name,
            similarity_threshold=60,
        )

        self.assertEqual(get("0123456789"), mp)  # exact
        self.assertEqual(get("012345"), mp)  # similar enough
        self.assertIsNone(get("0123"))  # not similar enough

    def test_get_for_constituency__by_constituency_representative(
        self,
    ):
        mp = create_sample_person()
        constituency = create_sample_constituency(name="0123456789")
        create_sample_representative(person=mp, constituency=constituency)

        get = partial(
            Person.objects.get_for_constituency,
            mp.name,
            similarity_threshold=60,
        )

        self.assertIsNone(constituency.mp)
        self.assertEqual(get("0123456789"), mp)
        self.assertEqual(get("012345"), mp)
        self.assertIsNone(get("0123"))
