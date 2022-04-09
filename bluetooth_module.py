import pyttsx3
import bluetooth
nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                flush_cache=True, lookup_class=False)
print(nearby_devices)

engine = pyttsx3.init()
name = "Halvor"
engine.say(f"Welcome, {name}")
engine.runAndWait()
