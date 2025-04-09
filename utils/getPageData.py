from datetime import datetime
from utils.getPublicData import *
from utils.query import querys


def getHomeData():
    maxUserLen = len(getAllUser())
    maxGames = len(getAllGames())
    gameList = getAllGames()
    allUserList = getAllUser()
    maxDiscountTitle = ''
    maxDiscount = 100
    typeDic = {}
    timeDic = {}
    for i in gameList:
        try:
            if int(i[6]) < maxDiscount:
                maxDiscount = int(i[6])
                maxDiscountTitle = i[1]
            for j in i[9]:
                if typeDic.get(j, -1) == -1:
                    typeDic[j] = 1
                else:
                    typeDic[j] += 1
            if timeDic.get(datetime.strptime(i[3], "%b %d, %Y").strftime("%Y-%m"), -1) == -1:
                timeDic[datetime.strptime(i[3], "%b %d, %Y").strftime("%Y-%m")] = 1
            else:
                timeDic[datetime.strptime(i[3], "%b %d, %Y").strftime("%Y-%m")] += 1
        except:
            pass
    gameListData = list(gameList)
    typeSort = list(sorted(typeDic.items(), key=lambda x: x[1], reverse=True))
    timeSort = list(sorted(timeDic.items(), key=lambda date: datetime.strptime(date[0], "%Y-%m")))

    def get_timeStamp(date):
        try:
            datetime.strptime(date, "%b %d, %Y").timestamp()
            return datetime.strptime(date, "%b %d, %Y").timestamp()
        except:
            return 0

    gameTimeSort = sorted(gameList, key=lambda x: get_timeStamp(x[3]), reverse=True)
    xData = []
    yData = []
    for i in timeSort:
        xData.append(i[0])
        yData.append(i[1])

    userDic = {}
    for i in allUserList:
        if userDic.get(i[-1], -1) == -1:
            userDic[i[-1]] = 1
        else:
            userDic[i[-1]] += 1
    userListData = []
    for key, value in userDic.items():
        userListData.append({
            'name': key,
            'value': value
        })
    typeListData = []
    for i in range(11):
        typeListData.append({
            'name': typeSort[i][0],
            'value': typeSort[i][1]
        })

    return typeSort[0][0], maxDiscountTitle, maxUserLen, maxGames, xData, yData, gameTimeSort[
                                                                                 :10], gameListData, userListData, typeListData


def get_tableData():
    gameList = getAllGames()
    gameListData = list(gameList)
    maxUserLen = len(getAllUser())
    maxGames = len(getAllGames())
    gameList = getAllGames()
    maxDiscountTitle = ''
    maxDiscount = 100
    typeDic = {}
    for i in gameList:
        try:
            if int(i[6]) < maxDiscount:
                maxDiscount = int(i[6])
                maxDiscountTitle = i[1]
            for j in i[9]:
                if typeDic.get(j, -1) == -1:
                    typeDic[j] = 1
                else:
                    typeDic[j] += 1
        except:
            pass
    typeSort = list(sorted(typeDic.items(), key=lambda x: x[1], reverse=True))
    return typeSort[0][0], maxDiscountTitle, maxUserLen, maxGames, gameListData


def getPrice(year):
    gameList = getAllGames()
    x1Data = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60 and above']
    y1Data = [0 for x in range(len(x1Data))]
    x2Data = ['0-10', '10-20', '20-30', '30-40', '40 and above']
    y2Data = [0 for x in range(len(x2Data))]
    for i in gameList:
        if datetime.strptime(i[3], "%b %d, %Y").strftime("%Y") == year:
            if float(i[7]) < 10:
                y1Data[0] += 1
            elif float(i[7]) < 20:
                y1Data[1] += 1
            elif float(i[7]) < 30:
                y1Data[2] += 1
            elif float(i[7]) < 40:
                y1Data[3] += 1
            elif float(i[7]) < 50:
                y1Data[4] += 1
            elif float(i[7]) < 60:
                y1Data[5] += 1
            else:
                y1Data[6] += 1

            if float(i[8]) < 10:
                y2Data[0] += 1
            elif float(i[8]) < 20:
                y2Data[1] += 1
            elif float(i[8]) < 30:
                y2Data[2] += 1
            elif float(i[8]) < 40:
                y2Data[3] += 1
            else:
                y2Data[4] += 1

    return x1Data, y1Data, x2Data, y2Data


def getTypeList():
    typeDic = {}
    gameList = getAllGames()
    for i in gameList:
        for j in i[9]:
            if typeDic.get(j, -1) == -1:
                typeDic[j] = 1
            else:
                typeDic[j] += 1
    typeSort = list(sorted(typeDic.items(), key=lambda x: x[1], reverse=True))
    x2Data = []
    y2Data = []
    for i in typeSort:
        x2Data.append(i[0])
        y2Data.append(i[1])
    return [x[0] for x in typeSort][:10], x2Data, y2Data


def getType(defaultType):
    typeDic = {}
    gameList = getAllGames()
    x1Data = []
    for i in gameList:
        flag = False
        for j in i[9]:
            if j == defaultType:
                flag = True
            if typeDic.get(j, -1) == -1:
                typeDic[j] = 1
            else:
                typeDic[j] += 1
        if flag:
            x1Data.append(int(i[6]))
    x1Data = list(set(x1Data))
    x1Data.sort()
    y1Data = [0 for x in range(len(x1Data))]
    for i in gameList:
        flag = False
        for j in i[9]:
            if j == defaultType:
                flag = True
        if flag:
            for index, j in enumerate(x1Data):
                if j == (int(i[6])):
                    y1Data[index] += 1
    return x1Data, y1Data


def getRate():
    gameList = getAllGames()
    rateOneList = [
        {
            'name': 'Positive',
            'value': 0
        },
        {
            'name': 'Mixed',
            'value': 0
        }
    ]

    rateTwoList = [
        {
            'name': 'Positive',
            'value': 0
        },
        {
            'name': 'Mixed',
            'value': 0
        }
    ]
    for i in gameList:
        if i[5] == 'Positive':
            rateOneList[0]['value'] += 1
        else:
            rateOneList[1]['value'] += 1
        if i[12] == 'Positive':
            rateTwoList[0]['value'] += 1
        else:
            rateTwoList[1]['value'] += 1
    return rateOneList, rateTwoList


def getDev():
    gameList = getAllGames()
    devDic = {}
    publishDic = {}
    for i in gameList:
        if devDic.get(i[13], -1) == -1:
            devDic[i[13]] = 1
        else:
            devDic[i[13]] += 1

        if publishDic.get(i[14], -1) == -1:
            publishDic[i[14]] = 1
        else:
            publishDic[i[14]] += 1
    return list(devDic.keys()), list(devDic.values()), list(publishDic.keys()), list(publishDic.values())


def getOther():
    gameList = getAllGames()

    otherList = [
        {
            'name': 'Mac',
            'value': 0
        },
        {
            'name': 'Win',
            'value': 0
        },
        {
            'name': 'Linux',
            'value': 0
        }
    ]
    for i in gameList:
        for j in i[4]:
            if j == 'mac':
                otherList[0]['value'] += 1
            elif j == 'win':
                otherList[1]['value'] += 1
            else:
                otherList[2]['value'] += 1

    return otherList

def getRecommend(recommendList):
    gameList = getAllGames()
    resList = []
    for i in gameList:
        if i[1] in recommendList:
            resList.append(i)
    return resList