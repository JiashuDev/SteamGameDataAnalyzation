from utils.query import querys
import json


def getAllGames():
    gameList = querys('select * from games', [], 'select')

    def map_fn(item):
        try:
            item = list(item)
            item[4] = json.loads(item[4])
            item[9] = json.loads(item[9])
            item[15] = json.loads(item[15])
            item[8] = round(float(item[8]), 2)
            return item
        except:
            pass

    result = [item for item in map(map_fn, gameList) if item is not None]
    return result



def getAllUser():
    userList = querys('select * from user', [], 'select')
    return userList
