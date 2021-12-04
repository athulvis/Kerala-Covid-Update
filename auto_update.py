from __future__ import print_function
import requests
from bs4 import BeautifulSoup 
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import time
from datetime import date

def authenticate():

    scopes = ['https://spreadsheets.google.com/feeds']
    #json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")

    #with open("token.json") as jsonfile:
        #creds_dict = json.load(jsonfile)
    json_creds = os.getenv("SHEETS_JSON")

    creds_dict = json.loads(json_creds)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    client = gspread.authorize(creds)
    
    return client


url = 'https://dashboard.kerala.gov.in/covid/daily.php'

def parse_data(url):
    out = requests.get(url)
    soup = BeautifulSoup(out.content, "html.parser")
    table = soup.find("table", attrs={'class':'table-sm'})
    rows = table.find_all('tr')
    data = {}
    for i in rows:
        table_data = i.findAll('td')
        td_data = [j.text for j in table_data]
        if len(td_data) > 0:
            data[td_data[0]] = td_data[1]
    return data
            
            
data = parse_data(url)

    
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)  
    
client = authenticate()
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1xy-YHgV---nLd344Zn93lx99dkgb1Sbbq5XhixKGwJs/edit#gid=0")
sheet = spreadsheet.sheet1  
#rows = sheet.get_all_records()
#print(sheet.row_values(1))

next_row = next_available_row(sheet)
sheet.update_acell("A{}".format(next_row), str(date.today()))
sheet.update_acell("B{}".format(next_row), data["Total"])
sheet.update_acell("C{}".format(next_row), data["Thiruvananthapuram"])
sheet.update_acell("D{}".format(next_row), data["Kollam"])
sheet.update_acell("E{}".format(next_row), data["Pathanamthitta"])
sheet.update_acell("F{}".format(next_row), data["Alappuzha"])
sheet.update_acell("G{}".format(next_row), data["Kottayam"])
sheet.update_acell("H{}".format(next_row), data["Idukki"])
sheet.update_acell("I{}".format(next_row), data["Ernakulam"])
sheet.update_acell("J{}".format(next_row), data["Thrissur"])
sheet.update_acell("K{}".format(next_row), data["Palakkad"])
sheet.update_acell("L{}".format(next_row), data["Malappuram"])
sheet.update_acell("M{}".format(next_row), data["Kozhikode"])
sheet.update_acell("N{}".format(next_row), data["Wayanad"])
sheet.update_acell("O{}".format(next_row), data["Kannur"])
sheet.update_acell("P{}".format(next_row), data["Kasaragod"])

