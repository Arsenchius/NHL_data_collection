import requests
import pandas as pd
from datetime import datetime


def main():
    feed = "f_4_-7_3_ru-kz_1"
    url_table = f"https://d.flashscorekz.com/x/feed/{feed}"
    data_table = requests.get(
        url=url_table, headers={"x-fsign": "SW9D1eZo"}
    ).text.split(sep="¬")
    block_data_table = [{}]
    for item in data_table:
        key = item.split(sep="÷")[0]
        val = item.split(sep="÷")[-1]
        if "~" in key:
            block_data_table.append({key: val})
        else:
            block_data_table[-1].update({key: val})
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
    print(df)


if __name__ == "__main__":
    main()
