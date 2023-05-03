import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import PIL
import numpy as np

# 导入文本数据并进行简单的文本处理
# 去掉换行符和空格以及标点符号
text = open("oh_emma.txt", encoding='utf8').read()
text = text.replace('\n', "").replace("，", "").replace("。", "").replace("、", "").replace("；", "").replace("！",
                                                                                                          "").replace(
    "：", "").replace('1', "").replace('VLOG', "").replace('/', "").replace('*', "").replace("'", "").replace('.',
                                                                                                             "").replace(
    '？',
    "").replace(
    "2", '').replace(',', "").replace('#', "").replace('l',"").replace('?',"").replace("【",'').replace("】",'').replace("!",'').replace("|",'').replace(":",'')

# 分词，返回结果为词的列表
text_cut = jieba.lcut(text)

# 停用词库
stop_words = open("Stop Words.txt", encoding="utf8").read().split("\n")

# 将分好的词用某个符号分割开连成字符串
text_cut = ' '.join(text_cut)
print(text_cut)

# 词云形状
image1 = PIL.Image.open('oh_emma.jpg')
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
