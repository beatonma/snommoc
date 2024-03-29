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
    EXPECTED_KML_BERWICKUPONTWEED,
)


class ConstituencyBoundaryConstructionTests(LocalTestCase):
    def setUp(self) -> None:
        Constituency.objects.create(
            parliamentdotuk=146749,
            name="Aldershot",
            gss_code="E14000530",
            constituency_type="borough",
        )

        Constituency.objects.create(
            parliamentdotuk=146750,
            name="Aldridge-Brownhills",
            gss_code="E14000531",
            constituency_type="borough",
        )

        Constituency.objects.create(
            parliamentdotuk=146779,
            name="Berwick-upon-Tweed",
            gss_code="E14000554",
            constituency_type="borough",
        )

    def test_create_boundary(self):
        _create_boundary(
            Placemark(
                gss="E14000530",
                polygons=[],
                area="52978156.0157678",
                boundary_length="42197.6617288791",
                lat="51.288952",
                long="-0.7841",
            )
        )

        c: ConstituencyBoundary = ConstituencyBoundary.objects.get(
            constituency__parliamentdotuk=146749
        )
        self.assertEqual(c.constituency.parliamentdotuk, 146749)
        self.assertEqual(c.constituency.name, "Aldershot")
        self.assertEqual(c.constituency.gss_code, "E14000530")
        self.assertEqual(c.area, "52978156.0157678")
        self.assertEqual(c.boundary_length, "42197.6617288791")
        self.assertEqual(c.center_latitude, "51.288952")
        self.assertEqual(c.center_longitude, "-0.7841")

    def test_import_boundaries_from_file(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(this_dir, "data/data_kml_sample.kml")

        import_boundaries_from_file(file)
        self.assertEqual(ConstituencyBoundary.objects.all().count(), 3)

        c: ConstituencyBoundary = ConstituencyBoundary.objects.get(
            constituency__parliamentdotuk=146750
        )

        self.assertEqual(c.constituency.parliamentdotuk, 146750)
        self.assertEqual(c.constituency.gss_code, "E14000531")
        self.assertEqual(c.center_latitude, "52.620869")
        self.assertEqual(c.center_longitude, "-1.93166")
        self.assertEqual(c.area, "44016547.9783729")
        self.assertEqual(c.boundary_length, "38590.1779551054")
        self.assertEqual(c.boundary_kml, EXPECTED_KML_ALDRIDGE)

        c: ConstituencyBoundary = ConstituencyBoundary.objects.get(
            constituency__parliamentdotuk=146749
        )
        self.assertEqual(c.constituency.parliamentdotuk, 146749)
        self.assertEqual(c.constituency.name, "Aldershot")
        self.assertEqual(c.constituency.gss_code, "E14000530")
        self.assertEqual(c.area, "52978156.0157678")
        self.assertEqual(c.boundary_length, "42197.6617288791")
        self.assertEqual(c.center_latitude, "51.288952")
        self.assertEqual(c.center_longitude, "-0.7841")
        self.assertEqual(c.boundary_kml, EXPECTED_KML_ALDERSHOT)

        c: ConstituencyBoundary = ConstituencyBoundary.objects.get(
            constituency__parliamentdotuk=146779
        )
        self.assertEqual(c.constituency.parliamentdotuk, 146779)
        self.assertEqual(c.constituency.name, "Berwick-upon-Tweed")
        self.assertEqual(c.constituency.gss_code, "E14000554")
        self.assertEqual(c.area, "2427302856.23729")
        self.assertEqual(c.boundary_length, "404925.7674161")
        self.assertEqual(c.center_latitude, "55.40086")
        self.assertEqual(c.center_longitude, "-1.9312")
        self.assertEqual(c.boundary_kml, EXPECTED_KML_BERWICKUPONTWEED)

    def tearDown(self) -> None:
        self.delete_instances_of(
            Constituency,
            ConstituencyBoundary,
        )
