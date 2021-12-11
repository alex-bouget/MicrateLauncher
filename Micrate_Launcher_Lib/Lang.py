from locale import getdefaultlocale
import json

lang: dict
"""Lang data"""
try:
    lang = json.load(open("Ressources/lang/"+getdefaultlocale()[0]+".json"))
except FileNotFoundError:
    lang = json.load(open("Ressources/lang/en_US.json"))
