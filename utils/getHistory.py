from utils.query import querys


def getData(userId, gameId):
    historyData = querys('select id from history where game_id = %s and user_id = %s', [gameId, userId], 'select')
    if len(historyData):
        querys('update history set count = count + 1 where game_id = %s and user_id = %s', [gameId, userId])
    else:
        querys('insert into history(game_id, user_id, count) values (%s, %s, %s)', [gameId, userId, 1])
