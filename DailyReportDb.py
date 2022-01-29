import email
from xmlrpc.client import DateTime
import requests
import json
import os
from dotenv import load_dotenv
import datetime
from core import *

load_dotenv()

dailyReportDatabaseId = os.getenv('DAILY_REPORT_DATABASE_ID') if not isTestMode() else os.getenv('TEST_DAILY_REPORT_DATABASE_ID')

class DailyReport:
    dayOfWeek = None
    day = None
    bankAmount = None
    bankAmountGL = None
    investments = None
    investmentsGL = None
    workoutStreak = None
    lastWorkout = None
    meditationStreak = None
    lastMeditation = None
    daysUntilPayday = None
    daysSinceLastDate = None

    def insert(self):
        insertDailyReport(self)
        emailReport(self)
    
    def setValues(self, dayList):
        print('Start setting Daily Report values')
        # Test Mode
        if isTestMode(): print(f"TEST MODE ON")

        #Day Of Week
        self.dayOfWeek = dayList[0].dayOfWeek
        print(f'Day Of Week set to { self.dayOfWeek}')

        # Date
        self.day = dayList[0].day
        print(f"Date: { self.day }")

        # Bank Account
        self.bankAmount = dayList[0].bankAmount
        self.bankAmountGL = dayList[0].bankAmount - dayList[1].bankAmount
        print(f"Bank Amount: { self.bankAmount }")
        print(f"Gain/Loss: {self.bankAmountGL }")

        # Investments
        self.investments = dayList[0].investments
        self.investmentsGL = dayList[0].investments - dayList[1].investments
        print(f"Investments: { self.investments }")
        print(f"Gain/Loss: {self.investmentsGL }")


        # Workout
        self.workoutStreak = 0
        i = 0
        while dayList[i].workedOut != False:
            self.workoutStreak += 1
            i += 1
        if self.workoutStreak == 0:
            for day in dayList:
                if day.workedOut == True:
                    self.lastWorkout = day.day
                    break
        else:
            self.lastWorkout = dayList[0].day
        print(f"Workout Streak: { self.workoutStreak }")
        print(f"Last Work Out: {self.lastWorkout }")

        # Meditation
        self.meditationStreak = 0
        i = 0
        while dayList[i].meditated != False:
            self.meditationStreak += 1
            i += 1
        if self.meditationStreak == 0:
            for day in dayList:
                if day.meditated > 0:
                    self.lastMeditation = day.day
                    break
        else:
            self.lastMeditation = dayList[0].day
        print(f"Mediation Streak: { self.meditationStreak }")
        print(f"Last Meditation: { self.lastMeditation }")

        # Days Until Paycheck
        todayDay = int(dayList[0].date.strftime("%d"))
        todayMonth = int(dayList[0].date.strftime("%m"))
        if todayDay == 19 or todayDay == 4:
            self.daysUntilPayday = 0
            print(f"PAY DAY")
        elif todayDay < 19 and todayDay > 4:
            self.daysUntilPayday = (dayList[0].date.replace(day=19) - dayList[0].date).days
            print(f"Days until payday: { self.daysUntilPayday }")
        elif todayDay > 19 or todayDay < 4:
            self.daysUntilPayday = (dayList[0].date.replace(month=todayMonth + 1).replace(day=4) - dayList[0].date).days
            print(f"Days until payday: { self.daysUntilPayday }")

        # Days Since Last Date
        for day in dayList:
            if "Date" in day.eventsList:
                self.daysSinceLastDate = (dayList[0].date - day.date).days
                print(f"Last date was { self.daysSinceLastDate } days ago")
                break

        print('Daily Report values set')


def insertDailyReport(dailyReport):
    print('Start inserting Daily Report to Notion')
    url = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": dailyReportDatabaseId },
        "properties": {
            "DayOfWeek": {
                "title": [
                    {
                        "text": {
                            "content": dailyReport.dayOfWeek,
                        }
                    }
                ]
            },
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
            "DaysUntilPayday": {
                "number": dailyReport.daysUntilPayday,
            },
            "DaysSinceLastDate": {
                "number": dailyReport.daysSinceLastDate,
            },
        }
    }

    data = json.dumps(newPageData)

    if getInsertToNotion():
        res = requests.request('POST', url, headers=getHeader(), data=data)
        if res.status_code == 200:
            print('Daily Report successfully inserted to Notion')
        else:
            print(f"ERROR writing Daily Report to DB: { res.status_code }")
            print(res.text)

def emailReport(dailyReport):    
    subject = f'Daily Report: { dailyReport.day }'

    body = f"""\
        <!DOCTYPE html>
        <html>
            <body>                
                <div style="display: flex; justify-content: center; align-items: center;">
                    <p style="font-size: 30px;">{ dailyReport.day }</p>
                </div>
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <p style="font-size: 20px; font-weight: bold;">Days</p>
                    <div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s; border-radius: 5px; width: fit-content; margin: 10px 0;">
                        <div style="margin: 2px 16px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                            <p>Days Until Payday</p>
                            <p>{ dailyReport.daysUntilPayday }</p>
                        </div>                    
                    </div>  
                    <div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s; border-radius: 5px; width: fit-content; margin: 10px 0;">
                        <div style="margin: 2px 16px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                            <p>Days since last date</p>
                            <p>{ dailyReport.daysSinceLastDate }</p>
                        </div>                        
                    </div>
                    <p style="font-size: 20px; font-weight: bold;">Financial</p>
                    <div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s; border-radius: 5px; width: fit-content; margin: 10px 0;">
                        <div style="margin: 2px 16px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                            <p>Bank Amount</p>
                            <p>{ dailyReport.bankAmount }</p>
                            <p>Gain/Loss: { dailyReport.bankAmountGL }</p>
                        </div>                        
                    </div>
                    <div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s; border-radius: 5px; width: fit-content; margin: 10px 0;">
                        <div style="margin: 2px 16px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                            <p>Investments</p>
                            <p>{ dailyReport.investments }</p>
                            <p>Gain/Loss: { dailyReport.investmentsGL }</p>
                        </div>                    
                    </div>
                    <p style="font-size: 20px; font-weight: bold;">Health</p>
                    <div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s; border-radius: 5px; width: fit-content; margin: 10px 0;">
                        <div style="margin: 2px 16px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                            <p>Workout Streak</p>
                            <p>{ dailyReport.workoutStreak }</p>
                            <p>Last Workout: { dailyReport.lastWorkout }</p>
                        </div>                        
                    </div>
                    <div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s; border-radius: 5px; width: fit-content; margin: 10px 0;">
                        <div style="margin: 2px 16px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                            <p>Meditation Streak</p>
                            <p>{ dailyReport.meditationStreak }</p>
                            <p>Last Meditation: { dailyReport.lastMeditation }</p>
                        </div>                    
                    </div> 
                </div>                
            </body>
        </html>
    """

    if getSendEmails():
        sendEmail(subject, body)