import requests
import json
import pandas as pd
from datetime import datetime


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


def parse_tables(header):
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


def parse_results(header):
    feed_table = "to_jZ2mBfIs_jkdXuB14_1"
    url = f"https://d.flashscorekz.com/x/feed/{feed_table}"
    response = requests.get(url=url, headers=header)
    data = response.text.split(sep="¬")
    block_data = [{}]
    for item in data:
        key = item.split(sep="÷")[0]
        val = item.split(sep="÷")[-1]

        if "~" in key:
            block_data.append({key: val})
        else:
            block_data[-1].update({key: val})

    for event in block_data:
        if "AA" in list(event.keys())[0]:
            date = datetime.fromtimestamp(int(event.get("AD")))
            team_1 = event.get("AE")
            team_2 = event.get("AF")
            score = f'{event.get("AG")}:{event.get("AH")}'
            print(date, team_1, team_2, score, sep=",")
        # result = game[]

        # print(json.dumps(event, ensure_ascii=False, indent=2))
        # print(all_leagues)

    # print(block_data)


def main():
    header = {"x-fsign": "SW9D1eZo"}
    parse_tables(header)
    # parse_results(header)


if __name__ == "__main__":
    main()
