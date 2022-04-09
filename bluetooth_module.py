import pyttsx3
import bluetooth
import time
devices = {} 
currently_visiting = set()

engine = pyttsx3.init()


while True:
    print("Current visitors:")
    [print(dvs) for dvs in currently_visiting]
    print()
    nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=True,
                    flush_cache=True, lookup_class=False)
    for device in nearby_devices:
        if not (device[0] in devices):
            devices[device[0]] = {'name': device[1], 'deviceName': device[1]}
            engine.say("New visitor found. Please register in the app.")
        if not (device[0] in currently_visiting):
            currently_visiting.add(device[0])
            name = devices[device[0]]["name"]
            engine.say(f"Welcome, {name}")
            engine.runAndWait()

    for device in currently_visiting:
        if device not in [d[0] for d in nearby_devices]:
            currently_visiting.remove(device)
            engine.say(f"Goodbye, {name}")
            engine.runAndWait()
    time.sleep(5)