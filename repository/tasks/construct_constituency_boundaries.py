"""
Parse constituency boundaries from ONS national kml file.
https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(BDY_PCON%2CDEC_2018)
"""

import logging
from typing import Optional
from xml.parsers import expat

from repository.models import (
    Constituency,
    ConstituencyBoundary,
)

log = logging.getLogger(__name__)


error_count = 0


class Polygon:
    def __init__(self, path=''):
        self.path = path
        self.is_open = False

    def add_tag(self, tag, attrs):
        self.is_open = True
        attr_string = ''
        for key, value in attrs:
            attr_string = f'{attr_string} {key}="{value}"'
        self.path = f'{self.path}<{tag}{attr_string}>'

    def add_value(self, value):
        self.is_open = True
        self.path = self.path + value

    def close_tag(self, tag):
        self.path = f'{self.path}</{tag}>'
        if tag == 'Polygon':
            self.is_open = False

    def validate(self):
        assert(self.path != '')
        assert(self.is_open is False)

    def __str__(self):
        return 'EMPTY!' if self.path == '' else 'HAS PATH'


class Placemark:
    def __init__(self, gss='', name='', lat='', long='', area='', boundary_length='', polygon=''):
        self.gss = gss
        self.name = name
        self.lat = lat
        self.long = long
        self.area = area
        self.boundary_length = boundary_length
        self.polygon = Polygon(polygon)

        self.current_tag = None

    def validate(self):
        assert(self.gss != '')
        assert(self.name != '')
        assert(self.lat != '')
        assert(self.long != '')
        assert(self.area != '')
        assert(self.boundary_length != '')
        self.polygon.validate()

    def __str__(self):
        return f'{self.gss} {self.name} {self.lat} {self.long} {self.area} {self.boundary_length} {self.polygon}'

    def open_data_tag(self, attrs):
        self.current_tag = attrs['name']

    def open_tag(self, tag, attrs):
        if tag == 'Polygon' or self.polygon.is_open:
            self.polygon.add_tag(tag, attrs)

    def set_value(self, value):
        if self.polygon.is_open:
            self.polygon.add_value(value)
            return

        if self.current_tag is None:
            return

        elif self.current_tag == 'pcon18cd':
            self.gss = self.gss + value

        elif self.current_tag == 'pcon18nm':
            self.name = self.name + value

        elif self.current_tag == 'lat':
            self.lat = self.lat + value

        elif self.current_tag == 'long':
            self.long = self.long + value

        elif self.current_tag == 'st_areashape':
            self.area = self.area + value

        elif self.current_tag == 'st_lengthshape':
            self.boundary_length = self.boundary_length + value

    def close_tag(self, tag):
        if self.polygon.is_open:
            self.polygon.close_tag(tag)

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
            'boundary_kml': _polygon_to_kml(placemark.polygon),
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

        if tag == 'Placemark':
            if placemark is not None:
                raise Exception(f'placemark has not been reset correctly: {placemark}')
            placemark = Placemark()

        elif tag == 'SimpleData':
            placemark.open_data_tag(attrs)

        elif placemark is not None:
            placemark.open_tag(tag, attrs)

    def end_handler(tag):
        nonlocal placemark
        if placemark is None:
            return

        if tag == 'Placemark':
            log.info(f'saving {placemark}')
            placemark.validate()
            _create_boundary(placemark)
            placemark = None

        elif tag == 'SimpleData':
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


def _polygon_to_kml(polygon: Polygon) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><Placemark>{polygon.path}</Placemark></Document></kml>"""

