import torch
from transformers import BertTokenizer, BertForTokenClassification
import pandas as pd

# 载入 BERT 模型和 tokenizer
model = BertForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

def extract_entities(text):
    # 使用 tokenizer 对文本进行编码
    inputs = tokenizer(text, return_tensors="pt")

    # 使用 BERT 模型进行预测
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)

    # 解码预测结果
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"].numpy()[0])
    labels = [model.config.id2label[prediction] for prediction in predictions.numpy()[0]]

    # 提取人物和组织的标签
    entities = []
    current_entity = {"text": "", "label": ""}
    for token, label in zip(tokens, labels):
        if label.startswith("B-"):
            if current_entity["text"]:
                entities.append(current_entity)
            current_entity = {"text": token, "label": label[2:]}
        elif label.startswith("I-"):
            current_entity["text"] += " " + token
        elif label == "O" and current_entity["text"]:
            entities.append(current_entity)
            current_entity = {"text": "", "label": ""}

    return entities

# 示例文本
news_text = """11月23日，生态环境部科财司一级巡视员朱广庆、生态司司长王志斌率领生态环境部科财司、生态司、土壤司等10个业务司的相关部门负责人到地理资源所调研中国科学院先导专项“美丽中国生态文明建设科技工程”（以下简称“美丽中国”先导专项）研究进展。调研会议由中国科学院科发局张鸿翔副局长主持。 
“美丽中国”先导专项负责人葛全胜研究员全面汇报专项近5年工作进展及取得的重要成果。专项各代表性成果负责人分别汇报了复合污染防治技术体系、生态修复及绿色发展技术模式、长江模拟器、山地灾害风险模拟预警平台、美丽中国建设智能化模拟系统、美丽中国和生态文明建设进程和成效评估以及农村清洁炊事和取暖路径与成本效益等专项代表性工作进展。 
朱广庆、王志斌对专项取得的丰富成果给予了高度肯定，认为“美丽中国”先导专项工作已融入到生态环境部等相关部门的业务工作之中、产生了实效，成果示范应用效果显著。双方就专项研发技术的应用，合作解决关键生态环境问题等方面进行了充分的交流。朱广庆指出，希望同“美丽中国”先导专项合作加强生态环境科技领域重大需求的研究，聚焦“卡脖子”问题，促进科技自立自强。王志斌强调要重视高层次生态环境监管，建议在监管目标指标体系、生态保护与发展布局等方面开展合作研究，通过技术成果转化等来解决生态环境监管需求问题。 
葛全胜对朱广庆、王志斌一行专程来地理资源所调研“美丽中国”先导专项工作进展表示欢迎，对生态环境部长期以来对“美丽中国”先导专项研发工作的支持表示感谢。他表示，专项将对标国家重大需求，进一步开展集成凝练工作，确保产出“用得上、有影响、留得下、推得开”的重大成果，高质量完成专项验收。 
生态环境部科财司科技处处长於俊杰、生态司综合处处长彭慧芳、土壤司综合处处长魏彦昌，中国科学院科发局环境处处长任小波，“美丽中国”先导专项总体组、专项管理办公室和专项主要参研人员等共计60余人参加调研交流。
"""

# 提取命名实体
entities = extract_entities(news_text)
print(48, entities)

# 存储到 CSV 文件
df = pd.DataFrame(entities)
df.to_csv("entities.csv", index=False)
