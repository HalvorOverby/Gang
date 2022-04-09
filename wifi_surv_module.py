from re import S
import subprocess
from mac_vendor_lookup import MacLookup
import datetime
import time
import json
import os

mac = MacLookup()

here_now = set()


#mac.update_vendors()
scan_IP = '10.0.0.0'
submask = 24
try:
    with open('people.json', 'r') as file:
        entries = json.load(file)
except:
    entries = {}


def welcome_message(mac):
    if entries[mac]['name']:
        subprocess.Popen(['festival', "-b", f"""'(voice_cmu_us_slt_arctic_hts)' \\ '(SayText "Welcome, {entries[mac]['name']}")'"""])

def goodbye_message(mac):
    if entries[mac]['name']:
        subprocess.Popen(['festival', "-b", f"""'(voice_cmu_us_slt_arctic_hts)' \\ '(SayText "Goodbye, {entries[mac]['name']}")'"""])


def update_macs():
    global here_now
    command = ['sudo', 'nmap', '-snP', scan_IP + '/' + str(submask)]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    o, e = proc.communicate()

    lines = o.decode('ascii').split('\n')
    here_right_now = set()
    for i,line in enumerate(lines[:-4]):
        if "Nmap scan report for" in line:
            ip = line[20:]
            mac = lines[i+2][13:30]
            if mac in entries.keys():
                entries[mac]['ip'] = ip
                entries[mac]['last_seen'] = str(datetime.datetime.now())
            else:
                entries[mac] = {'name': '','ip': ip, 'mac': mac, 'first_seen': str(datetime.datetime.now()), 'last_seen': str(datetime.datetime.now())}
                try:
                    entries[mac]['vendor'] = mac.lookup(mac)
                except:
                    entries[mac]['vendor'] = 'Unknown'
            here_right_now.add(mac)
    for mac in here_right_now.difference(here_now):
        welcome_message(mac)
    for mac in here_now.difference(here_right_now):
        goodbye_message(mac)
    here_now = here_right_now.copy()


i = 0
while True:
    if i % 1 == 0:
        with open('people.json', 'w') as file:
            json_data = json.dumps(entries, indent=4)
            file.write(json_data)
    update_macs()
    print(str(datetime.datetime.now()), ">")
    i += 1