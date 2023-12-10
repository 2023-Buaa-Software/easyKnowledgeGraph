import spacy
from spacy import displacy
import pandas as pd
from spacy.matcher import Matcher 
import networkx as nx
import matplotlib.pyplot as plt
# nlp = spacy.load("zh_core_web_sm")
nlp = spacy.load("zh_core_web_trf")

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
news_text = read_file("./data/text1.txt")

def get_entities(sent):
    ## chunk 1
    ent1 = ""
    ent2 = ""

    prv_tok_dep = ""    # dependency tag of previous token in the sentence
    prv_tok_text = ""   # previous token in the sentence

    prefix = ""
    modifier = ""
    #############################################################
    
    for tok in nlp(sent).sents:
        for token in doc:
            print(tok.text, tok.dep_, tok.pos_)
            ## chunk 2
            # if token is a punctuation mark then move on to the next token
            if tok.dep_ != "punct":
                # check: token is a compound word or not
                if tok.dep_ == "compound:nn":
                    prefix = prefix + tok.text
                    # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound:nn":
                        prefix = prv_tok_text + tok.text
                
                # check: token is a modifier or not
                if tok.dep_.endswith("mod") == True:
                    modifier = tok.text
                    # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound:nn":
                        modifier = prv_tok_text + tok.text
                
                ## chunk 3
                if tok.dep_.find("subj") == True:
                    ent1 = modifier +" "+ prefix + " "+ tok.text
                    prefix = ""
                    modifier = ""
                    prv_tok_dep = ""
                    prv_tok_text = ""      

                ## chunk 4
                if tok.dep_.find("obj") == True:
                    ent2 = modifier +" "+ prefix +" "+ tok.text
                    
                ## chunk 5  
                # update variables
                prv_tok_dep = tok.dep_
                prv_tok_text = tok.text
        #############################################################

        return [ent1.strip(), ent2.strip()]

def get_relation(sent):
    doc = nlp(sent)

    # 用spaCy词汇表初始化Matcher
    matcher = Matcher(nlp.vocab)

    # 基于规则的spaCy匹配 define the pattern 
    pattern = [{'DEP':'ROOT'}, {'DEP':'prep','OP':"?"}, {'DEP':'agent','OP':"?"}, {'POS':'ADJ','OP':"?"}, {'POS': 'VERB','OP':"?"}] 

    matcher.add("matching_1", [pattern]) 

    # 输出： [(7604275899133490726, 6, 8)],有三个元素, 第一个元素“7604275899133490726”是匹配ID。第二个和第三个元素是匹配标记的位置。
    matches = matcher(doc)
    k = len(matches) - 1

    # 获得匹配的宽度
    span = doc[matches[k][1]:matches[k][2]] 

    return(span.text)

def graph(entities, relations):
    # extract subject
    source = [i[0] for i in entities]

    # extract object
    target = [i[1] for i in entities]

    print(106, source, target, relations)

    kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})

    G1 = nx.MultiDiGraph()
    G1.graph['edge'] = {'arrowsize': '0.3', 'splines': 'curved', 'color':'red'}
    G1.graph['node'] = {'shape':'ellipse', 'fontname':"FangSong"}
    G=nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=G1)

    plt.rcParams['font.sans-serif'] = ['SimHei']  #  可以选用任何已经存在的字体
    plt.figure(figsize=(12,12))

    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
    plt.show()  

# entity_pairs = get_entities("John completed the task")
# relations = get_relation("John completed the task")

lst_docs = [sent for sent in doc.sents]  
entity_pairs = get_entities(news_text)
# relations = get_relation(news_text)

print(115, entity_pairs)
# print(116, relations)


# 处理文本
# doc = nlp(news_text)

# 提取人物和活动
# entities = []
# for tok in doc:
    # print(tok.text, tok.dep_, tok.head, tok.pos_, tok.tag_)
    # entities.append({"text": tok.text, "label": tok.label_})

# 存储到 CSV 文件
# df = pd.DataFrame(entities)
# df.to_csv("entities.csv", index=False)
