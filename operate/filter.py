from selenium.common.exceptions import NoSuchElementException
import spacy
from spacy import displacy
import pandas as pd
import aiohttp
import asyncio

# nlp = spacy.load("zh_core_web_sm")
nlp = spacy.load("zh_core_web_trf")

def is_nan(nan):
    return nan != nan

async def get_content(title, content):
    doc = nlp(content)
    df = pd.DataFrame([1], [title])
    df.to_csv('./data/quoto.csv', mode='a', header=False, index=True, encoding='utf-8')
    # 从文本到句子列表  
    for sent in doc.sents:
        if len(str(sent).strip()):
            if str(sent) != 'nan':
                df = pd.DataFrame([0], [sent])
                df.to_csv('./data/fliter_quoto.csv', mode='a', header=False, index=True, encoding='utf-8')


def run():
    df = pd.read_csv("./data/quoto.csv")
    titles = df.iloc[:,0]
    contents = df.iloc[:,1].astype(str)
    for i in range(len(titles)):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_content(titles[i], contents[i]))



if __name__ =='__main__':
    run()