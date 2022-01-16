import requests
import json
import os
from dotenv import load_dotenv
from core import *
from DayDb import *
from DailyReportDb import * 

load_dotenv()

dayList = getDayList()

# Test Mode
if isTestMode: print(f"TEST MODE ON")
print('')

# Init Daily Report
dailyReport = DailyReport()

# Date
dailyReport.day = dayList[0].day
print(f"Date: { dailyReport.day }")
print('')

# Bank Account
dailyReport.bankAmount = dayList[0].bankAmount
dailyReport.bankAmountGL = dayList[0].bankAmount - dayList[1].bankAmount
print(f"Bank Amount: { dailyReport.bankAmount }")
print(f"Gain/Loss: {dailyReport.bankAmountGL }")
print('')

# Investments
dailyReport.investments = dayList[0].investments
dailyReport.investmentsGL = dayList[0].investments - dayList[1].investments
print(f"Investments: { dailyReport.investments }")
print(f"Gain/Loss: {dailyReport.investmentsGL }")
print('')

# Workout
dailyReport.workoutStreak = 0
i = 0
while dayList[i].workedOut != False:
    dailyReport.workoutStreak += 1
    i += 1
if dailyReport.workoutStreak == 0:
    for day in dayList:
        if day.workedOut == True:
            dailyReport.lastWorkout = day.day
            break
else:
    dailyReport.lastWorkout = dayList[0].day
print(f"Workout Streak: { dailyReport.workoutStreak }")
print(f"Last Work Out: {dailyReport.lastWorkout }")
print('')

# Meditation
dailyReport.meditationStreak = 0
i = 0
while dayList[i].meditated != False:
    dailyReport.meditationStreak += 1
    i += 1
if dailyReport.meditationStreak == 0:
    for day in dayList:
        if day.meditated > 0:
            dailyReport.lastMeditation = day.day
            break
else:
    dailyReport.lastMeditation = dayList[0].day
print(f"Mediation Streak: { dailyReport.meditationStreak }")
print(f"Last Meditation: { dailyReport.lastMeditation }")
print('')

# Send Report
dailyReport.insert()