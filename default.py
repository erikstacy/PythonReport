from time import daylight
import requests, json
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
testMode = os.getenv('TESTMODE') == "ON"
dayDatabaseId = os.getenv('DAY_DATABASE_ID') if not testMode else os.getenv('TEST_DAY_DATABASE_ID')
dailyReportDatabaseId = os.getenv('DAILY_REPORT_DATABASE_ID') if not testMode else os.getenv('TEST_DAILY_REPORT_DATABASE_ID')
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

class Day:
    def __init__(self, day, rating, workedOut, meditated, bankAmount, investments):
        self.day = day
        self.rating = rating
        self.workedOut = workedOut
        self.meditated = meditated
        self.bankAmount = bankAmount
        self.investments = investments

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




def readDatabase(databaseId, headers):
    url = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", url, headers=headers)
    if res.status_code != 200:
        exit

    data = res.json()

    # PRINT DB TO DB.JSON FILE
    # with open('./db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False)

    daysList = []
    for row in data['results']:        
        daysList.append(Day(
            row['properties']['Day']['date']['start'],
            row['properties']['Rating']['number'],
            row['properties']['WorkedOut']['checkbox'],
            row['properties']['Meditated']['number'],
            row['properties']['BankAmount']['number'],
            row['properties']['Investing']['number']
        ))
    
    return daysList

def createReport(daysList):
    # Test Mode
    if testMode: print(f"TEST MODE ON")
    print('')

    # Init Daily Report
    dailyReport = DailyReport()

    # Date
    dailyReport.day = daysList[0].day
    print(f"Date: { dailyReport.day }")
    print('')

    # Bank Account
    dailyReport.bankAmount = daysList[0].bankAmount
    dailyReport.bankAmountGL = daysList[0].bankAmount - daysList[1].bankAmount
    print(f"Bank Amount: { dailyReport.bankAmount }")
    print(f"Gain/Loss: {dailyReport.bankAmountGL }")
    print('')

    # Investments
    dailyReport.investments = daysList[0].investments
    dailyReport.investmentsGL = daysList[0].investments - daysList[1].investments
    print(f"Investments: { dailyReport.investments }")
    print(f"Gain/Loss: {dailyReport.investmentsGL }")
    print('')

    # Workout
    dailyReport.workoutStreak = 0
    i = 0
    while daysList[i].workedOut != False:
        dailyReport.workoutStreak += 1
        i += 1
    if dailyReport.workoutStreak == 0:
        for day in daysList:
            if day.workedOut == True:
                dailyReport.lastWorkout = day.day
                break
    else:
        dailyReport.lastWorkout = daysList[0].day
    print(f"Workout Streak: { dailyReport.workoutStreak }")
    print(f"Last Work Out: {dailyReport.lastWorkout }")
    print('')

    # Meditation
    dailyReport.meditationStreak = 0
    i = 0
    while daysList[i].meditated != False:
        dailyReport.meditationStreak += 1
        i += 1
    if dailyReport.meditationStreak == 0:
        for day in daysList:
            if day.meditated > 0:
                dailyReport.lastMeditation = day.day
                break
    else:
        dailyReport.lastMeditation = daysList[0].day
    print(f"Mediation Streak: { dailyReport.meditationStreak }")
    print(f"Last Meditation: { dailyReport.lastMeditation }")
    print('')

    return dailyReport

def createPage(dailyReport, databaseId, headers):
    url = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": databaseId },
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
    res = requests.request('POST', url, headers=headers, data=data)
    if res.status_code == 200:
        print('Daily Report Wrote to DB')
        print('')
    else:
        print(f"ERROR writing Daily Report to DB: { res.status_code }")
        print(res.text)
        print('')

daysList = readDatabase(dayDatabaseId, headers)
dailyReport = createReport(daysList)
createPage(dailyReport, dailyReportDatabaseId, headers)