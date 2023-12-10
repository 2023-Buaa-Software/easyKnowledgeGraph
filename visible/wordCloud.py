import collections
import re
import jieba
import requests
import parsel
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
import pyecharts.options as opts
from wordcloud import WordCloud
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np


def words_counts():
    with open('./data/wordCloudText.txt', mode='r', encoding='utf-8') as f:
        strData = f.read()

    # 替换符合parrtern的文本
    pattern = re.compile(r'\t|,|/|。|\n|\.|-|:|;|\)|\(|\?|，。，！”"')
    strData = re.sub(pattern, '', strData)  # 将符合模式的字符去除

    # 开始分词，精准模式
    words = jieba.cut(strData, cut_all=False)
    resultWords = [] # 空列表
    # 自定义停用词
    stopWords = [u'的', u'要', u'“', u'”', u'和', u'，', u'为', u'是',
                    '以' u'随着', u'对于', u'对', u'等', u'能', u'都', u'。',
                    u' ', u'、', u'中', u'在', u'了', u'通常', u'如果', u'我',
                    u'她', u'（', u'）', u'他', u'你', u'？', u'—', u'就',
                    u'着', u'说', u'上', u'这', u'那', u'有', u'也',
                    u'什么', u'·', u'将', u'没有', u'到', u'不', u'去']
    #
    for word in words:
        if word not in stopWords:
            resultWords.append(word)
    # print(resultWords) #  打印结果

    # 开始统计词频
    word_counts = collections.Counter(resultWords) # 一个词频统计对象
    # print(word_counts)

    # 获取高频词的列表
    word_counts_all = word_counts.most_common() # 一个列表，列表里是元组
    # print(word_counts_all)
    word_counts_top10 = word_counts.most_common(10)
    return word_counts_top10

def echart_top_10():
    data = words_counts()
    lab = [i[0] for i in data]
    num = [i[1] for i in data]
    # print(lab, num)

    bar = (
        Bar(init_opts=opts.InitOpts(width='1000px', height='700px', theme=ThemeType.LIGHT))
        .add_xaxis(xaxis_data=lab)
        .add_yaxis(
            series_name='',
            y_axis=num,
            label_opts=opts.LabelOpts(is_show=True, color='red'),
            bar_max_width='100px',
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='高词频前10',
                title_textstyle_opts=opts.TextStyleOpts(font_size=28,)
            ),
            legend_opts=opts.LegendOpts(
                pos_top='10%',
                pos_left='10%',
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=45), # 倾斜45度
            ),
            toolbox_opts=opts.ToolboxOpts(),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger='axis',# 触发类型，(axis表示坐标轴触发，鼠标移动上去的时候会有一条垂直于x轴的实线跟随鼠标移动，并且提示信息)
                axis_pointer_type='cross',# 指示器类型，(Cross表示生成两条分别垂直于x轴和y轴的虚线，不启用trigger才会显示完全)
            ),
        )
    ).render('top10.html')

def word_cloud_style():
    """
    另外一种生成词云的方法
    """
    # f = open('../Spiders/content.txt', 'r', encoding='utf-8')  # 这是数据源，也是想生成词云的数据
    # txt = f.read()  # 读取文件
    # print(type(txt))
    # print('=========================================')
    # f.close()  # 关闭文件，其实可以用withopen
    with open('./data/wordCloudText.txt', mode='r', encoding='utf-8') as f:
        txt = f.read()
        # 如果是文章的话，需要用到jieba分词，分完之后也可以自己处理下再生成词云
        # newTxt = re.sub("A-Z0-9-a-z\!\%\[\]\,\。", "", txt)
        # print(newTxt)

        # words = jieba.lcut(newTxt)
        # print(words)
        # img = Image.open(r'wc.jpg')  # 想要做的形状
        # img_array = np.array(img)

        # 相关配置，里面这个collections可以避免重复
        wordcloud = WordCloud(
            background_color='white',
            width=1080,
            height=960,
            # font_path = "../文悦新青年.otf",
            font_path='C:/Windows/Fonts/simfang.ttf',
            max_words=150,
            scale=10,  # 清晰度
            max_font_size=100,
            # mask=img_array,
            collocations=False).generate(txt)

        # plt.imshow(wordcloud)
        # plt.axis('off')
        # plt.show()
        wordcloud.to_file('wordCloud1.png')

if __name__ =='__main__':
    # word_cloud_style()
    echart_top_10()