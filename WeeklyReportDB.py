from distutils import core
from core import *
import requests
import json
from dotenv import load_dotenv

load_dotenv()

weeklyReportDatabaseId = os.getenv('WEEKLY_REPORT_DATABASE_ID') if not isTestMode() else os.getenv('TEST_WEEKLY_REPORT_DATABASE_ID')

class WeeklyReport:
    startDay = None
    endDay = None
    bankAmount = None
    bankAmountGL = None
    bankAmountHigh = None
    bankAmountLow = None
    investments = None
    investmentsGL = None
    investmentsHigh = None
    investmentsLow = None
    daysWorkedOut = None
    daysMeditated = None

    def insert(self):
        insertWeeklyReport(self)
        emailReport(self)

    def setValues(self, dayList):
        print('Start setting Weekly Report values')

        # Test Mode
        if isTestMode(): print(f"TEST MODE ON")

        # Start Day
        self.startDay = dayList[6].day
        print(f'Start Day: {self.startDay}')

        # End Day
        self.endDay = dayList[0].day
        print(f'End Day: {self.endDay}')

        # Bank Account
        self.bankAmount = dayList[0].bankAmount
        self.bankAmountGL = dayList[0].bankAmount - dayList[6].bankAmount        
        print(f"Bank Amount: { self.bankAmount }")
        print(f"Gain/Loss: {self.bankAmountGL }")
        
        for i in range(7):
            if i == 0:
                self.bankAmountHigh = dayList[i].bankAmount
                self.bankAmountLow = dayList[i].bankAmount
            else:
                if self.bankAmountHigh < dayList[i].bankAmount: self.bankAmountHigh = dayList[i].bankAmount
                if self.bankAmountLow > dayList[i].bankAmount: self.bankAmountLow = dayList[i].bankAmount
        print(f"Bank Amount High: {self.bankAmountHigh}")
        print(f"Bank Amount Low: {self.bankAmountLow}")

        # Investments
        self.investments = dayList[0].investments
        self.investmentsGL = dayList[0].investments - dayList[6].investments
        print(f"Investments: { self.investments }")
        print(f"Gain/Loss: {self.investmentsGL }")

        for i in range(7):
            if i == 0:
                self.investmentsHigh = dayList[i].investments
                self.investmentsLow = dayList[i].investments
            else:
                if self.investmentsHigh < dayList[i].investments: self.investmentsHigh = dayList[i].investments
                if self.investmentsLow > dayList[i].investments: self.investmentsLow = dayList[i].investments
        print(f"Investments High: {self.investmentsHigh}")
        print(f"Investments Low: {self.investmentsLow}")

        # Days Worked Out AND Days Meditated
        self.daysWorkedOut = 0
        self.daysMeditated = 0
        for i in range(7):
            if dayList[i].workedOut == True: self.daysWorkedOut += 1
            if dayList[i].meditated > 0: self.daysMeditated += 1
        print(f"Days Worked Out: {self.daysWorkedOut}/7")
        print(f"Days Meditated: {self.daysMeditated}/7")

        print('Weekly Report values set')

def insertWeeklyReport(weeklyReport):
    print('Start inserting Weekly Report to Notion')
    url = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": weeklyReportDatabaseId },
        "properties": {
            "StartDay": {
                "date": {
                    "start": weeklyReport.startDay,
                }
            },
            "EndDay": {
                "date": {
                    "start": weeklyReport.endDay,
                }
            },
            "BankAmount": {
                "number": weeklyReport.bankAmount,
            },
            "BankAmountGL": {
                "number": weeklyReport.bankAmountGL,
            },
            "BankAmountHigh": {
                "number": weeklyReport.bankAmountHigh,
            },
            "BankAmountLow": {
                "number": weeklyReport.bankAmountLow,
            },
            "Investments": {
                "number": weeklyReport.investments,
            },
            "InvestmentsGL": {
                "number": weeklyReport.investmentsGL,
            },
            "InvestmentsHigh": {
                "number": weeklyReport.investmentsHigh,
            },
            "InvestmentsLow": {
                "number": weeklyReport.investmentsLow,
            },
            "DaysWorkedOut": {
                "number": weeklyReport.daysWorkedOut,
            },
            "DaysMeditated": {
                "number": weeklyReport.daysMeditated,
            },
        }
    }

    data = json.dumps(newPageData)

    if getInsertToNotion():
        res = requests.request('POST', url, headers=getHeader(), data=data)
        if res.status_code == 200:
            print('Weekly Report successfully inserted to Notion')
        else:
            print(f"ERROR writing Weekly Report to DB: { res.status_code }")
            print(res.text)

def emailReport(weeklyReport):    
    subject = f'Weekly Report: { weeklyReport.startDay } - { weeklyReport.endDay }'

    body = f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1>{ weeklyReport.startDay } - { weeklyReport.endDay }</h1>
                <br>
                <h3>Bank Amount</h3>
                <p><b>{ weeklyReport.bankAmount }</b></p>
                <p>Gain/Loss: {weeklyReport.bankAmountGL }</p>
                <p>High: {weeklyReport.bankAmountHigh }</p>
                <p>Low: {weeklyReport.bankAmountLow }</p>
                <br>
                <h3>Investments</h3>
                <p><b>{ weeklyReport.investments }</b></p>
                <p>Gain/Loss: {weeklyReport.investmentsGL }</p>
                <p>High: {weeklyReport.investmentsHigh }</p>
                <p>Low: {weeklyReport.investmentsLow }</p>
                <br>
                <h3>Days Worked Out</h3>
                <p><b>{ weeklyReport.daysWorkedOut }/7</b></p>
                <br>
                <h3>Days Meditated</h3>
                <p><b>{ weeklyReport.daysMeditated }/7</b></p>
                <br>
            </body>
        </html>
    """

    if getSendEmails():
        sendEmail(subject, body)