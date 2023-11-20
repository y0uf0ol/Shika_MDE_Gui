import os
import time
from art import logo
from create_app import client,hunt_client
import json
import pandas as pd
import requests

print(logo)



def ask_action():
    action = input("what do you want to do? (Alerts / Hunt / Live / Help) ").lower()
    return action


def helper():
    print("This is the Helper Page\nAlerts: will put you in the Alert overview and lets you select an alert you want to investigate\n"
          "Hunt: will give you the possibility to run KQL queries via direct or txt file input\n"
          "Live: lets you run the Live Response Module from MDE and push and run Powershell Scripts")


def alerts():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    pd.set_option('display.max_colwidth', None)
    # TODO model thid shit so it looks nice
    print("Here are the Alerts from today\n"
          "if you want to search for a specific one enter the ID\n"
          "if you want to go further back enter time (3d / 1w / 1m)")
    print("did not provide id here ist the list of the alerts")
    get_alerts = client().get("https://graph.microsoft.com/v1.0/security/alerts_v2").json()
    list=pd.DataFrame(get_alerts['value'])
    print(list.columns.to_list)
    print(list[['id','title','createdDateTime']])
    state = True
    while state == True:
        id = input("What alert do you want to investigate ? ")
        if id == "non":
            state = False
        get_alerts = client().get(f"https://graph.microsoft.com/v1.0/security/alerts_v2/{id}")
        alert_data = pd.DataFrame([get_alerts])
        print(alert_data)

def hunt():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    hunting_query=input("Enter the Kusto query you like to fire ")
    hunt=hunt_client(hunting_query)
    print(pd.DataFrame(hunt))

def respond():
    print("Enter the ClientID/Name you want to initiate a Live Response")


def shika():
    state = 0
    while state == 0:
        action = ask_action()
        if action == "exit":
            print("bye")
            state = 1

        if action == "reload":
            ##TODO 1 DONE clear screen and reload program
            os.system('clear')
        elif action == "help":
            helper()
        elif action == "alerts":
            alerts()
        elif action == "hunt":
            hunt()


shika()
# TODO 1 selection function umschreiben
# TODO 2 add Alert overview class
# TODO 3 add Hunt class
# TODO 4 Add Live Response mechanism with powershell scripts to run
# TODO 5 make it "huebschi"
# TODO 6 info screen with Help

