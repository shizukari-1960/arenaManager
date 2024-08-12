##WIP##

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pymongo import MongoClient

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('E:\\VSC_workspace\\automaticUndertaker\\arena-save-9b32919f2536.json', scope)
client = gspread.authorize(creds)

ss_url = 'https://docs.google.com/spreadsheets/d/19cGIwV5GhOMDoHHoydSUkq1pB4U4L4Rvxh3ULSvdJ-E/edit'
spreadsheet = client.open_by_url(ss_url)
worksheet = spreadsheet.sheet1

worksheet.batch_get()

