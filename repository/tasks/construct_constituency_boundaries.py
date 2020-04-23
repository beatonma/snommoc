"""
Parse constituency boundaries from ONS national kml file.
https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(BDY_PCON%2CDEC_2018)
"""

import logging
import re

from repository.models import (
    Constituency,
    ConstituencyBoundary,
)

log = logging.getLogger(__name__)


def _simpledata(key):
    return re.compile(rf'<SimpleData name="{key}">([a-zA-Z\d\-.]+)</SimpleData>', re.DOTALL)


PLACEMARK_REGEX = re.compile(r'(<Placemark>.*?</Placemark>)', re.DOTALL)
POLYGON_REGEX = re.compile(r'.*(<Polygon>.*?</Polygon>).*')
LATITUDE_REGEX = _simpledata('lat')
LONGITUDE_REGEX = _simpledata('long')
AREA_REGEX = _simpledata('st_areashape')
LENGTH_REGEX = _simpledata('st_lengthshape')
GSS_REGEX = _simpledata('pcon18cd')


def _create_boundary(constituency_gss_code, kml, boundary_area, boundary_length, center_lat, center_long):
    try:
        constituency = Constituency.objects.get(gss_code=constituency_gss_code)
    except (Constituency.DoesNotExist, Constituency.MultipleObjectsReturned) as e:
        log.warning(f'Constituency lookup failed for gss={constituency_gss_code}: {e}')
        return

    c, _ = ConstituencyBoundary.objects.get_or_create(
        constituency=constituency,
        defaults={
            'boundary_kml': kml,
            'center_latitude': center_lat,
            'center_longitude': center_long,
            'area': boundary_area,
            'boundary_length': boundary_length,
        }
    )


def import_boundaries_from_file(filepath):
    imported_count = 0
    chunk = []

    for line in open(filepath, 'r'):
        if '<Placemark>' in line:
            chunk = [line]
        elif '</Placemark>' in line:
            chunk.append(line)
            build_constituency_boundaries_from_text(''.join(chunk))
            imported_count = imported_count + 1
        else:
            chunk.append(line)

    return imported_count


def build_constituency_boundaries_from_text(text: str):
    results = PLACEMARK_REGEX.findall(text)
    for place in results:
        try:
            kml = _build_boundary_kml(place)
            area = AREA_REGEX.search(place).group(1)
            length = LENGTH_REGEX.search(place).group(1)
            latitude = LATITUDE_REGEX.search(place).group(1)
            longitude = LONGITUDE_REGEX.search(place).group(1)
            gss = GSS_REGEX.search(place).group(1)

            _create_boundary(gss, kml, area, length, latitude, longitude)
        except Exception as e:
            log.warning(f'Failed to build constituency boundary: {e}')


def _build_boundary_kml(placemark_xml) -> str:
    polygon = POLYGON_REGEX.search(placemark_xml).group(1)
    return f"""<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><Placemark>{polygon}</Placemark></Document></kml>"""

