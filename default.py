import requests
import json
import os
from dotenv import load_dotenv
from WeeklyReportDB import WeeklyReport
from core import *
from DayDb import *
from DailyReportDb import *

load_dotenv()

print('Started Task')

dayList = getDayList()

dailyReport = DailyReport
dailyReport.setValues(dailyReport, dayList)
dailyReport.insert(dailyReport)

if dayList[0].dayOfWeek == 'Sunday':
    weeklyReport = WeeklyReport
    weeklyReport.setValues(weeklyReport, dayList)
    weeklyReport.insert(weeklyReport)

insertNewDay()

print('Task Completed')