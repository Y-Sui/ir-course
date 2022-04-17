import re

import nltk
from nltk.corpus import stopwords


# nltk.download('stopwords')

class PreprocessFile:
    def __init__(self):
        pass

    def preProcess(self, filePath):
        file = open(filePath, 'r')
        doc = file.read()
        doc_ = self.stemming(doc)  # doc_返回文档经预处理后的分词列表
        return doc_

    def stemming(self, doc):
        """
        :param doc: 读取得到的文档内容
        :return: doc_ 返回文档经过文本处理后的分词列表
        """
        lower = doc.lower()
        deleteSignal = [',', '.', ';', '-', '&', ':', '<', '@', '>', "'", '--', '$', '`', '(', ')', '+', '!', '*', '"',
                        '?', '#', '*', '%', '~']
        # 去除数字
        lower = re.sub(r'[0-9]+', '', lower)
        # 去除标点符号
        for signal in deleteSignal:
            lower = lower.replace(signal, '')
        without_punctuation = lower
        # 分词
        tokens = nltk.word_tokenize(without_punctuation)
        # 去除停用词
        without_stopwords = [w for w in tokens if not w in stopwords.words('english')]
        # 提取题干,e.g., cleaning/cleans/cleaned等==clean
        cleaner = nltk.stem.SnowballStemmer('english')
        cleaned_text = [cleaner.stem(ws) for ws in without_stopwords]
        return cleaned_text

# a = PreprocessFile()
# print(a.preProcess("./hyatt-k/corp_memos/13"))
