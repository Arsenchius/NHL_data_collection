import requests
import pandas as pd


def main():
    # overall_table:
    feed_table = "to_jZ2mBfIs_jkdXuB14_1"
    feed_table_home = "to_jZ2mBfIs_jkdXuB14_2"
    feed_table_guest = "to_jZ2mBfIs_jkdXuB14_3"
    url_table = f"https://d.flashscorekz.com/x/feed/{feed_table}"
    url_home = f"https://d.flashscorekz.com/x/feed/{feed_table_home}"
    url_guest = f"https://d.flashscorekz.com/x/feed/{feed_table_guest}"
    data_table = requests.get(
        url=url_table, headers={"x-fsign": "SW9D1eZo"}
    ).text.split(sep="¬")
    data_home = requests.get(url=url_home, headers={"x-fsign": "SW9D1eZo"}).text.split(
        sep="¬"
    )
    data_guest = requests.get(
        url=url_guest, headers={"x-fsign": "SW9D1eZo"}
    ).text.split(sep="¬")
    block_data_table = [{}]
    block_data_home = [{}]
    block_data_guest = [{}]
    for item in data_table:
        key = item.split(sep="÷")[0]
        val = item.split(sep="÷")[-1]
        if "~" in key:
            block_data_table.append({key: val})
        else:
            block_data_table[-1].update({key: val})
    for item in data_home[:100]:
        key = item.split(sep="÷")[0]
        val = item.split(sep="÷")[-1]
        if "~" in key:
            block_data_home.append({key: val})
        else:
            block_data_home[-1].update({key: val})
    for item in data_guest:
        key = item.split(sep="÷")[0]
        val = item.split(sep="÷")[-1]
        if "~" in key:
            block_data_guest.append({key: val})
        else:
            block_data_guest[-1].update({key: val})
    for block in block_data_home:
        print(block)
    # column_names = ['team', 'pos', 'tm', 'tw', 'twr', 'two', 'tl', 'tlr', 'tlo', 'sg', 'cg', 'tp', 'division']
    # table_info = []
    # curr_division = ""
    # for block in block_data:
    #     if 'TC' in block.keys():
    #         if block.get('TC') == 'Западная конференция':
    #             curr_division = 'West'
    #         elif block.get('TC') == 'Восточная конференция':
    #             curr_division = 'East'
    #         else:
    #             curr_division = ''
    #     if curr_division in ['West', 'East']:
    #         if '~TR' in block.keys():
    #             table_info.append([block.get('TN'),
    #             int(block.get('~TR')),
    #             int(block.get('TM')),
    #             int(block.get('TW')),
    #             int(block.get('TWR')),
    #             int(block.get('TWO')),
    #             int(block.get('TL')),
    #             int(block.get('TLR')),
    #             int(block.get('TLO')),
    #             int(block.get('TG').split(':')[0]),
    #             int(block.get('TG').split(':')[-1]),
    #             int(block.get('TP')),
    #             curr_division])
    # print(block.keys())
    # print(block)

    # df = pd.DataFrame(table_info, columns = column_names)
    # print (df)
    # print(response.text)


if __name__ == "__main__":
    main()
