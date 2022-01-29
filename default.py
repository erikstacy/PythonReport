import requests
import json
import os
from dotenv import load_dotenv
from core import *
from DayDb import *
from DailyReportDb import *

load_dotenv()

print('Started Task')

dayList = getDayList()

dailyReport = DailyReport
dailyReport.setValues(dailyReport, dayList)
dailyReport.insert(dailyReport)

insertNewDay()

print('Task Completed')