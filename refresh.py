import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials



scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
         <PATH TO CREDENTIALS GO HERE>, scope)


def refresh_data():
    print("Starting refresh!")
    gc = gspread.authorize(credentials)

    wks = gc.open("Fall 2020 Grading").sheet1

    data = wks.get_all_values()
    headers = data.pop(0)

    wks2 = gc.open("Fall 2020 Application Responses").sheet1
    data2 = wks2.get_all_values()
    headers2 = data2.pop(0)

    grades = pd.DataFrame(data, columns=headers)
    apps = pd.DataFrame(data2, columns=headers2)

    grades.to_csv("grades.csv")
    apps.to_csv("apps.csv")
    print("Completed refresh!\n")
