from ..basic import DATA, read, write, logger

import json

def getGroupData(group: str, key: str = None):
    data = read(DATA + "/" + str(group) + "/settings.json")
    if not data:
        return False
    else:
        data = json.loads(data)
    if not key:
        return data
    else:
        return data[key]

def setGroupData(group: str, key: str, new):
    data = json.loads(read(DATA + "/" + str(group) + "/settings.json"))
    if not data:
        return False
    data[key] = new
    write(DATA + "/" + str(group) + "/settings.json", json.dumps(data, ensure_ascii=False))
    return True