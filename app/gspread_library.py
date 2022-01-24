import gspread
from oauth2client.service_account import ServiceAccountCredentials
# import pprint
from operator import itemgetter

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials_path = 'secret/google-credentials.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)

def get_data_from_gsheet(url):
    workbook = gc.open_by_url(url)
    skins = workbook.sheet1.get_all_records()
    return skins