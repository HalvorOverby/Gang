import pyttsx3
import bluetooth
nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=True,
                flush_cache=True, lookup_class=False)

engine = pyttsx3.init()
for device in nearby_devices:
    engine.say(f"Welcome, {device[1]}")
engine.runAndWait()
