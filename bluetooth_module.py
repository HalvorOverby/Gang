import pyttsx3
import bluetooth
devices = {} 
currently_visiting = set()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
for voice in voices:
    if voice.languages[0] == u'en_US':
        engine.setProperty('voice', voice.id)
        break

while True:
    
    nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=True,
                    flush_cache=True, lookup_class=False)
    for device in nearby_devices:
        if not (device[0] in devices):
            devices[device[0]] = {'name': device[1], 'deviceName': device[1]}
            engine.say("Ny besøkende registrert. Vennligst registrer i appen.")
        if not (device[0] in currently_visiting):
            currently_visiting.add(device[0])

    for device in currently_visiting:
        if device not in [d[0] for d in nearby_devices]:
            currently_visiting.remove(device)
    
    for device in nearby_devices:
        name = devices[device[0]]["name"]
        engine.say(f"Velkommen, {name}")
    engine.runAndWait()
