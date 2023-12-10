import spacy
from spacy import displacy
import pandas as pd

nlp = spacy.load("zh_core_web_sm")
# nlp = spacy.load("zh_core_web_trf")

news_text = """
11月23日，生态环境部科财司一级巡视员朱广庆、生态司司长王志斌率领生态环境部科财司、生态司、土壤司等10个业务司的相关部门负责人到地理资源所调研中国科学院先导专项“美丽中国生态文明建设科技工程”（以下简称“美丽中国”先导专项）研究进展。调研会议由中国科学院科发局张鸿翔副局长主持。 
"""

# 处理文本
doc = nlp(news_text)
# 直接显示在Jupyter Notebook中
displacy.render(doc, style='ent', jupyter=True)


# 提取人物和活动
entities = []
# for tok in doc:
    # print("doc_text", tok.text, "dep", tok.dep_)
# for ent in doc.ents:
    # print("ents_text", ent.text, "label", ent.label_)



# 从文本到句子列表  
lst_docs = [sent for sent in doc.sents]  
print ( "tot sentences:" , len(lst_docs))

i = 2
print(lst_docs[i], "\n---")

for token in lst_docs[i]:    
    print(token.text, "-->", "pos: " + token.pos_, "|", "dep: " + token.dep_, "")

for tag in lst_docs[i].ents:    
    print(tag.text, f"({tag.label_})") 

displacy.render(lst_docs[i], style="dep", options={"distance":100})
