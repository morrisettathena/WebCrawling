import json
import consts as c

def get_keywords():
    with open(c.Kword_file) as file:
        return json.load(file)