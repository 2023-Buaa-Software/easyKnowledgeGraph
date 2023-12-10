from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import urlopen
from aiohttp.client import ClientSession
import pandas as pd
import aiohttp
import asyncio
import time

download_contents = []

async def get_content(href, title):
    try:
        html = urlopen(href)
        print(15, href)
        # 使用 Beautiful Soup 解析页面源代码
        soup = BeautifulSoup(html.read(), 'html.parser')
        # 通过 CSS 选择器查找元素
        contents = soup.find_all(attrs={"align":"justify"})
        info = []
        for content in contents:
            info.append(content.text)
        else: 
            content = ' '.join(info)
            print(19, title, content)
            df = pd.DataFrame([content], [title])
            df.to_csv('content.csv', mode='a', header=False, index=True, encoding='utf-8')
    except NoSuchElementException:
        print("Element not found")

def run():
    df = pd.read_csv("data.csv")
    hrefs = df.iloc[:,0]
    titles = df.iloc[:,1]
    for i in range(len(hrefs)):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_content(hrefs[i], titles[i]))

if __name__ =='__main__':
    run()