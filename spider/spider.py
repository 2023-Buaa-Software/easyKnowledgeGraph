from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import asyncio
import pandas as pd
import re
import os
import csv

html = urlopen("http://www.igsnrr.cas.cn/news/picnews/index.html")
hrefList = ["http://www.igsnrr.cas.cn/news/picnews/index.html"]
titleList = []

def check_existed(title):
    if os.path.exists("data.csv"):
        df = pd.read_csv("data.csv")
        titles = df.iloc[:,1]
        if title in titles:
            return False
        else:
            return True

async def get_hrefs():
    soup = BeautifulSoup(html.read(), 'html.parser')
    anchor_tags = soup.findAll('span')
    index = 1
    for tag in anchor_tags:
        text = tag.text
        if text.find('页') != -1:
            for index in range(1, int(re.findall(r'\d+', text)[0])):
                hrefList.append('http://www.igsnrr.cas.cn/news/picnews/index_' + str(index) + '.html')

async def get_titles():
    # 读入数据
    df = pd.DataFrame(['title', 'href'])
    for href in hrefList:
        try:
            html = urlopen(href)
            # 使用 Beautiful Soup 解析页面源代码
            soup = BeautifulSoup(html.read(), 'html.parser')
            # 通过 CSS 选择器查找元素
            titles = soup.findAll('a', class_="tj")
            for title in titles:
                if title.text.find('转载') == -1:
                    if(check_existed(title.text)):
                        df = pd.DataFrame([title.text], [title.get('href')])
                        df.to_csv('url.csv', mode='a', header=False, index=True, encoding='utf-8')
                    else:
                        break
                        
        except NoSuchElementException:
            print("Element not found")

if __name__ == '__main__':    
    asyncio.run(get_hrefs())
    asyncio.run(get_titles(titles))


