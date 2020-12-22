from CoreStructure import Core
from time import sleep

print("Creating Core object...")
core = Core()
print("Calling process()...")
core.process([{'intent': 'modes', 'probability': '0.90'}], 'set desk to study and bed to christmas')
print("Done")
sleep(5)
core.process([{'intent': 'modes', 'probability': '0.90'}], 'set desk to christmas and bed to party')
print("Done")