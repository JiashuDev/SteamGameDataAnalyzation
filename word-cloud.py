import jieba
from matplotlib import pylab as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from pymysql import *


def get_img(field, targetImage, resImage):
    conn = connect(host='localhost', user='root', passwd='root', database='steamdata', port=3306, charset='utf8mb4')

    cursor = conn.cursor()

    # Correcting the SQL query using an f-string
    sql = "SELECT summary FROM games"
    cursor.execute(sql)
    data = cursor.fetchall()

    text = ''

    for i in data:
        if i[0] != None:
            tagArr = i
            for j in tagArr:
                text += j
    cursor.close()

    img = Image.open(targetImage)
    img_arr = np.array(img)
    wc = WordCloud(
        font_path='STHUPO.TTF',
        mask=img_arr,
        background_color='white',
    )
    wc.generate_from_text(text)
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(resImage, dpi=800, bbox_inches='tight', pad_inches=-0.1)


get_img("title", "./static/picture/test.jpg", "./static/image/summaryCloud.png")
