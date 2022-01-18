import this
import requests
import json
import os
from dotenv import load_dotenv
from core import *
from DayDb import *
from DailyReportDb import * 

load_dotenv()

printToConsole('Started Task')

dayList = getDayList()

dailyReport = DailyReport
dailyReport.setValues(this, dayList)
dailyReport.insert(this)

printToConsole('Task Completed')