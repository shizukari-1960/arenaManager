import gspread
import matplotlib.pyplot as plot
import os
import pymongo

import pymongo.collation
import pymongo.database

from pprint import pprint
from matplotlib import rcParams
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep

os.chdir(os.path.dirname(os.path.abspath(__file__)))
client = pymongo.MongoClient('mongodb://localhost:27017')
dblist = client.list_database_names()
db = client["chrDB"]
collection_list = sorted(db.list_collection_names(), key = lambda x: int(x.split('_')[1]))
collection_list.reverse()
print(collection_list)
newest_collection_name = collection_list[0]
newest_collection = db[newest_collection_name]

#-------------------------------------------DATA ZONE-------------------------------------------


def list_all_PL(db: pymongo.database.Database, col_name):
    collection = db[col_name]
    cursor = collection.find({}, {'player': 1, '_id': 0})
    return list({doc['player'] for doc in cursor if 'player' in doc})


def get_xp_by_PL(db: pymongo.database.Database):
    """
    輸出所有玩家在所有庫的XP總和。
    輸出Format:
    {
        players: [pl_list],
        COL_name: [
            [values],
            [chrCount]
        ]
    }
    """
    xp_totals = {}
    PL_list = list_all_PL(db, 'shitenkai_2504230000') #newest , todo.
    xp_totals['players'] = PL_list

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        xp_totals[collection_name] = [[],[]]
        
        for player in PL_list:
            ppl = [
                {'$match': {'player': f'{player}'}},
                {'$group': {'_id': None, 'total_XP': {'$sum': '$totalXP'}}}
            ]
            result = list(collection.aggregate(ppl))
            total_xp = result[0]['total_XP'] if result else 0

            chrCount = collection.count_documents({'player': f'{player}'})

            total_xp = total_xp - 3000 * chrCount

            xp_totals[collection_name][0].append(total_xp)
            xp_totals[collection_name][1].append(chrCount)
    
    return xp_totals

def get_values(value_name: str):
    """
    輸出所有資料的腳卡名稱與特定數值的對。
    輸出Format:
    [[player1, val1]...]
    """
    rt = []
    collection = newest_collection

    for doc in collection.find({}, {'name': 1, f'{value_name}': 1, '_id': 0}):
        name = doc.get('name')
        vals = doc.get(f'{value_name}')
        rt.append([name, vals])

    return rt






#-------------------------------------------UPDATE ZONE-------------------------------------------

def insert_columns_from_cell(sheet_name: str, start_cell: str, data_src: list, isCol: bool = False, credentials_path: str, spreadsheet_url: str):
    """
    從指定儲存格開始，以欄為單位插入多欄資料（支援 column-wise 結構，會自動轉置）。

    :param spreadsheet_url: Google 試算表的網址
    :param sheet_name: 要操作的工作表名稱
    :param start_cell: 起始儲存格，例如 "B3"
    :param column_data: 列優先的資料模式 列表
    :param isCol: 是否為列優先資料
    :param credentials_path: Google Service Account 的 JSON 憑證檔案路徑
    """
    # 設定 API scope 並授權
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)

    # 開啟試算表與工作表
    spreadsheet = client.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet(sheet_name)

    # 分析起始儲存格
    import re
    match = re.match(r"([A-Za-z]+)(\d+)", start_cell)
    if not match:
        raise ValueError("起始儲存格格式錯誤（例：B3）")

    start_col_letter, start_row = match.groups()
    start_row = int(start_row)
    start_col_index = col_letter_to_index(start_col_letter)

    # 將欄為主的資料轉為列為主的資料（轉置）
    if isCol:
        data_matrix = list(map(list, zip(*data_src)))  # 轉置為 column_data
    else:
        data_matrix = data_src
    # 計算終止儲存格
    num_rows = len(data_matrix)
    num_cols = len(data_matrix[0]) if num_rows > 0 else 0
    end_col_index = start_col_index + num_cols - 1
    end_col_letter = col_index_to_letter(end_col_index)
    end_row = start_row + num_rows - 1
    end_cell = f"{end_col_letter}{end_row}"

    # 建立儲存格範圍並寫入
    cell_range = f"{start_cell}:{end_cell}"
    worksheet.update(cell_range, data_matrix)


def col_letter_to_index(col_letter):
    """將 Excel 欄位字母轉換為 0-indexed 數字（A=0, B=1, ..., Z=25, AA=26, AB=27, ...）"""
    col_letter = col_letter.upper()
    result = 0
    for c in col_letter:
        result = result * 26 + (ord(c) - ord('A') + 1)
    return result - 1  # 改為 0-indexed


def col_index_to_letter(index):
    """將 0-indexed 欄位數字轉換為 Excel 字母"""
    index += 1  # 改為 1-indexed
    letters = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


#-------------------------------------------TEST ZONE-------------------------------------------

def unzip_xp_total(db: pymongo.database.Database ,xp_total_dict: dict):
    rt = []
    rt.append(xp_total_dict['players'])
    for collection_name in sorted(db.list_collection_names(), key = lambda x: int(x.split('_')[1])):
        rt.append(xp_total_dict[collection_name][0])
        rt.append(xp_total_dict[collection_name][1])
    return rt


#-------------------------------------------EXECUTE ZONE-------------------------------------------
def main():
    insert_columns_from_cell('Activity', 'A3', unzip_xp_total(db,get_xp_by_PL(db)),isCol=True) #XP-total Compare
    value_need = {
        'totalXP': 'totalXP',
        'totalMoney': 'totalMoney',
        'gr': 'growth',
        'reputation': 'reputation',
        'AGI': 'agi',
        'DEX': 'dex',
        'STR': 'str',
        'VIT': 'vit',
        'INT': 'int',
        'SPI': 'spi'
    }
    for key,value in value_need.items():
        insert_columns_from_cell(key, 'A2', get_values(value))
        sleep(2)
    

    
main()



