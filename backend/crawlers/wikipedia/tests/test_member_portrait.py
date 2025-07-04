from unittest.mock import patch

from basetest.testcase import DatabaseTestCase
from crawlers.context import TaskContext
from crawlers.wikipedia.tasks.member_portrait import update_wikipedia_member_portraits
from notifications.models import TaskNotification
from repository.models import MemberPortrait, Person
from repository.tests.data.create import create_sample_person

CONTEXT = TaskContext(None, TaskNotification())

"""
Edited sample response for main images from url:
https://en.wikipedia.org/w/api.php?titles=David_Evans%2C_Baron_Evans_of_Watford|Robert_Fellowes%2C_Baron_Fellowes|Daniel_Finkelstein|Michael_Forsyth%2C_Baron_Forsyth_of_Drumlean|Christopher_Fox%2C_Baron_Fox&action=query&format=json&pilicense=free&maxlag=2&prop=pageimages&piprop=original|thumbnail
"""
_SAMPLE_MAIN = {
    "batchcomplete": "",
    "query": {
        "normalized": [
            {
                "from": "David_Evans,_Baron_Evans_of_Watford",
                "to": "David Evans, Baron Evans of Watford",
            },
            {
                "from": "Robert_Fellowes,_Baron_Fellowes",
                "to": "Robert Fellowes, Baron Fellowes",
            },
            {"from": "Daniel_Finkelstein", "to": "Daniel Finkelstein"},
            {
                "from": "Michael_Forsyth,_Baron_Forsyth_of_Drumlean",
                "to": "Michael Forsyth, Baron Forsyth of Drumlean",
            },
            {"from": "Christopher_Fox,_Baron_Fox", "to": "Christopher Fox, Baron Fox"},
        ],
        "pages": {
            "416749": {
                "pageid": 416749,
                "ns": 0,
                "title": "Michael Forsyth, Baron Forsyth of Drumlean",
            },
            "2244218": {
                "pageid": 2244218,
                "ns": 0,
                "title": "Robert Fellowes, Baron Fellowes",
                "original": {
                    "source": "https://upload.wikimedia.org/wikipedia/commons/PatchedPrimaryImages.jpg",
                    "width": 220,
                    "height": 179,
                },
                "thumbnail": {
                    "source": "https://upload.wikimedia.org/wikipedia/commons/thumb/PatchedSample.png",
                    "width": 1000,
                    "height": 814,
                },
            },
            "10237002": {
                "pageid": 10237002,
                "ns": 0,
                "title": "David Evans, Baron Evans of Watford",
                "original": {
                    "source": "https://upload.wikimedia.org/wikipedia/en/0/02/Lord_David_Evans.jpg",
                    "width": 356,
                    "height": 528,
                },
                "thumbnail": {
                    "source": "https://upload.wikimedia.org/wikipedia/en/0/02/Lord_David_Evans.jpg",
                    "width": 356,
                    "height": 528,
                },
            },
            "14234607": {
                "pageid": 14234607,
                "ns": 0,
                "title": "Daniel Finkelstein",
                "original": {
                    "source": "https://upload.wikimedia.org/wikipedia/commons/2/25/Daniel_Finkelstein_at_Ten_Years_of_Shaping_the_Policy_Agenda.jpg",
                    "width": 2427,
                    "height": 2197,
                },
                "thumbnail": {
                    "source": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Daniel_Finkelstein_at_Ten_Years_of_Shaping_the_Policy_Agenda.jpg/1000px-Daniel_Finkelstein_at_Ten_Years_of_Shaping_the_Policy_Agenda.jpg",
                    "width": 1000,
                    "height": 905,
                },
            },
            "44009709": {
                "pageid": 44009709,
                "ns": 0,
                "title": "Christopher Fox, Baron Fox",
                "original": {
                    "source": "https://upload.wikimedia.org/wikipedia/commons/6/60/Patched__Chris_Fox_Bournemouth_1.jpg",
                    "width": 2000,
                    "height": 2000,
                },
                "thumbnail": {
                    "source": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Chris_Fox_Bournemouth_1.jpg/1000px-Chris_Fox_Bournemouth_1__patched.jpg",
                    "width": 1000,
                    "height": 1000,
                },
            },
        },
    },
}


class WikiMemberPortraitTests(DatabaseTestCase):
    def setUp(self) -> None:
        create_sample_person(wikipedia="David_Evans,_Baron_Evans_of_Watford")
        create_sample_person(wikipedia="Robert_Fellowes,_Baron_Fellowes")
        create_sample_person(wikipedia="Daniel_Finkelstein")
        create_sample_person(wikipedia="Michael_Forsyth,_Baron_Forsyth_of_Drumlean")
        create_sample_person(wikipedia="Christopher_Fox,_Baron_Fox")

    def test_update_wikipedia_member_portraits(self):
        with patch(
            "crawlers.wikipedia.wikipedia_client.get_json",
            side_effect=lambda *args, **kwargs: _SAMPLE_MAIN,
        ):
            members = Person.objects.all()
            update_wikipedia_member_portraits(members, CONTEXT)

        cfox = MemberPortrait.objects.get(
            person__wikipedia="Christopher_Fox,_Baron_Fox"
        )
        self.assertEqual(
            cfox.fullsize_url,
            "https://upload.wikimedia.org/wikipedia/commons/6/60/Patched__Chris_Fox_Bournemouth_1.jpg",
        )
        cfox_thumb = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Chris_Fox_Bournemouth_1.jpg/1000px-Chris_Fox_Bournemouth_1__patched.jpg"
        self.assertEqual(cfox.square_url, cfox_thumb)
        self.assertEqual(cfox.tall_url, cfox_thumb)
        self.assertEqual(cfox.wide_url, cfox_thumb)
