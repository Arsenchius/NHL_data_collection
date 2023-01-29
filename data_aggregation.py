import pandas as pd
import numpy as np
from typing import List, Dict, NoReturn
import datetime


def get_block_data(data: List) -> List[Dict]:
    block_data = [{}]
    for item in data:
        key = item.split(sep="÷")[0]
        val = item.split(sep="÷")[-1]
        if "~" in key:
            block_data.append({key: val})
        else:
            block_data[-1].update({key: val})

    return block_data


def get_table_data(block_data: List[Dict], name: str) -> NoReturn:
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


def transform_tables(folder: str) -> NoReturn:
    table = pd.read_json(folder + "/table.json")
    overall_table = table.sort_values(by=["tp"], ascending=False).reset_index(drop=True)
    overall_table["pos"] = overall_table.index + 1
    overall_table["win_rate"] = overall_table["tw"] / overall_table["tm"]
    overall_table["lose_rate"] = overall_table["tl"] / overall_table["tm"]
    overall_table["win_rate_ft"] = overall_table["twr"] / overall_table["tw"]
    overall_table["lose_rate_ft"] = overall_table["tlr"] / overall_table["tl"]
    overall_table["tie_ft_rate"] = (
        overall_table["tw"]
        - overall_table["twr"]
        + overall_table["tl"]
        - overall_table["tlr"]
    ) / overall_table["tm"]
    overall_table["sg_per_game"] = overall_table["sg"] / overall_table["tm"]
    overall_table["cg_per_game"] = overall_table["cg"] / overall_table["tm"]
    overall_table = overall_table.drop(
        ["tm", "tw", "twr", "two", "tl", "tlr", "tlo", "division"], axis=1
    )
    overall_table.to_json(folder + "/table.json", orient="records")

    table_home = pd.read_json(folder + "/table_home.json")
    table_home["win_rate_home"] = table_home["tw"] / table_home["tm"]
    table_home["lose_rate_home"] = table_home["tl"] / table_home["tm"]
    table_home["sg_per_game_home"] = table_home["sg"] / table_home["tm"]
    table_home["cg_per_game_home"] = table_home["cg"] / table_home["tm"]
    table_home["tie_ft_rate_home"] = (
        table_home["tw"] - table_home["twr"] + table_home["tl"] - table_home["tlr"]
    ) / table_home["tm"]
    table_home = table_home.rename(
        columns={"sg": "sg_home", "cg": "cg_home", "tp": "tp_home"}
    )
    table_home = table_home.drop(
        ["pos", "tm", "tw", "twr", "two", "tl", "tlr", "tlo", "division"], axis=1
    )
    table_home.to_json(folder + "/table_home.json", orient="records")

    table_guest = pd.read_json(folder + "/table_guest.json")
    table_guest["win_rate_guest"] = table_guest["tw"] / table_guest["tm"]
    table_guest["lose_rate_guest"] = table_guest["tl"] / table_guest["tm"]
    table_guest["sg_per_game_guest"] = table_guest["sg"] / table_guest["tm"]
    table_guest["cg_per_game_guest"] = table_guest["cg"] / table_guest["tm"]
    table_guest["tie_ft_rate_guest"] = (
        table_guest["tw"] - table_guest["twr"] + table_guest["tl"] - table_guest["tlr"]
    ) / table_guest["tm"]
    table_guest = table_guest.rename(
        columns={"sg": "sg_guest", "cg": "cg_guest", "tp": "tp_guest"}
    )
    table_guest = table_guest.drop(
        ["pos", "tm", "tw", "twr", "two", "tl", "tlr", "tlo", "division"], axis=1
    )
    table_guest.to_json(folder + "/table_guest.json", orient="records")


def aggregate_data_for_future(folder: str) -> NoReturn:
    future_games = pd.read_json(folder + "/next_tour_games.json")
    overall_table = pd.read_json(folder + "/table.json")
    table_home = pd.read_json(folder + "/table_home.json")
    table_guest = pd.read_json(folder + "/table_guest.json")
    future_games = future_games.join(overall_table.set_index("team"), on="home_team")
    cols = {}
    for column in future_games.columns[3:]:
        cols[column] = "h_" + column
    future_games = future_games.rename(columns=cols)
    future_games = future_games.join(overall_table.set_index("team"), on="guest_team")
    for column in cols:
        temp = cols[column]
        cols[column] = "g" + temp[1:]
    future_games = future_games.rename(columns=cols)
    future_games = future_games.join(table_home.set_index("team"), on="home_team")
    future_games = future_games.join(table_guest.set_index("team"), on="guest_team")
    future_games.to_json(folder + "/next_tour_games.json", orient="records")


def prepare_data(folder: str) -> NoReturn:
    results_table = pd.read_json(folder + "/results_1.json")
    prev_day = datetime.datetime.today() - datetime.timedelta(days=1)
    prev_date = str(prev_day.day) + "." + str(prev_day.month)
    folder_prev = f"data_{prev_date}"
    tour_games = pd.read_json(folder_prev + "/next_tour_games.json")
    df = pd.merge(
        tour_games,
        results_table,
        left_on=["home_team", "guest_team", "date"],
        how="left",
        right_on=["home_team", "guest_team", "date"],
    )
    df["total>5.5"] = np.where(df["home_score"] + df["guest_score"] > 5.5, 1, 0)
    conditions = [
        df["home_score"] > df["guest_score"],
        df["home_score"] < df["guest_score"],
    ]
    choices = ["home", "guest"]
    df["winner"] = np.select(conditions, choices, default=None)
    df.to_json(f"training_data/{prev_date}.json", orient="records")
