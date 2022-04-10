from re import S
import subprocess
from mac_vendor_lookup import MacLookup
import datetime
import time
import json
import pyttsx3
import copy
import random

mac = MacLookup()

here_now = set()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    #if "danish" in voice.id:
    engine.setProperty('voice', 'mb-en1')
    engine.setProperty('rate', 50)
    #    "https://raw.githubusercontent.com/numediart/MBROLA-voices/master/data/en1/en1"

scan_IP = '10.0.0.0'
submask = 24
welcome_messages = [
        "How has your day been? Had any coffee today?",
        "Are you hungry? Halvor could probably make you something.",
        "You look like sparkling rose today.",
        "Hope you have a good time visiting!"
    ]
goodbye_messages = [
        "Please rate your guest on a scale from 1 to 10 in the app.",
        "Hope they were a good friend."
    ]

TIMEOUT_MINUTES = 1

try:
    with open('people.json', 'r') as file:
        entries = json.load(file)
except:
    entries = {}


def welcome_message(mac):
    if entries[mac]['name']:
        engine.say(" ")
        engine.say(f"Welcome, {entries[mac]['name']}")
        engine.say(random.choice(welcome_messages))
        

def goodbye_message(mac):
    if entries[mac]['name']:
        engine.say(" ")
        engine.say(f"Goodbye, {entries[mac]['name']}")
        engine.say(random.choice(goodbye_messages))
        

def scan(command):
    global here_now
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    lines = o.decode('ascii').split('\n')
    past_entries = copy.deepcopy(entries)
    for i,line in enumerate(lines[:-4]):
        if "Nmap scan report for" in line:
            ip = line[21:]
            mac = lines[i+2][13:30]
            if mac in entries.keys():
                entries[mac]['ip'] = ip
                entries[mac]['last_seen'] = time.time()
            else:
                entries[mac] = {'name': '','ip': ip, 'mac': mac, 'first_seen': time.time(), 'last_seen': time.time()}
            here_now.add(mac)

    for mac in entries.keys():
        if len(past_entries) and time.time() - entries[mac]['last_seen'] > 60*TIMEOUT_MINUTES and mac in here_now:
            goodbye_message(mac)
            here_now.remove(mac)
    for mac in here_now:
        if mac not in past_entries.keys() or time.time() - past_entries[mac]['last_seen'] > 60*TIMEOUT_MINUTES:
            welcome_message(mac)

def fetch_names():
    try:
        with open('people.json', 'r') as file:
            saved_entries = json.load(file)
            for entry in saved_entries:
                entries[entry]['name'] = saved_entries[entry]['name']
    except:
        pass

i = 0
while True:
    if i % 60 == 0:
        print(str(datetime.datetime.now()), "> Full scan")
        scan(['sudo', 'nmap', '-snP', scan_IP + '/' + str(submask)])
        fetch_names()
        with open('people.json', 'w') as file:
            json_data = json.dumps(entries, indent=4)
            file.write(json_data)
    else:
        print(str(datetime.datetime.now()), "> Regular scan")
        scan(['sudo', 'nmap', '-snP'] + [entry['ip'] for entry in entries.values()])

    if i % 5 == 0:
        print(str(datetime.datetime.now()), "> Updating names")
        fetch_names()
    engine.runAndWait()
    print(str(datetime.datetime.now()), "> Completed iteration")
    i += 1
    time.sleep(2)