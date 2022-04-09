import pyttsx3
import bluetooth
devices = {} 
engine = pyttsx3.init()

voices = engine.getProperty('voices')
for voice in voices:
    if voice.languages[0] == u'no_NB':
        engine.setProperty('voice', voice.id)
        break

while True:
    
    nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=True,
                    flush_cache=True, lookup_class=False)
    for device in nearby_devices:
        if not (device[0] in devices):
            devices[device[0]] = {'name': 'Ukjent', 'deviceName': device[1]}
            engine.say("Ny besøkende registrert. Vennligst registrer i appen.")
    
    for device in nearby_devices:
        name = devices[device[0]]["name"]
        engine.say(f"Velkommen, {name}")
    engine.runAndWait()
