import requests
import json
from dotenv import load_dotenv
from core import *

load_dotenv()

personDatabaseId = os.getenv('PERSON_DATABASE_ID') if not isTestMode() else os.getenv('TEST_PERSON_DATABASE_ID')

class Person:
    id = None
    name = None
    targetProperty = None
    targetDays = None
    currentCount = None

    def __init__(self, id, name, targetProperty, targetDays, currentCount):
        self.id = id
        self.name = name
        self.targetProperty = targetProperty
        self.targetDays = targetDays
        self.currentCount = currentCount

def getPersonList():
    print('Getting Person from Notion')
    url = (f"https://api.notion.com/v1/databases/{ personDatabaseId }/query")

    res = requests.request("POST", url, headers=getHeader())
    if res.status_code != 200:
        print('Failed to get Person from Notion')
        exit

    data = res.json()

    # PRINT DB TO DB.JSON FILE
    # with open('./db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False)

    personList = []
    for row in data['results']:
        # Create the Person List
        personList.append(Person(
            row['id'],
            row['properties']['Name']['title'][0]['text']['content'],
            row['properties']['TargetProperty']['select']['name'],
            row['properties']['TargetDays']['number'],
            row['properties']['CurrentCount']['number']
        ))
    
    print('Finished getting Person List')
    return personList

def updatePersonList(personList, dayList):
    for dayPerson in dayList[0].virtualConversation:
        for person in personList:            
            if dayPerson == person.name:
                person.currentCount = -1                
    return personList

def sendPersonWarnings(personList):
    for person in personList:
        person.currentCount += 1
        updatePerson(person)
        if person.currentCount >= person.targetDays:
            sendPersonEmail(person)

def updatePerson(person):
    url = (f"https://api.notion.com/v1/pages/{ person.id }")

    updatePageData = {
        "properties": {
            "CurrentCount": {
                "number": person.currentCount,
            },
        }
    }

    data = json.dumps(updatePageData)

    if getInsertToNotion():
        res = requests.request('PATCH', url, headers=getHeader(), data=data)
        if res.status_code == 200:
            print('Person successfully updated in Notion')
        else:
            print(f"ERROR updating Person in DB: { res.status_code }")
            print(res.text)

def sendPersonEmail(person):
    subject = f'Person Warning: { person.name }'

    body = f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1>{ person.name }</h1>
                <br>
                <h3>Days since { person.targetProperty }</h3>
                <p><b>{ person.currentCount }</b></p>
            </body>
        </html>
    """

    if getSendEmails():
        sendEmail(subject, body)