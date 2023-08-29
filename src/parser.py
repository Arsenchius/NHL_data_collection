import os

os.environ["OMP_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["VECLIB_MAXIMUM_THREADS"] = "4"
os.environ["NUMEXPR_NUM_THREADS"] = "4"

import requests
import json
import pandas as pd
from datetime import datetime, date, timedelta
import time
from multiprocessing import Process
from typing import List, Dict, NoReturn
from data_aggregation import (
    aggregate_data_for_future,
    transform_tables,
    get_block_data,
    get_table_data,
    prepare_data,
)
import argparse

fence = "-------------------------------------------------------------"


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


def collect_results(header: Dict, index: int, folder: str) -> str:
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
    current_time = datetime.now()
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
                game_time = datetime.fromtimestamp(int(block.get("AD")))
                if game_time < current_time:
                    results.append(
                        [
                            block.get("CX"),
                            block.get("AF"),
                            int(block.get("AG")),
                            int(block.get("AH")),
                            tie_in_full_time,
                            aot,
                            shootout,
                            game_time,
                        ]
                    )

    df = pd.DataFrame(results, columns=column_names)
    name = folder + "/results_1.json"
    df.to_json(name, orient="records")
    if df.empty:
        return "no results today"
    else:
        return "ok"


def get_future_games(header: Dict, folder: str, day_index: int) -> bool:
    feed = f"f_4_{day_index}_3_ru-kz_1"
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


def collect_data(folder: str, index: int, day_index: int) -> NoReturn:
    header = {"x-fsign": "SW9D1eZo"}
    print("Collecting tables...")
    collect_tables(header, folder)
    print("Table data collected!")
    print(fence)
    print("Collecting game results...")
    # part_jobs = []
    # for index in range(8):
    #     part_jobs.append(Process(target=collect_results, args=(header, index)))

    # for job in part_jobs:
    #     job.start()

    # for job in part_jobs:
    #     job.join()
    err = collect_results(header, index=index, folder=folder)
    if err == "ok":
        print("Games results collected!")
    else:
        print("No results of matches today(")
    print(fence)

    print("Collecting future games...")
    get_future_games(header, folder, day_index)


def run(args):
    day = args.day
    if day == "yesterday":
        today = date.today() - timedelta(days=1)
        index = 1
        day_index = 0
    else:
        today = date.today()
        index = 0
        day_index = 1

    cur_date = str(today.day) + "." + str(today.month)
    folder = f"data_{cur_date}"
    if not os.path.isdir(folder):
        os.mkdir(folder)
    collect_data(folder, index, day_index)
    transform_tables(folder)
    error = aggregate_data_for_future(folder)
    if error == "ok":
        print("Future games collected!")
        print(fence)
        resp = prepare_data(folder, day)
        if resp != "ok":
            print("No prepared data for training(")
        else:
            print("Data prepared for training!")
        print(fence)
    else:
        print("No games tomorrow(")
        print(fence)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--day",
        type=str,
        help="Choose for which day you want to collect results: yesterday or today",
        required=True,
    )
    args = parser.parse_args()
    run(args)
