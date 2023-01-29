import os

os.environ["OMP_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["VECLIB_MAXIMUM_THREADS"] = "4"
os.environ["NUMEXPR_NUM_THREADS"] = "4"

import requests
import json
import pandas as pd
from datetime import datetime, date
from multiprocessing import Process
from typing import List, Dict, NoReturn
from data_aggregation import (
    aggregate_data_for_future,
    transform_tables,
    get_block_data,
    get_table_data,
    prepare_data
)


def collect_tables(header: Dict, folder: str) -> NoReturn:
    feed_table = "to_jZ2mBfIs_jkdXuB14_1"
    feed_table_home = "to_jZ2mBfIs_jkdXuB14_2"
    feed_table_guest = "to_jZ2mBfIs_jkdXuB14_3"

    url_table = f"https://d.flashscorekz.com/x/feed/{feed_table}"
    data_table = requests.get(url=url_table, headers=header).text.split(sep="¬")
    block_data_table = get_block_data(data_table)
    get_table_data(block_data_table, name=folder + "/table.json")

    url_home = f"https://d.flashscorekz.com/x/feed/{feed_table_home}"
    data_home = requests.get(url=url_home, headers=header).text.split(sep="¬")
    block_data_home = get_block_data(data_home)
    get_table_data(block_data_home, name=folder + "/table_home.json")

    url_guest = f"https://d.flashscorekz.com/x/feed/{feed_table_guest}"
    data_guest = requests.get(url=url_guest, headers=header).text.split(sep="¬")
    block_data_guest = get_block_data(data_guest)
    get_table_data(block_data_guest, name=folder + "/table_guest.json")


def collect_results(header: Dict, index: int, folder: str) -> NoReturn:
    feed = f"f_4_-{str(index)}_3_ru-kz_1"
    url_table = f"https://d.flashscorekz.com/x/feed/{feed}"
    data_table = requests.get(url=url_table, headers=header).text.split(sep="¬")
    block_data_table = get_block_data(data_table)
    cur_league = ""
    results = []
    column_names = [
        "home_team",
        "guest_team",
        "home_score",
        "guest_score",
        "tie_in_ft",
        "aot",
        "shootout",
        "date",
    ]
    for block in block_data_table:
        if "~ZA" in block:
            if block["~ZA"] == "США: НХЛ":
                cur_league = "США: НХЛ"
            else:
                cur_league = "other"

        if cur_league == "США: НХЛ":
            if "AT" and "AU" in block.keys():
                tie_in_full_time = 1
                if block.get("BG") == block.get("BH"):
                    aot = 0
                    shootout = 1
                else:
                    aot = 1
                    shootout = 0
            else:
                tie_in_full_time = 0
                aot = 0
                shootout = 0
            if "CX" in block.keys():
                results.append(
                    [
                        block.get("CX"),
                        block.get("AF"),
                        int(block.get("AG")),
                        int(block.get("AH")),
                        tie_in_full_time,
                        aot,
                        shootout,
                        datetime.fromtimestamp(int(block.get("AD"))),
                    ]
                )

    df = pd.DataFrame(results, columns=column_names)
    name = folder + "/results_" + str(index + 1) + ".json"
    df.to_json(name, orient="records")


def get_future_games(header: Dict, folder: str) -> NoReturn:
    feed = f"f_4_1_3_ru-kz_1"
    url_table = f"https://d.flashscorekz.com/x/feed/{feed}"
    data_table = requests.get(url=url_table, headers=header).text.split(sep="¬")
    block_data_table = get_block_data(data_table)
    cur_league = ""
    results = []
    column_names = [
        "home_team",
        "guest_team",
        "date",
    ]
    for block in block_data_table:
        if "~ZA" in block:
            if block["~ZA"] == "США: НХЛ":
                cur_league = "США: НХЛ"
            else:
                cur_league = "other"

        if cur_league == "США: НХЛ":
            if "CX" in block.keys():
                results.append(
                    [
                        block.get("CX"),
                        block.get("AF"),
                        datetime.fromtimestamp(int(block.get("AD"))),
                    ]
                )

    df = pd.DataFrame(results, columns=column_names)
    name = folder + "/next_tour_games.json"
    df.to_json(name, orient="records")


def collect_data(folder:str) -> NoReturn:
    header = {"x-fsign": "SW9D1eZo"}
    print("Collecting tables...")
    collect_tables(header, folder)
    print("Collecting game results...")
    # part_jobs = []
    # for index in range(8):
    #     part_jobs.append(Process(target=collect_results, args=(header, index)))

    # for job in part_jobs:
    #     job.start()

    # for job in part_jobs:
    #     job.join()
    collect_results(header, index=0,folder=folder)

    print("Collecting future games...")
    get_future_games(header, folder)


if __name__ == "__main__":
    today = date.today()
    cur_date = str(today.day) + '.' + str(today.month)
    folder = f'data_{cur_date}'
    if not os.path.isdir(folder):
        os.mkdir(folder)
    collect_data(folder)
    transform_tables(folder)
    aggregate_data_for_future(folder)
    prepare_data(folder)
