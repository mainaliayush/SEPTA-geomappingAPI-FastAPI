'''
this file is just to parse and load teh data.
'''

import zipfile
import xml.etree.ElementTree as ET
import json
import logging
from fastapi import HTTPException

def parse_kmz(kmz_file):
    with zipfile.ZipFile(kmz_file, 'r') as z:
        for filename in z.namelist():
            if filename.endswith('.kml'):
                with z.open(filename) as kml_file:
                    tree = ET.parse(kml_file)
                    root = tree.getroot()
                    return root


def get_septa_data(file_name):
    stations = parse_kmz(file_name)
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

    final_septa_data = []
    for placemark in stations.findall('.//kml:Placemark', namespace):
        name_element = placemark.find('kml:name', namespace)
        coordinate_element = placemark.find('.//kml:coordinates', namespace)

        if name_element is not None and coordinate_element is not None:
            name = name_element.text.strip()
            coordinates = coordinate_element.text.strip()
            lon, lat, *_ = map(float, coordinates.split(','))

            final_septa_data.append({
                "name": name,
                "coordinates": [lat, lon] 
            })

    return final_septa_data
