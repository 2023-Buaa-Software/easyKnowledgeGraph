
from selenium.common.exceptions import NoSuchElementException
import spacy
from spacy import displacy
import pandas as pd
import aiohttp
import asyncio
import csv
   
nlp = spacy.load("zh_core_web_trf")

async def csv_to_txt(title):
    doc = nlp(title)
    for tag in doc.ents:   
        print(tag.text, f"({tag.label_})") 
        with open('./data/wordCloudText_content.txt', 'a', encoding='utf-8') as txt:
            txt.write(tag.text + '\n')

def run():
    df = pd.read_csv("./data/content.csv")
    titles = df.iloc[:,0]
    contents = df.iloc[:,1].astype(str)
    for i in range(len(titles)):
        print(i)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(csv_to_txt(contents[i]))

if __name__ =='__main__':
    run()