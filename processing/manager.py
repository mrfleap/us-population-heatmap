import json
import os
import pathlib
import time

from tqdm import tqdm
from aggregator import aggregate
from download import DOWNLOAD_PATH, download_files, unzip_files
from tqdm.contrib.concurrent import process_map


def main():
    start = time.time()
    # print("Downloading files...")
    # download_files()

    # print("Unzipping shapefiles...")
    # unzip_files()

    state_ids = []
    for file in os.listdir(DOWNLOAD_PATH):
        file_path = os.path.join(DOWNLOAD_PATH, file)

        if os.path.isfile(file_path) and pathlib.Path(file_path).suffix == ".txt":
            state_ids.append(file[file.index("BG") + 2 : file.index(".")])

    # print("Computing population JSON heatmaps...")
    # compute_json_heatmaps(state_ids)

    print("Aggregating JSON files into one...")
    aggegrate_json_files(state_ids)

    end = time.time()
    print(f"Done in {(end - start):0.2f}s")


def compute_json_heatmaps(state_ids):
    data_files = []
    for state_id in state_ids:
        data_files.append(
            (
                state_id,
                os.path.join(DOWNLOAD_PATH, f"CenPop2020_Mean_BG{state_id}.txt"),
                os.path.join(DOWNLOAD_PATH, f"tl_2020_{state_id}_bg", f"tl_2020_{state_id}_bg.shp"),
            )
        )

    process_map(create_json_for_state, data_files, max_workers=4)


def aggegrate_json_files(state_ids):
    with open("public/data/pop.json", "w") as f:
        f.write("""{"type": "FeatureCollection", "features": [""")

    # state_ids = state_ids[:2]

    features = []
    for state_id in tqdm(state_ids):
        geojson = None
        with open(os.path.join(DOWNLOAD_PATH, f"{state_id}.json")) as f:
            geojson = json.load(f)

        with open("public/data/pop.json", "a") as f:
            f.write(json.dumps(geojson["features"])[1:-1] + ("," if state_id != state_ids[-1] else ""))

    with open("public/data/pop.json", "a") as f:
        f.write("]}")


def create_json_for_state(args):
    return aggregate(*args, hide_output=True)


if __name__ == "__main__":
    main()
