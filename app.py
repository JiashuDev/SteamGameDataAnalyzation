from flask import Flask, request, render_template, session, redirect
import time
from utils.query import querys
import sys
import io
from utils.getPublicData import *
from utils.getPageData import *
from utils.getHistory import *
from recommendation.machine import *
app = Flask(__name__)
app.secret_key = 'This is secret Key'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdout = sys.stderr


@app.route('/')
def hello_world():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        print(form_data)

        def filter_fns(item):
            return form_data['username'] in item and form_data['password'] in item

        users = querys('select * from user', [], 'select')
        login_success = list(filter(filter_fns, users))
        if not login_success:
            return "username or password incorrect"
        session['username'] = form_data['username']
        return redirect('/home')
    else:
        return render_template('./pages-login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        request_data = request.form.to_dict()
        if request_data['username'] and request_data['password'] and request_data['passwordChecked']:
            if request_data['password'] != request_data['passwordChecked']:
                return "Passwords don't match"
            else:
                def filter_fn(item):
                    return request_data['username'] in item
            users = querys('select * from user', [], 'select')
            filter_list = list(filter(filter_fn, users))
            if len(filter_list):
                return "Username already exists"
            else:
                querys('insert into user (username, password) values (%s, %s)',
                       [request_data['username'], request_data['password']])
        else:
            return "username or password can not be null"
        return redirect('/login')
    else:
        return render_template('./pages-register.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, xData, yData, gameTimeSort, gameListData, userListData, typeListData = getHomeData()
    return render_template('index.html',
                           username=username,
                           typeSort=typeSort,
                           maxDiscountTitle=maxDiscountTitle,
                           maxUserLen=maxUserLen,
                           maxGames=maxGames,
                           xData=xData,
                           yData=yData,
                           gameTimeSort=gameTimeSort,
                           gameListData=gameListData,
                           userListData=userListData,
                           typeListData=typeListData)


@app.route('/search', methods=['GET', 'POST'])
def search():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    if request.method == 'POST':
        searchWord = request.form.to_dict()["searchInput"]

        def filter_fn(item):
            if item[1].lower().find(searchWord.lower()) == -1:
                return False
            else:
                return True

        data = list(filter(filter_fn, getAllGames()))

        return render_template('search.html',
                               username=username,
                               typeSort=typeSort,
                               maxDiscountTitle=maxDiscountTitle,
                               maxUserLen=maxUserLen,
                               maxGames=maxGames,
                               categoryList=categoryList,
                               data=data)
    else:
        return render_template('search.html',
                               username=username,
                               typeSort=typeSort,
                               maxDiscountTitle=maxDiscountTitle,
                               maxUserLen=maxUserLen,
                               maxGames=maxGames,
                               categoryList=categoryList)


@app.route('/logOut', methods=['GET', 'POST'])
def logOut():
    session.clear()
    return redirect('/login')


@app.route('/dataForm', methods=['GET', 'POST'])
def dataForm():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    return render_template('dataForm.html',
                           username=username,
                           typeSort=typeSort,
                           maxDiscountTitle=maxDiscountTitle,
                           maxUserLen=maxUserLen,
                           maxGames=maxGames,
                           categoryList=categoryList)


@app.route('/addHistory/<int:gameId>', methods=['GET', 'POST'])
def addHistory(gameId=None):
    username = session['username']
    userId = querys('select id from user where username =%s', [username], 'select')[0][0]
    gameId = querys('select id from games where id =%s', [gameId], 'select')[0][0]
    getData(userId, gameId)
    gameUrl = querys('select detailLink from games where id =%s', [gameId], 'select')[0][0]
    return redirect(gameUrl)


@app.route('/price', methods=['GET', 'POST'])
def price():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    yearList = ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012',
                '2011', '2010', '2009', '2008']
    defaultYear = yearList[0]

    if request.method == 'POST':
        year = request.form.get('year')
        defaultYear = year
        x1Data, y1Data, x2Data, y2Data = getPrice(defaultYear)
        resData = []
        for index, x in enumerate(x2Data):
            resData.append([x, y2Data[index]])

        return render_template('price.html',
                               username=username,
                               typeSort=typeSort,
                               maxDiscountTitle=maxDiscountTitle,
                               maxUserLen=maxUserLen,
                               maxGames=maxGames,
                               categoryList=categoryList,
                               yearList=yearList,
                               defaultYear=defaultYear,
                               resData=resData,
                               x1Data=x1Data,
                               y1Data=y1Data)
    else:
        x1Data, y1Data, x2Data, y2Data = getPrice(defaultYear)
        resData = []
        for index, x in enumerate(x2Data):
            resData.append([x, y2Data[index]])
        return render_template('price.html',
                               username=username,
                               typeSort=typeSort,
                               maxDiscountTitle=maxDiscountTitle,
                               maxUserLen=maxUserLen,
                               maxGames=maxGames,
                               categoryList=categoryList,
                               yearList=yearList,
                               defaultYear=defaultYear,
                               resData=resData,
                               x1Data=x1Data,
                               y1Data=y1Data)


@app.route('/type', methods=['GET', 'POST'])
def type():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    typeList, x2Data, y2Data = getTypeList()
    defaultType = typeList[0]

    if request.args.get('type'):
        defaultType = request.args.get('type')
        x1Data, y1Data = getType(defaultType)

        return render_template('type.html',
                               username=username,
                               typeSort=typeSort,
                               maxDiscountTitle=maxDiscountTitle,
                               maxUserLen=maxUserLen,
                               maxGames=maxGames,
                               categoryList=categoryList,
                               typeList=typeList,
                               defaultType=defaultType,
                               x1Data=x1Data,
                               y1Data=y1Data,
                               x2Data=x2Data,
                               y2Data=y2Data)

    else:
        x1Data, y1Data = getType(defaultType)

        return render_template('type.html',
                               username=username,
                               typeSort=typeSort,
                               maxDiscountTitle=maxDiscountTitle,
                               maxUserLen=maxUserLen,
                               maxGames=maxGames,
                               categoryList=categoryList,
                               typeList=typeList,
                               defaultType=defaultType,
                               x1Data=x1Data,
                               y1Data=y1Data,
                               x2Data=x2Data,
                               y2Data=y2Data)


@app.route('/rate', methods=['GET', 'POST'])
def rate():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    rateOneList, rateTwoList = getRate()
    return render_template('rate.html',
                           username=username,
                           typeSort=typeSort,
                           maxDiscountTitle=maxDiscountTitle,
                           maxUserLen=maxUserLen,
                           maxGames=maxGames,
                           categoryList=categoryList,
                           rateOneList=rateOneList,
                           rateTwoList=rateTwoList
                           )


@app.route('/dev', methods=['GET', 'POST'])
def dev():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    x1Data, y1Data, x2Data, y2Data = getDev()
    return render_template('dev.html',
                           username=username,
                           typeSort=typeSort,
                           maxDiscountTitle=maxDiscountTitle,
                           maxUserLen=maxUserLen,
                           maxGames=maxGames,
                           categoryList=categoryList,
                           x1Data=x1Data,
                           y1Data=y1Data,
                           x2Data=x2Data,
                           y2Data=y2Data
                           )


@app.route('/other', methods=['GET', 'POST'])
def other():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    otherList = getOther()
    return render_template('other.html',
                           username=username,
                           typeSort=typeSort,
                           maxDiscountTitle=maxDiscountTitle,
                           maxUserLen=maxUserLen,
                           maxGames=maxGames,
                           categoryList=categoryList,
                           otherList=otherList,
                           )


@app.route('/titleCloud', methods=['GET', 'POST'])
def titleCloud():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    return render_template('titleCloud.html',
                           username=username,
                           typeSort=typeSort,
                           maxDiscountTitle=maxDiscountTitle,
                           maxUserLen=maxUserLen,
                           maxGames=maxGames,
                           categoryList=categoryList)


@app.route('/summaryCloud', methods=['GET', 'POST'])
def summaryCloud():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    return render_template('summaryCloud.html',
                           username=username,
                           typeSort=typeSort,
                           maxDiscountTitle=maxDiscountTitle,
                           maxUserLen=maxUserLen,
                           maxGames=maxGames,
                           categoryList=categoryList)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    username = session['username']
    typeSort, maxDiscountTitle, maxUserLen, maxGames, categoryList = get_tableData()
    user_ratings = getUser_ratings()
    recommend_list = user_base_collaborative_filtering(username, user_ratings)
    resList = getRecommend(recommend_list)
    return render_template('recommend.html',
                           username=username,
                           typeSort=typeSort,
                           maxDiscountTitle=maxDiscountTitle,
                           maxUserLen=maxUserLen,
                           maxGames=maxGames,
                           categoryList=categoryList,
                           resList=resList)


if __name__ == '__main__':
    app.run()
