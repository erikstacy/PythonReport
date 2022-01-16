import os
from dotenv import load_dotenv

load_dotenv()

def getHeader():
    return {
        "Authorization": "Bearer " + os.getenv('TOKEN'),
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16"
    }

def isTestMode():
    return os.getenv('TESTMODE') == 'ON'