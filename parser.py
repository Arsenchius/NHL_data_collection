import os

os.environ["OMP_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["VECLIB_MAXIMUM_THREADS"] = "4"
os.environ["NUMEXPR_NUM_THREADS"] = "4"

import requests
import json
import pandas as pd
from datetime import datetime
from multiprocessing import Process


def get_block_data(data):
    block_data = [{}]
    for item in data:
        key = item.split(sep="÷")[0]
        val = item.split(sep="÷")[-1]
        if "~" in key:
            block_data.append({key: val})
        else:
            block_data[-1].update({key: val})

    return block_data


def get_table_data(block_data, name):
    column_names = [
        "team",
        "pos",
        "tm",
        "tw",
        "twr",
        "two",
        "tl",
        "tlr",
        "tlo",
        "sg",
        "cg",
        "tp",
        "division",
    ]
    table_info = []
    curr_division = ""
    for block in block_data:
        if "TC" in block.keys():
            if block.get("TC") == "Западная конференция":
                curr_division = "West"
            elif block.get("TC") == "Восточная конференция":
                curr_division = "East"
            else:
                curr_division = ""
        if curr_division in ["West", "East"]:
            if "~TR" in block.keys():
                table_info.append(
                    [
                        block.get("TN"),
                        int(block.get("~TR")),
                        int(block.get("TM")),
                        int(block.get("TW")),
                        int(block.get("TWR")),
                        int(block.get("TWO")),
                        int(block.get("TL")),
                        int(block.get("TLR")),
                        int(block.get("TLO")),
                        int(block.get("TG").split(":")[0]),
                        int(block.get("TG").split(":")[-1]),
                        int(block.get("TP")),
                        curr_division,
                    ]
                )

    df_table = pd.DataFrame(table_info, columns=column_names)
    df_table.to_json(name, orient="records")


def collect_tables(header):
    feed_table = "to_jZ2mBfIs_jkdXuB14_1"
    feed_table_home = "to_jZ2mBfIs_jkdXuB14_2"
    feed_table_guest = "to_jZ2mBfIs_jkdXuB14_3"

    url_table = f"https://d.flashscorekz.com/x/feed/{feed_table}"
    data_table = requests.get(url=url_table, headers=header).text.split(sep="¬")
    block_data_table = get_block_data(data_table)
    get_table_data(block_data_table, name="data/table.json")

    url_home = f"https://d.flashscorekz.com/x/feed/{feed_table_home}"
    data_home = requests.get(url=url_table, headers=header).text.split(sep="¬")
    block_data_home = get_block_data(data_home)
    get_table_data(block_data_home, name="data/table_home.json")

    url_guest = f"https://d.flashscorekz.com/x/feed/{feed_table_guest}"
    data_guest = requests.get(url=url_table, headers=header).text.split(sep="¬")
    block_data_guest = get_block_data(data_guest)
    get_table_data(block_data_guest, name="data/table_guest.json")


def collect_results(header, index):
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
    name = "data/results_" + str(index + 1) + ".json"
    df.to_json(name, orient="records")


def collect_data():
    header = {"x-fsign": "SW9D1eZo"}
    collect_tables(header)
    part_jobs = []
    for index in range(8):
        part_jobs.append(Process(target=collect_results, args=(header, index)))

    for job in part_jobs:
        job.start()

    for job in part_jobs:
        job.join()


if __name__ == "__main__":
    collect_data()
