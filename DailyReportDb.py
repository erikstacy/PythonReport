import requests
import json
import os
from dotenv import load_dotenv
from core import *

load_dotenv()

dailyReportDatabaseId = os.getenv('DAILY_REPORT_DATABASE_ID') if not isTestMode() else os.getenv('TEST_DAILY_REPORT_DATABASE_ID')

class DailyReport:
    day = None
    bankAmount = None
    bankAmountGL = None
    investments = None
    investmentsGL = None
    workoutStreak = None
    lastWorkout = None
    meditationStreak = None
    lastMeditation = None

    def insert(self):
        insertDailyReport(self)


def insertDailyReport(dailyReport):
    url = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": dailyReportDatabaseId },
        "properties": {
            "Day": {
                "date": {
                    "start": dailyReport.day,
                }
            },
            "BankAmount": {
                "number": dailyReport.bankAmount,
            },
            "BankAmountGL": {
                "number": dailyReport.bankAmountGL,
            },
            "Investments": {
                "number": dailyReport.investments,
            },
            "InvestmentsGL": {
                "number": dailyReport.investmentsGL,
            },
            "WorkoutStreak": {
                "number": dailyReport.workoutStreak,
            },
            "LastWorkout": {
                "date": {
                    "start": dailyReport.lastWorkout,
                }
            },
            "MeditationStreak": {
                "number": dailyReport.meditationStreak,
            },
            "LastMeditation": {
                "date": {
                    "start": dailyReport.lastMeditation,
                }
            },
        }
    }

    data = json.dumps(newPageData)
    res = requests.request('POST', url, headers=getHeader(), data=data)
    if res.status_code == 200:
        print('Daily Report Wrote to DB')
        print('')
    else:
        print(f"ERROR writing Daily Report to DB: { res.status_code }")
        print(res.text)
        print('')