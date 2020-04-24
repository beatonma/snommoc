"""

"""

import logging
import os

from basetest.testcase import LocalTestCase
from repository.models import (
    Constituency,
    ConstituencyBoundary,
)
from repository.tasks.construct_constituency_boundaries import (
    Placemark,
    _create_boundary,
    import_boundaries_from_file,
)
from repository.tests.data.data_construct_constituency_boundaries import (
    EXPECTED_KML_ALDERSHOT,
    EXPECTED_KML_ALDRIDGE,
)

log = logging.getLogger(__name__)


class ConstituencyBoundaryConstructionTests(LocalTestCase):
    def setUp(self) -> None:
        Constituency.objects.create(
            parliamentdotuk=1234,
            name='Aldershot',
            gss_code='E14000530',
            constituency_type='borough',
        ).save()

        Constituency.objects.create(
            parliamentdotuk=4321,
            name='Aldridge-Brownhills',
            gss_code='E14000531',
            constituency_type='borough',
        ).save()

    def test_create_boundary(self):
        _create_boundary(Placemark(
            gss='E14000530',
            polygon='',
            area='52978156.0157678',
            boundary_length='42197.6617288791',
            lat='51.288952',
            long='-0.7841',
        ))

        c: ConstituencyBoundary = ConstituencyBoundary.objects.get(constituency__parliamentdotuk=1234)
        self.assertEqual(c.constituency.parliamentdotuk, 1234)
        self.assertEqual(c.constituency.name, 'Aldershot')
        self.assertEqual(c.constituency.gss_code, 'E14000530')
        self.assertEqual(c.area, '52978156.0157678')
        self.assertEqual(c.boundary_length, '42197.6617288791')
        self.assertEqual(c.center_latitude, '51.288952')
        self.assertEqual(c.center_longitude, '-0.7841')

    def test_import_boundaries_from_file(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(this_dir, 'data/data_kml_sample.kml')

        import_boundaries_from_file(file)
        self.assertEqual(ConstituencyBoundary.objects.all().count(), 2)

        c: ConstituencyBoundary = ConstituencyBoundary.objects.get(
            constituency__parliamentdotuk=4321)

        self.assertEqual(c.constituency.parliamentdotuk, 4321)
        self.assertEqual(c.constituency.gss_code, 'E14000531')
        self.assertEqual(c.center_latitude, '52.620869')
        self.assertEqual(c.center_longitude, '-1.93166')
        self.assertEqual(c.area, '44016547.9783729')
        self.assertEqual(c.boundary_length, '38590.1779551054')
        self.assertEqual(c.boundary_kml, EXPECTED_KML_ALDRIDGE)

        c: ConstituencyBoundary = ConstituencyBoundary.objects.get(
            constituency__parliamentdotuk=1234)
        self.assertEqual(c.constituency.parliamentdotuk, 1234)
        self.assertEqual(c.constituency.name, 'Aldershot')
        self.assertEqual(c.constituency.gss_code, 'E14000530')
        self.assertEqual(c.area, '52978156.0157678')
        self.assertEqual(c.boundary_length, '42197.6617288791')
        self.assertEqual(c.center_latitude, '51.288952')
        self.assertEqual(c.center_longitude, '-0.7841')
        self.assertEqual(c.boundary_kml, EXPECTED_KML_ALDERSHOT)

    def tearDown(self) -> None:
        self.delete_instances_of(
            Constituency,
            ConstituencyBoundary
        )
