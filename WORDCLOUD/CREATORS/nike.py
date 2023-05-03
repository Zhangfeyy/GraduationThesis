import jieba
from jieba import analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import PIL
import numpy as np

# 导入文本数据并进行简单的文本处理
# 去掉换行符和空格以及标点符号
text = open("妮可蹦蹦.txt", encoding='utf8').read()
text = text.replace('\n', "").replace("，", "").replace("。", "").replace("、", "").replace("；", "").replace("！",
                                                                                                          "").replace(
    "：", "").replace('【',"").replace('】',"").replace('妮可',"").replace('*',"").replace("'","").replace('｜',"").replace('？',"").replace("～",'').replace(',',"").replace('|',
                                                                                                                                                                        "").replace(
    '化妆','').replace('护肤','').replace('粉底液','').replace('粉底','').replace('妆容','').replace('2018','').replace('视频','')
# keys=jieba.analyse.extract_tags(text,topK=10,withWeight=True)
# print(keys)
# input()

# 分词，返回结果为词的列表
text_cut = jieba.lcut(text)

# 停用词库
stop_words = open("Stop Words.txt", encoding="utf8").read().split("\n")

# 将分好的词用某个符号分割开连成字符串
text_cut = ' '.join(text_cut)

# 词云形状
image1 = PIL.Image.open('妮可蹦蹦.jpg')
MASK = np.array(image1)

# 绘制词云
word_cloud = WordCloud(font_path="simsun.ttc",
                       background_color="white",
                       colormap='autumn',
                       mask=MASK,  # 指定词云的形状
                       stopwords=stop_words
                       )
word_cloud.generate(text_cut)

# 运用matplotlib展现结果
plt.subplots(figsize=(12, 8))
plt.imshow(word_cloud)
plt.axis("off")
plt.show()
