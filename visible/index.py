# 统计文本文档中词频并生成词云图.py
import numpy as np
import jieba 
from wordcloud import WordCloud
from matplotlib import pyplot as plt 
from PIL import Image

# 以只读模式打开txt文档
f = open('D:/work/homework_spider/data/wordCloud.txt','r',encoding='utf-8') 
txt = f.read()
f.close()

# 预处理文本和背景图片
words = jieba.lcut(txt)		# 文本分词
newtxt = ' '.join(words)	# 将词语连接起来，以空格为连接词
# img = Image.open(r'back_pic_cloud.jpg')	 # 打开背景图片
# img_array = np.array(img)		# 将图片转换为数组
print(18, words, newtxt)

# 去除不希望在词云图中显示的词汇
excludes = []

# 设置词云图参数
wordcloud = WordCloud(
	background_color="black",
	width = 1080,
	height = 960,
	max_words = 150,
	max_font_size = 100,
	stopwords = excludes,
    font_path = "C:/Windows/Fonts/simfang.ttf",# 词云图 字体（中文需要设定为本机有的中文字体）
).generate(newtxt)

# 展示词云图并保存
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
# wordcloud.to_file('wordCloud.png')

