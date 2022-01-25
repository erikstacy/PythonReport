from datetime import date
import calendar
import requests
import json
import os
from dotenv import load_dotenv
from core import *

load_dotenv()

dayDatabaseId = os.getenv('DAY_DATABASE_ID') if not isTestMode() else os.getenv('TEST_DAY_DATABASE_ID')

class Day:
    def __init__(self, dayOfWeek, day, rating, workedOut, meditated, bankAmount, investments):
        self.dayOfWeek = dayOfWeek
        self.day = day
        self.rating = rating
        self.workedOut = workedOut
        self.meditated = meditated
        self.bankAmount = bankAmount
        self.investments = investments

def getDayList():
    printToConsole('Getting Day List from Notion')
    url = (f"https://api.notion.com/v1/databases/{ dayDatabaseId }/query")

    res = requests.request("POST", url, headers=getHeader())
    if res.status_code != 200:
        printToConsole('Failed to get Day List from Notion')
        exit

    data = res.json()

    # PRINT DB TO DB.JSON FILE
    # with open('./db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False)

    daysList = []
    for row in data['results']:        
        daysList.append(Day(
            row['properties']['DayOfWeek']['title'][0]['text']['content'],
            row['properties']['Day']['date']['start'],
            row['properties']['Rating']['number'],
            row['properties']['WorkedOut']['checkbox'],
            row['properties']['Meditated']['number'],
            row['properties']['BankAmount']['number'],
            row['properties']['Investing']['number']
        ))
    
    printToConsole('Finished getting Day List')
    return daysList

def insertNewDay():
    printToConsole('Start inserting New Day to Notion')
    url = 'https://api.notion.com/v1/pages'

    curr_date = date.today()

    newPageData = {
        "parent": { "database_id": dayDatabaseId },
        "properties": {
            "DayOfWeek": {
                "title": [
                    {
                        "text": {
                            "content": calendar.day_name[curr_date.weekday()],
                        }
                    }
                ]
            },
            "Day": {
                "date": {
                    "start": curr_date.strftime("%Y-%m-%d"),
                }
            },
            "Meditated": {
                "number": 0,
            },
        }
    }

    data = json.dumps(newPageData)
    res = requests.request('POST', url, headers=getHeader(), data=data)
    if res.status_code == 200:
        printToConsole('New Day successfully inserted to Notion')
    else:
        printToConsole(f"ERROR writing Day to DB: { res.status_code }")
        print(res.text)