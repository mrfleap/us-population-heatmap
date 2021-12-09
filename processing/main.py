import csv
from black import json
import shapefile
from tqdm import tqdm

from color import pixel
from shape import Region


def main():
    regions = None
    with open("data/CenPop2020_Mean_BG53.txt") as csv_file:
        reader = csv.DictReader(csv_file)
        regions = list(reader)

    counties = {}

    print("Parsing population data into tree...")
    for region in tqdm(regions):
        if region["COUNTYFP"] not in counties:
            counties[region["COUNTYFP"]] = {}

        county = counties[region["COUNTYFP"]]

        if region["TRACTCE"] not in county:
            county[region["TRACTCE"]] = {}

        tract = county[region["TRACTCE"]]

        population = int(region["POPULATION"])

        if region["BLKGRPCE"] not in tract:
            tract[region["BLKGRPCE"]] = population

    sf = shapefile.Reader("data/tl_2020_53_bg/tl_2020_53_bg.shp")
    geojson = sf.__geo_interface__

    scales = []

    print("Calculating region area and scale factor...")
    for feature in tqdm(geojson["features"]):
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

    print("Calculating region colors...")
    for feature in tqdm(geojson["features"]):
        properties = feature["properties"]

        scale = properties["_scale"]

        linear_scale = int(round((scale / (max_scale - min_scale)) * 100, 0))
        linear_scale = min(linear_scale, 100)

        # print(linear_scale)

        r, g, b = [int(t * 255) for t in pixel(linear_scale, width=101)]

        properties["color"] = "#%02x%02x%02x" % (r, g, b)

    geojson["features"] = geojson["features"]
    # ok_features = []

    # for feature in geojson["features"]:
    #     add = True
    #     geometry = feature["geometry"]

    #     for set in geometry["coordinates"]:
    #         for pair in set:
    #             for num in pair:
    #                 if (isinstance(num, float)) or (isinstance(num, int)):
    #                     add = False

    #     if add:
    #         ok_features.append(feature)

    print("Writing to JSON file...")
    with open("src/assets/wa_pop.json", "w") as f:
        json.dump(geojson, f)
        # json.dump({"type": "FeatureCollection", "features": ok_features}, f)


if __name__ == "__main__":
    main()
