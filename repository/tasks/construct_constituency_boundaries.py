"""
Parse constituency boundaries from ONS national kml file.
https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(BDY_PCON%2CDEC_2018)
"""

import logging
from typing import (
    List,
    Optional,
)
from xml.parsers import expat

from repository.models import (
    Constituency,
    ConstituencyBoundary,
)

VALUE_GSS = 'pcon18cd'
VALUE_NAME = 'pcon18nm'
VALUE_LATITUDE = 'lat'
VALUE_LONGITUDE = 'long'
VALUE_AREA = 'st_areashape'
VALUE_LENGTH = 'st_lengthshape'

TAG_PLACEMARK = 'Placemark'
TAG_MULTIGEOMETRY = 'MultiGeometry'
TAG_POLYGON = 'Polygon'
TAG_SIMPLEDATA = 'SimpleData'


log = logging.getLogger(__name__)


error_count = 0


class Polygon:
    def __init__(self, kml=''):
        self.kml = kml
        self.is_open = False

    def add_tag(self, tag, attrs):
        self.is_open = True
        attr_string = ''
        for key, value in attrs:
            attr_string = f'{attr_string} {key}="{value}"'
        self.kml = f'{self.kml}<{tag}{attr_string}>'

    def add_value(self, value):
        self.is_open = True
        self.kml = self.kml + value

    def close_tag(self, tag):
        self.kml = f'{self.kml}</{tag}>'
        if tag == TAG_POLYGON:
            self.is_open = False

    def validate(self):
        assert(self.kml != '')
        assert(self.is_open is False)

    def __str__(self):
        return 'EMPTY!' if self.kml == '' else 'HAS KML'


class Geometry:
    def __init__(self, polygons: List[Polygon]):
        self.is_open: bool = False
        self.polygons: List[Polygon] = polygons
        self.active_polygon: Optional[Polygon] = None

    def add_tag(self, tag, attrs):
        print(f'add tag "{tag}"')
        if tag == TAG_MULTIGEOMETRY:
            self.is_open = True
            return
        if tag == TAG_POLYGON:
            self.is_open = True
            self.active_polygon = Polygon()

        self.active_polygon.add_tag(tag, attrs)

    def add_value(self, value):
        print(f'add value "{value}"')
        if self.active_polygon is not None:
            self.active_polygon.add_value(value)

    def close_tag(self, tag):
        print(f'close tag {tag}')
        if self.active_polygon is not None:
            self.active_polygon.close_tag(tag)

            if not self.active_polygon.is_open:
                self.polygons.append(self.active_polygon)
                self.active_polygon = None
        if tag == TAG_MULTIGEOMETRY:
            self.is_open = False

    def kml(self):
        polygon_kml = ''.join([p.kml for p in self.polygons])
        if len(self.polygons) > 1:
            return f'<{TAG_MULTIGEOMETRY}>{polygon_kml}</{TAG_MULTIGEOMETRY}>'
        else:
            return polygon_kml

    def validate(self):
        assert(len(self.polygons) > 0)
        for p in self.polygons:
            p.validate()

    def __str__(self):
        return f'Geometry: {len(self.polygons)} shapes'


class Placemark:
    def __init__(
            self, gss='', name='', lat='', long='', area='', boundary_length='', polygons=None
    ):
        self.gss = gss
        self.name = name
        self.lat = lat
        self.long = long
        self.area = area
        self.boundary_length = boundary_length
        self.geometry: Geometry = Geometry(polygons or [])

        self.current_tag = None

    def validate(self):
        assert(self.gss != '')
        assert(self.name != '')
        assert(self.lat != '')
        assert(self.long != '')
        assert(self.area != '')
        assert(self.boundary_length != '')
        self.geometry.validate()

    def __str__(self):
        return f'{self.gss} {self.name} {self.lat} {self.long} {self.area} {self.boundary_length} {self.geometry}'

    def open_data_tag(self, attrs):
        self.current_tag = attrs['name']

    def open_tag(self, tag, attrs):
        if tag == TAG_MULTIGEOMETRY or tag == TAG_POLYGON or self.geometry.is_open:
            self.geometry.add_tag(tag, attrs)

    def set_value(self, value):
        if self.geometry.is_open:
            self.geometry.add_value(value)
            return

        if self.current_tag is None:
            return

        elif self.current_tag == VALUE_GSS:
            self.gss = self.gss + value

        elif self.current_tag == VALUE_NAME:
            self.name = self.name + value

        elif self.current_tag == VALUE_LATITUDE:
            self.lat = self.lat + value

        elif self.current_tag == VALUE_LONGITUDE:
            self.long = self.long + value

        elif self.current_tag == VALUE_AREA:
            self.area = self.area + value

        elif self.current_tag == VALUE_LENGTH:
            self.boundary_length = self.boundary_length + value

    def close_tag(self, tag):
        if self.geometry.is_open:
            self.geometry.close_tag(tag)

    def close_data_tag(self):
        self.current_tag = None


def _create_boundary(placemark: Placemark):
    try:
        constituency = Constituency.objects.get(gss_code=placemark.gss)
    except (Constituency.DoesNotExist, Constituency.MultipleObjectsReturned) as e:
        log.warning(f'Constituency lookup failed for placemark={placemark}')
        return

    c, _ = ConstituencyBoundary.objects.get_or_create(
        constituency=constituency,
        defaults={
            'boundary_kml': _geometry_to_kml(placemark.geometry),
            'center_latitude': placemark.lat,
            'center_longitude': placemark.long,
            'area': placemark.area,
            'boundary_length': placemark.boundary_length,
        }
    )


def import_boundaries_from_file(filepath):
    placemark: Optional[Placemark] = None

    def start_handler(tag, attrs):
        nonlocal placemark

        if tag == TAG_PLACEMARK:
            if placemark is not None:
                raise Exception(f'placemark has not been reset correctly: {placemark}')
            placemark = Placemark()

        elif tag == TAG_SIMPLEDATA:
            placemark.open_data_tag(attrs)

        elif placemark is not None:
            placemark.open_tag(tag, attrs)

    def end_handler(tag):
        nonlocal placemark
        if placemark is None:
            return

        if tag == TAG_PLACEMARK:
            log.info(f'saving {placemark}')
            placemark.validate()
            _create_boundary(placemark)
            print(f'finished placemark: {placemark.name}')
            placemark = None

        elif tag == TAG_SIMPLEDATA:
            placemark.close_data_tag()

        else:
            placemark.close_tag(tag)

    def character_handler(chars):
        nonlocal placemark
        if placemark is None:
            return

        placemark.set_value(chars)

    parser = expat.ParserCreate('utf-8')
    parser.StartElementHandler = start_handler
    parser.CharacterDataHandler = character_handler
    parser.EndElementHandler = end_handler

    with open(filepath, 'rb') as f:
        parser.ParseFile(f)


def _geometry_to_kml(geometry: Geometry) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><Placemark>{geometry.kml()}</Placemark></Document></kml>"""

