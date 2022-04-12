import subprocess
from mac_vendor_lookup import MacLookup
import datetime
import time
import json
import copy
import random
import sys
class Surveilance:
    def __init__(self):
        self.mac = MacLookup()
        self.here_now = set()

        proc = subprocess.Popen(["ifconfig", "wlan0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()
        output = o.decode('ascii').split("\n")
        for line in output:
            if "netmask" in line:
                x = [l for l in line.split(" ") if l]
                self.scan_IP = x[1]
                break
            else:
                self.scan_IP = "10.0.0.0"
                break


        self.submask = 24
        with open("messages.json", "r") as file:
            x = json.load(file)
            self.welcome_messages = x['welcome_messages']
            self.goodbye_messages = x['goodbye_messages']
        with open("settings.json", "r") as file:
            x = json.load(file)
            self.TIMEOUT_MINUTES = x["timeout_minutes"]
        try:
            with open('people.json', 'r') as file:
                self.entries = json.load(file)
        except:
            self.entries = {}

    def say(self, text):
        print("Speaking / Holding thread")
        if sys.platform == 'linux':
            command = ["espeak", "-v", "mb-en1", f'" - ... - {text}"', "-p65", "-s120"]
        elif sys.platform == 'darwin':
            command = ["say", f'" - ... - {text}"']
        subprocess.run(command)

    def welcome_message(self, mac):
        if self.entries[mac]['name']:
            self.say(f"Welcome, {self.entries[mac]['name']}")
            self.say(random.choice(self.welcome_messages))

    def goodbye_message(self, mac):
        if self.entries[mac]['name']:
            self.say(f"Goodbye, {self.entries[mac]['name']}")
            

    def scan(self, command):
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()
        lines = o.decode('ascii').split('\n')
        past_entries = copy.deepcopy(self.entries)

        # parse nmap output
        for i,line in enumerate(lines[:-4]):
            if "Nmap scan report for" in line:
                ip = line[21:]
                mac = lines[i+2][13:30]
                if mac in self.entries.keys():
                    self.entries[mac]['ip'] = ip
                    self.entries[mac]['last_seen'] = time.time()
                else:
                    self.entries[mac] = {'name': '','ip': ip, 'mac': mac, 'first_seen': time.time(), 'last_seen': time.time()}
                self.here_now.add(mac)

        # say welcome and goodbye messages
        for mac in self.entries.keys():
            if len(past_entries) and time.time() - self.entries[mac]['last_seen'] > 60*self.TIMEOUT_MINUTES and mac in self.here_now:
                self.goodbye_message(mac)
                self.here_now.remove(mac)
        for mac in self.here_now:
            if mac not in past_entries.keys() or time.time() - past_entries[mac]['last_seen'] > 60*self.TIMEOUT_MINUTES:
                self.welcome_message(mac)

    def fetch_names(self):
        try:
            with open('people.json', 'r') as file:
                saved_entries = json.load(file)
                for entry in saved_entries:
                    self.entries[entry]['name'] = saved_entries[entry]['name']
        except:
            print("Something is wrong with people.json. If you keep seeing this message, try to find the root cause.")
            pass

    def get_guest_list(self):
        return [self.entries[mac]["name"] for mac in self.here_now if self.entries[mac]["name"]]


    def surveil(self, guests):
        i = 0
        while True:

            guests.update(self.get_guest_list())

            if i % 30 == 0:
                print(str(datetime.datetime.now()), "> Full scan")
                self.scan(['sudo', 'nmap', '-snP', self.scan_IP + '/' + str(self.submask)])
                self.fetch_names()
                with open('people.json', 'w') as file:
                    json_data = json.dumps(self.entries, indent=4)
                    file.write(json_data)
            else:
                print(str(datetime.datetime.now()), "> Regular scan")
                self.scan(['sudo', 'nmap', '-snP'] + [entry['ip'] for entry in self.entries.values()])

            if i % 5 == 0:
                print(str(datetime.datetime.now()), "> Updating names")
                self.fetch_names()
            
            print(str(datetime.datetime.now()), "> Completed iteration")

            i += 1
            time.sleep(2)