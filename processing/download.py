import asyncio
import os
import shutil
import aiohttp
import zipfile
import tqdm.asyncio
from pathlib import Path
from urllib import parse


POP_BLOCK_GROUP_URLS = [f"https://www2.census.gov/geo/docs/reference/cenpop2020/blkgrp/CenPop2020_Mean_BG{i + 1:02}.txt" for i in range(56)]

SHAPEFILE_BLOCK_GORUP_URLS = [f"https://www2.census.gov/geo/tiger/TIGER2020/BG/tl_2020_{i + 1:02}_bg.zip" for i in range(56)]


DOWNLOAD_PATH = Path("data/")
CHUNK_SIZE = 1024 * 32

if __name__ == "__main__":
    sem = asyncio.Semaphore(30)


async def download_file(url):
    resource_path = parse.urlparse(url).path
    resource = resource_path[resource_path.rfind("/") + 1 :]

    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return

                with open(os.path.join(DOWNLOAD_PATH, resource), "wb") as fd:
                    async for chunk in resp.content.iter_chunked(CHUNK_SIZE):
                        fd.write(chunk)


async def queue_downloads():
    # Recreate directory
    shutil.rmtree(DOWNLOAD_PATH)
    os.mkdir(DOWNLOAD_PATH)

    tasks = []
    for pop_block_group_url in POP_BLOCK_GROUP_URLS:
        task = asyncio.create_task(download_file(pop_block_group_url))
        tasks.append(task)

    for pop_block_group_url in SHAPEFILE_BLOCK_GORUP_URLS:
        task = asyncio.create_task(download_file(pop_block_group_url))
        tasks.append(task)

    for task in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await task


async def unzip_file(path: Path):
    target_dir = os.path.join(DOWNLOAD_PATH, path.stem)

    # try:
    #     with zipfile.ZipFile(path, "r") as zip_file:
    #         bad_files = zip_file.testzip()

    #         if bad_files:
    #             raise Exception(f"Found bad files")
    # except Exception as err:
    #     print(f"{path} is a bad zip file")
    #     return

    with zipfile.ZipFile(path, "r") as zip_file:
        zip_file.extractall(target_dir)


async def queue_unzip_files():
    tasks = []
    for file in os.listdir(DOWNLOAD_PATH):
        file_path = os.path.join(DOWNLOAD_PATH, file)
        if os.path.isfile(file_path) and Path(file_path).suffix == ".zip":
            tasks.append(asyncio.create_task(unzip_file(Path(file_path))))

    for task in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await task


def download_files():
    asyncio.run(queue_downloads())


def unzip_files():
    asyncio.run(queue_unzip_files())


if __name__ == "__main__":
    download_files()
    unzip_files()
