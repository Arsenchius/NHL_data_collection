import requests
import pandas as pd
from datetime import datetime


def main():
    feed = "f_4_1_3_ru-kz_1"
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
    print(df)


if __name__ == "__main__":
    main()
