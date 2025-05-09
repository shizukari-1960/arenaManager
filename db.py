import pymongo
import copy
import os
import pprint
import sys
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import time
#INIT

os.chdir(os.path.dirname(os.path.abspath(__file__)))
client = pymongo.MongoClient('mongodb://localhost:27017')
dblist = client.list_database_names()
db = client["chrDB"]
collection = db["shitenkai_2504230000"]



SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file("arena-save-9b32919f2536.json",scopes=SCOPES)
gcli = gspread.authorize(creds)
main_sheet = gcli.open_by_key("").sheet1

default_ChrFormat = {
    "name" : "",
    "player" : "",
    "race" : "",
    "gender" : "",
    "belief" : "",
    "level" : 1,
    "soulScar" : 0,
    "totalXP" : 3000,
    "totalMoney" : 0,
    "growth" : 0,
    "adRank" : "",
    "reputation" : 0,
    "dex" : 0,
    "agi" : 0,
    "str" : 0,
    "vit" : 0,
    "int" : 0,
    "spi" : 0,
    "HP" : 0,
    "MP" : 0,
    "battleSkills": {
        "dancer" : "",
        "lvl1" : "",
        "lvl3" : "",
        "lvl5" : "",
        "lvl7" : "",
        "lvl9" : "",
        "lvl11" : "",
        "lvl13" : "",
        "lvl15" : "",
        "sup16" : "",
        "sup17" : ""
    }
}
address_collect = {
    "8.2":{
        "name" : "B31",
        "player" : "B28",
        "race" : "E33",
        "gender" : "E35",
        "belief" : "E36",
        "level" : "AM5",
        "soulScar" : "N39",
        "totalXP" : "AM14",
        "usedXP": "AM18",
        "totalMoney" : "AF16",
        "growth" : "AI12",
        "adRank" : "AC122",
        "reputation" : "AX124",
        "dex" : "AA4",
        "agi" : "AA7",
        "str" : "AA10",
        "vit" : "AA13",
        "int" : "AA16",
        "spi" : "AA19",
        "HP" : "AF4",
        "MP" : "AI4",
        "battleSkills": {
            "dancer" : "BD8",
            "lvl1" : "BD13",
            "lvl3" : "BD16",
            "lvl5" : "BD19",
            "lvl7" : "BD22",
            "lvl9" : "BD25",
            "lvl11" : "BD28",
            "lvl13" : "BD31",
            "lvl15" : "BD34",
            "sup16" : "BD40",
            "sup17" : "BD43"
        }
    },
    "8.3":{
        "name" : "B33",
        "player" : "B30",
        "race" : "E35",
        "gender" : "E37",
        "belief" : "E38",
        "level" : "AM5",
        "soulScar" : "N41",
        "totalXP" : "AM14",
        "usedXP": "AM18",
        "totalMoney" : "AF16",
        "growth" : "AI12",
        "adRank" : "AC124",
        "reputation" : "AX126",
        "dex" : "AA4",
        "agi" : "AA7",
        "str" : "AA10",
        "vit" : "AA13",
        "int" : "AA16",
        "spi" : "AA19",
        "HP" : "AF4",
        "MP" : "AI4",
        "battleSkills": {
            "dancer" : "BD7",
            "lvl1" : "BD13",
            "lvl3" : "BD16",
            "lvl5" : "BD19",
            "lvl7" : "BD22",
            "lvl9" : "BD25",
            "lvl11" : "BD28",
            "lvl13" : "BD31",
            "lvl15" : "BD34",
            "sup16" : "BD42",
            "sup17" : "BD45"
        }
    },
    "9.0":{
        "name" : "AG6",
        "player" : "W6",
        "race" : "Z8",
        "gender" : "AF13",
        "belief" : "Z10",
        "level" : "BE6",
        "soulScar" : "AN15",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ265",
        "growth" : "BK6",
        "adRank" : "E158",
        "reputation" : "G168",
        "dex" : "O29",
        "agi" : "O32",
        "str" : "O35",
        "vit" : "O38",
        "int" : "O41",
        "spi" : "O44",
        "HP" : "R50",
        "MP" : "R52",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "9.2":{
        "name" : "AG6",
        "player" : "W6",
        "race" : "Z8",
        "gender" : "AF13",
        "belief" : "Z10",
        "level" : "BE6",
        "soulScar" : "AN15",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ265",
        "growth" : "BK6",
        "adRank" : "E158",
        "reputation" : "G168",
        "dex" : "O29",
        "agi" : "O32",
        "str" : "O35",
        "vit" : "O38",
        "int" : "O41",
        "spi" : "O44",
        "HP" : "R50",
        "MP" : "R52",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "9.3":{
        "name" : "AG6",
        "player" : "W6",
        "race" : "Z8",
        "gender" : "AF13",
        "belief" : "Z10",
        "level" : "BE6",
        "soulScar" : "AN15",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ265",
        "growth" : "BK6",
        "adRank" : "E158",
        "reputation" : "G168",
        "dex" : "O29",
        "agi" : "O32",
        "str" : "O35",
        "vit" : "O38",
        "int" : "O41",
        "spi" : "O44",
        "HP" : "R50",
        "MP" : "R52",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "9.4":{
        "name" : "AG6",
        "player" : "W6",
        "race" : "Z8",
        "gender" : "AF13",
        "belief" : "Z10",
        "level" : "BE6",
        "soulScar" : "AN15",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ265",
        "growth" : "BK6",
        "adRank" : "E158",
        "reputation" : "G168",
        "dex" : "O29",
        "agi" : "O32",
        "str" : "O35",
        "vit" : "O38",
        "int" : "O41",
        "spi" : "O44",
        "HP" : "R50",
        "MP" : "R52",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "9.5":{
        "name" : "L5",
        "player" : "B5",
        "race" : "E7",
        "gender" : "K12",
        "belief" : "E9",
        "level" : "BE6",
        "soulScar" : "S14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ265",
        "growth" : "S38",
        "adRank" : "E158",
        "reputation" : "G168",
        "dex" : "P21",
        "agi" : "P24",
        "str" : "P27",
        "vit" : "P30",
        "int" : "P33",
        "spi" : "P36",
        "HP" : "R45",
        "MP" : "R47",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "9.6":{
        "name" : "L5",
        "player" : "B5",
        "race" : "E7",
        "gender" : "K12",
        "belief" : "E9",
        "level" : "BE6",
        "soulScar" : "S14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ265",
        "growth" : "S38",
        "adRank" : "E158",
        "reputation" : "G168",
        "dex" : "P21",
        "agi" : "P24",
        "str" : "P27",
        "vit" : "P30",
        "int" : "P33",
        "spi" : "P36",
        "HP" : "R45",
        "MP" : "R47",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "9.7":{
        "name" : "L5",
        "player" : "B5",
        "race" : "E7",
        "gender" : "K12",
        "belief" : "E9",
        "level" : "BE6",
        "soulScar" : "S14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ265",
        "growth" : "S38",
        "adRank" : "E158",
        "reputation" : "G168",
        "dex" : "P21",
        "agi" : "P24",
        "str" : "P27",
        "vit" : "P30",
        "int" : "P33",
        "spi" : "P36",
        "HP" : "R45",
        "MP" : "R47",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "9.8":{
        "name" : "L5",
        "player" : "B5",
        "race" : "E7",
        "gender" : "K12",
        "belief" : "E9",
        "level" : "BE6",
        "soulScar" : "S14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ273",
        "growth" : "S38",
        "adRank" : "E160",
        "reputation" : "G170",
        "dex" : "P21",
        "agi" : "P24",
        "str" : "P27",
        "vit" : "P30",
        "int" : "P33",
        "spi" : "P36",
        "HP" : "R45",
        "MP" : "R47",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "10.0":{
        "name" : "L5",
        "player" : "B5",
        "race" : "E7",
        "gender" : "K12",
        "belief" : "E9",
        "level" : "BE6",
        "soulScar" : "S14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ294",
        "growth" : "S38",
        "adRank" : "E160",
        "reputation" : "G170",
        "dex" : "P21",
        "agi" : "P24",
        "str" : "P27",
        "vit" : "P30",
        "int" : "P33",
        "spi" : "P36",
        "HP" : "R45",
        "MP" : "R47",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "10.1":{
        "name" : "L5",
        "player" : "B5",
        "race" : "E7",
        "gender" : "K12",
        "belief" : "E9",
        "level" : "BE6",
        "soulScar" : "S14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ296",
        "growth" : "S38",
        "adRank" : "E160",
        "reputation" : "G170",
        "dex" : "P21",
        "agi" : "P24",
        "str" : "P27",
        "vit" : "P30",
        "int" : "P33",
        "spi" : "P36",
        "HP" : "R45",
        "MP" : "R47",
        "battleSkills": {
            "dancer" : "D97",
            "lvl1" : "D82",
            "lvl3" : "D85",
            "lvl5" : "D88",
            "lvl7" : "D91",
            "lvl9" : "Q82",
            "lvl11" : "Q85",
            "lvl13" : "Q88",
            "lvl15" : "Q91",
            "sup16" : "Q97",
            "sup17" : "Q100"
        }
    },
    "10.9":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ308",
        "growth" : "BK6",
        "adRank" : "E174",
        "reputation" : "G184",
        "dex" : "S45",
        "agi" : "S48",
        "str" : "S51",
        "vit" : "S54",
        "int" : "S57",
        "spi" : "S60",
        "HP" : "AL46",
        "MP" : "AL48",
        "battleSkills": {
            "dancer" : "D109",
            "lvl1" : "D94",
            "lvl3" : "D97",
            "lvl5" : "D100",
            "lvl7" : "D103",
            "lvl9" : "Q94",
            "lvl11" : "Q97",
            "lvl13" : "Q100",
            "lvl15" : "Q103",
            "sup16" : "Q109",
            "sup17" : "Q112"
        }
    },
    "11.4":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ388",
        "growth" : "AA62",
        "adRank" : "E234",
        "reputation" : "G244",
        "dex" : "S45",
        "agi" : "S48",
        "str" : "S51",
        "vit" : "S54",
        "int" : "S57",
        "spi" : "S60",
        "HP" : "AN44",
        "MP" : "AN47",
        "battleSkills": {
            "dancer" : "Q116",
            "lvl1" : "D116",
            "lvl3" : "D119",
            "lvl5" : "D122",
            "lvl7" : "D125",
            "lvl9" : "D128",
            "lvl11" : "D131",
            "lvl13" : "D134",
            "lvl15" : "D137",
            "sup16" : "Q122",
            "sup17" : "Q125"
        }
    },
    "12.2":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ433",
        "growth" : "AA64",
        "adRank" : "F269",
        "reputation" : "G262",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q116",
            "lvl1" : "D116",
            "lvl3" : "D119",
            "lvl5" : "D122",
            "lvl7" : "D125",
            "lvl9" : "D128",
            "lvl11" : "D131",
            "lvl13" : "D134",
            "lvl15" : "D137",
            "sup16" : "Q122",
            "sup17" : "Q125"
        }
    },
    "12.3":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ455",
        "growth" : "AA64",
        "adRank" : "F278",
        "reputation" : "G268",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q116",
            "lvl1" : "D116",
            "lvl3" : "D119",
            "lvl5" : "D122",
            "lvl7" : "D125",
            "lvl9" : "D128",
            "lvl11" : "D131",
            "lvl13" : "D134",
            "lvl15" : "D137",
            "sup16" : "Q122",
            "sup17" : "Q125"
        }
    },
    "12.4":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ448",
        "growth" : "AA64",
        "adRank" : "F270",
        "reputation" : "G262",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q116",
            "lvl1" : "D116",
            "lvl3" : "D119",
            "lvl5" : "D122",
            "lvl7" : "D125",
            "lvl9" : "D128",
            "lvl11" : "D131",
            "lvl13" : "D134",
            "lvl15" : "D137",
            "sup16" : "Q122",
            "sup17" : "Q125"
        }
    },
    "12.5":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ448",
        "growth" : "AA64",
        "adRank" : "F270",
        "reputation" : "G262",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q116",
            "lvl1" : "D116",
            "lvl3" : "D119",
            "lvl5" : "D122",
            "lvl7" : "D125",
            "lvl9" : "D128",
            "lvl11" : "D131",
            "lvl13" : "D134",
            "lvl15" : "D137",
            "sup16" : "Q122",
            "sup17" : "Q125"
        }
    },
    "12.6":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ462",
        "growth" : "AA64",
        "adRank" : "F284",
        "reputation" : "G276",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q116",
            "lvl1" : "D116",
            "lvl3" : "D119",
            "lvl5" : "D122",
            "lvl7" : "D125",
            "lvl9" : "D128",
            "lvl11" : "D131",
            "lvl13" : "D134",
            "lvl15" : "D137",
            "sup16" : "Q122",
            "sup17" : "Q125"
        }
    },
    "12.8":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ752",
        "growth" : "AA64",
        "adRank" : "F574",
        "reputation" : "G566",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q117",
            "lvl1" : "D117",
            "lvl3" : "D120",
            "lvl5" : "D123",
            "lvl7" : "D126",
            "lvl9" : "D129",
            "lvl11" : "D132",
            "lvl13" : "D135",
            "lvl15" : "D138",
            "sup16" : "Q123",
            "sup17" : "Q126"
        }
    },
    "12.9":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ773",
        "growth" : "AA64",
        "adRank" : "F595",
        "reputation" : "G587",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q117",
            "lvl1" : "D117",
            "lvl3" : "D120",
            "lvl5" : "D123",
            "lvl7" : "D126",
            "lvl9" : "D129",
            "lvl11" : "D132",
            "lvl13" : "D135",
            "lvl15" : "D138",
            "sup16" : "Q123",
            "sup17" : "Q126"
        }
    },
    "13.0":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ773",
        "growth" : "AA64",
        "adRank" : "F595",
        "reputation" : "G587",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q117",
            "lvl1" : "D117",
            "lvl3" : "D120",
            "lvl5" : "D123",
            "lvl7" : "D126",
            "lvl9" : "D129",
            "lvl11" : "D132",
            "lvl13" : "D135",
            "lvl15" : "D138",
            "sup16" : "Q123",
            "sup17" : "Q126"
        }
    },
    "13.1":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BK10",
        "usedXP" : "BE14",
        "totalMoney" : "BJ773",
        "growth" : "AA64",
        "adRank" : "F595",#UK
        "reputation" : "G587",#UK
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q117",
            "lvl1" : "D117",
            "lvl3" : "D120",
            "lvl5" : "D123",
            "lvl7" : "D126",
            "lvl9" : "D129",
            "lvl11" : "D132",
            "lvl13" : "D135",
            "lvl15" : "D138",
            "sup16" : "Q123",
            "sup17" : "Q126"
        }
    },
    "13.4":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BJ6",
        "usedXP" : "BJ8",
        "totalMoney" : "BJ773",
        "growth" : "AA64",
        "adRank" : "F595",
        "reputation" : "G587",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q117",
            "lvl1" : "D117",
            "lvl3" : "D120",
            "lvl5" : "D123",
            "lvl7" : "D126",
            "lvl9" : "D129",
            "lvl11" : "D132",
            "lvl13" : "D135",
            "lvl15" : "D138",
            "sup16" : "Q123",
            "sup17" : "Q126"
        }
    },
    "13.5":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BJ6",
        "usedXP" : "BJ8",
        "totalMoney" : "BJ918",
        "growth" : "AA64",
        "adRank" : "F740",
        "reputation" : "G732",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q134",
            "lvl1" : "D134",
            "lvl3" : "D137",
            "lvl5" : "D140",
            "lvl7" : "D143",
            "lvl9" : "D146",
            "lvl11" : "D149",
            "lvl13" : "D152",
            "lvl15" : "D155",
            "sup16" : "Q140",
            "sup17" : "Q143"
        }
    },
    "13.8":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BJ6",
        "usedXP" : "BJ8",
        "totalMoney" : "BJ1033",
        "growth" : "AA64",
        "adRank" : "F810",
        "reputation" : "G802",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q134",
            "lvl1" : "D134",
            "lvl3" : "D137",
            "lvl5" : "D140",
            "lvl7" : "D143",
            "lvl9" : "D146",
            "lvl11" : "D149",
            "lvl13" : "D152",
            "lvl15" : "D155",
            "sup16" : "Q140",
            "sup17" : "Q143"
        }
    },
    "13.9":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BE6",
        "soulScar" : "AN14",
        "totalXP" : "BJ6",
        "usedXP" : "BJ8",
        "totalMoney" : "BJ1033",
        "growth" : "AA64",
        "adRank" : "F810",
        "reputation" : "G802",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q134",
            "lvl1" : "D134",
            "lvl3" : "D137",
            "lvl5" : "D140",
            "lvl7" : "D143",
            "lvl9" : "D146",
            "lvl11" : "D149",
            "lvl13" : "D152",
            "lvl15" : "D155",
            "sup16" : "Q140",
            "sup17" : "Q143"
        }
    },
    "13.91":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BJ4",
        "soulScar" : "AN14",
        "totalXP" : "BJ6",
        "usedXP" : "BJ8",
        "totalMoney" : "BJ1033",
        "growth" : "AA64",
        "adRank" : "F810",
        "reputation" : "G802",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q134",
            "lvl1" : "D134",
            "lvl3" : "D137",
            "lvl5" : "D140",
            "lvl7" : "D143",
            "lvl9" : "D146",
            "lvl11" : "D149",
            "lvl13" : "D152",
            "lvl15" : "D155",
            "sup16" : "Q140",
            "sup17" : "Q143"
        }
    },
    "13.92":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BJ4",
        "soulScar" : "AN14",
        "totalXP" : "BJ6",
        "usedXP" : "BJ8",
        "totalMoney" : "BJ1033",
        "growth" : "AA64",
        "adRank" : "F810",
        "reputation" : "G802",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q134",
            "lvl1" : "D134",
            "lvl3" : "D137",
            "lvl5" : "D140",
            "lvl7" : "D143",
            "lvl9" : "D146",
            "lvl11" : "D149",
            "lvl13" : "D152",
            "lvl15" : "D155",
            "sup16" : "Q140",
            "sup17" : "Q143"
        }
    },
    "13.93":{
        "name" : "AG5",
        "player" : "W5",
        "race" : "Z7",
        "gender" : "AF12",
        "belief" : "Z9",
        "level" : "BJ4",
        "soulScar" : "AN14",
        "totalXP" : "BJ6",
        "usedXP" : "BJ8",
        "totalMoney" : "BJ1033",
        "growth" : "AA64",
        "adRank" : "F810",
        "reputation" : "G802",
        "dex" : "S47",
        "agi" : "S50",
        "str" : "S53",
        "vit" : "S56",
        "int" : "S59",
        "spi" : "S62",
        "HP" : "AN46",
        "MP" : "AN49",
        "battleSkills": {
            "dancer" : "Q134",
            "lvl1" : "D134",
            "lvl3" : "D137",
            "lvl5" : "D140",
            "lvl7" : "D143",
            "lvl9" : "D146",
            "lvl11" : "D149",
            "lvl13" : "D152",
            "lvl15" : "D155",
            "sup16" : "Q140",
            "sup17" : "Q143"
        }
    }
}

def addr_extract(addr:dict):
    repl = []
    for k,v in addr.items():
        if k == "battleSkills":
            for kb,vb in v.items():
                repl.append(vb)
        else:
            repl.append(v)
    return repl

def fetch_vals(vals:dict ,addr_dict:dict ):
    #addr[stats:addr]
    #vals[addr:vals]
    rt = {}
    for stats,addr in addr_dict.items():
        if stats != "battleSkills":
            rt[stats] = vals[addr][0][0] if vals[addr] else ''
        else:
            rt["battleSkills"] = {}
            for skil,addr in addr_dict['battleSkills'].items():
                rt["battleSkills"][skil] = vals[addr][0][0] if vals[addr] else ''
    return rt

def getChrInfo(url):

    try:
        ver = checkVer(url)
        sheet = gcli.open_by_url(url)
        worksheet = sheet.worksheet(title=f'空白角色紙v{ver}')
    except Exception as e:
        print(sys.exc_info())
        info = "BAD URL"
        print("Load Failed.")
        
        return info
    
    worksheet:gspread.worksheet.Worksheet
    info = copy.deepcopy(default_ChrFormat)
    req = []
    req = addr_extract(address_collect[f'{ver}'])
    raw_vals = worksheet.batch_get(req)
    val_dict = dict(map(lambda x,y:[x,y],req,raw_vals))
    info = fetch_vals(val_dict,address_collect[ver])
    print(f'{info["name"]} by {info["player"]} loaded.')
    quanti(info)
    return info

def quanti(info:dict):
    for k,v in info.items():
        if k != 'battleSkills':
            if v.isdigit():
                info[k] = int(v)
    
    return info


def checkVer(url):
    sheet = gcli.open_by_url(url)
    wslist = []
    for i in sheet.worksheets():
        wslist.append(i.title)
    interval1 = []
    result = []
    
    for i in range(len(wslist)):
        if "空白角色紙" in wslist[i]:
            interval1.append(wslist[i])
    #print(interval1)
    for i in range(len(interval1)):
        if "(" not in interval1[i]:
            result.append(interval1[i])
    
    
    rt = result[0].split("v")
    #print(rt)
    return rt[1]



def main():
    urlList = main_sheet.get_values('P263:P587') #107
    print(urlList)
    for i in urlList:
        url = i[0]
        updateInfo(url)
        time.sleep(1.5)


    #target = collection.find_one({},{
        #"name" : name,
        #"player" : player
    #})
    #print(target)
    #print(target == None)

def updateInfo(url):
    global collection
    info = getChrInfo(url)
    if info == "BAD URL":
        return
    
    info['player'] = str(info["player"])
    info['update-at'] = datetime.utcnow()
    
    x = collection.insert_one(info)
    print(x)

main()


