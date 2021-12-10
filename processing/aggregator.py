import csv
import os
from black import json
import shapefile
from tqdm import tqdm

from color import pixel
from download import DOWNLOAD_PATH
from shape import Region


def aggregate(state_id, population_center_file_url, shapefile_url, hide_output=True):
    regions = None
    with open(population_center_file_url) as csv_file:
        reader = csv.DictReader(csv_file)
        regions = list(reader)

    counties = {}

    if not hide_output:
        print("Parsing population data into tree...")
    for region in tqdm(regions, disable=hide_output):
        if region["COUNTYFP"] not in counties:
            counties[region["COUNTYFP"]] = {}

        county = counties[region["COUNTYFP"]]

        if region["TRACTCE"] not in county:
            county[region["TRACTCE"]] = {}

        tract = county[region["TRACTCE"]]

        population = int(region["POPULATION"])

        if region["BLKGRPCE"] not in tract:
            tract[region["BLKGRPCE"]] = population

    sf = shapefile.Reader(shapefile_url)
    geojson = sf.__geo_interface__

    scales = []

    if not hide_output:
        print("Calculating region area and scale factor...")
    for feature in tqdm(geojson["features"], disable=hide_output):
        properties = feature["properties"]

        county, tract, blkgrp = properties["COUNTYFP"], properties["TRACTCE"], properties["BLKGRPCE"]

        feature_pop = counties[county][tract][blkgrp]

        region_poly = Region(feature)
        area = region_poly.get_area()
        feature["geometry"] = region_poly.mapping

        properties["_population"] = feature_pop
        properties["_area"] = area

        scale = feature_pop / area

        properties["_scale"] = scale

        scales.append(scale)

    scales = sorted(scales)
    # print(sorted(scales))
    min_scale = 0
    max_scale = scales[-(len(scales) // 20)]  # Top 5%

    if not hide_output:
        print("Calculating region colors...")
    for feature in tqdm(geojson["features"], disable=hide_output):
        properties = feature["properties"]

        scale = properties["_scale"]

        linear_scale = int(round((scale / (max_scale - min_scale)) * 100, 0))
        linear_scale = min(linear_scale, 100)

        # print(linear_scale)

        r, g, b = pixel(linear_scale, width=101)

        # properties["color"] = "#%02x%02x%02x" % (r, g, b)
        properties["rgb"] = {"r": r, "g": g, "b": b}

    geojson["features"] = geojson["features"]

    if not hide_output:
        print("Writing to JSON file...")
    with open(os.path.join(DOWNLOAD_PATH, f"{state_id}.json"), "w") as f:
        json.dump(geojson, f)
        # json.dump({"type": "FeatureCollection", "features": ok_features}, f)
