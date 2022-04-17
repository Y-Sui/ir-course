import os
import json

from generateIdMap import IdMap
from preProcess import PreprocessFile
from compressIndex import CompressedPostings


class EstablishIndex:
    """
    filePath = "./hyatt-k"
    load_data: 获得目录下所有文件的路径,并保存到hyatt-k目录下的dir.txt文件
    sortTheDict: 对词典数据进行排序
    getWordList：获得词表
    getDocName：获得docID对应的文档相对路径
    """
    def __init__(self):
        self.load_data("./hyatt-k")
        self.invertedIndex = {}
        self.wordList = []
        self.doc_map = IdMap()
        self.wholeDocList = []
        self.dict = {}

    def load_data(self, filePath):
        f = open("./cache/dir.txt", "a")
        for root, dirs, files in os.walk(filePath):
            for file in files:
                f.writelines(os.path.join(root, file).replace('\\', '/') + "\n")

    def sortTheDict(self, dict):
        sortedDict = {k: dict[k] for k in sorted(dict.keys())}
        for stem in sortedDict:
            sortedDict[stem] = {k: sortedDict[stem][k] for k in sorted(sortedDict[stem].keys())}
        return sortedDict

    def getWordList(self):
        # 获得词表
        for word in self.invertedIndex.keys():
            self.wordList.append(word)

    def getDocName(self, docID):
        # 返回docID对应的文档相对路径
        return self.doc_map._get_str(docID)

    def writeToFile(self, data, savePath):
        file = open(savePath, 'w')
        str = json.JSONEncoder().encode(data)
        file.write(str)
        file.close()

    def printIndex(self, index):
        for stem in index:
            print(stem)
            for doc in index[stem]:
                print("    ", doc, " : ", index[stem][doc])

    def createIndex(self):
        with open("./cache/dir.txt", "r") as f:
            files = []
            for line in f.readlines():
                line = line.split("\n")
                files.extend(line)
            while '' in files:
                files.remove('')
        os.remove("./cache/dir.txt")
        for file in files:
            print("Analyzing file: ", file)
            doc = PreprocessFile().preProcess(file)  # doc是文档经过预处理后的分词列表
            docID = self.doc_map._get_id(file)
            self.wholeDocList.append(docID)
            num = 0  # term在doc中的位置
            for term in doc:
                if term not in self.invertedIndex:
                    docList = {}
                    docList[docID] = [num]
                    self.invertedIndex[term] = docList
                else:
                    if docID not in self.invertedIndex[term]:
                        self.invertedIndex[term][docID] = [num]
                    else:
                        self.invertedIndex[term][docID].append(num)
                num += 1
        # 给倒排索引中的词项排序
        self.invertedIndex = self.sortTheDict(self.invertedIndex)
        # 获得词项列表
        self.getWordList()
        # 测试
        # self.printIndex(self.invertedIndex)
        self.dict = dict(zip(self.wholeDocList, files))
        # 数据写入文件
        # self.writeToFile(CompressedPostings.encode(self.invertedIndex), "./cache/invertIndex.json")
        self.writeToFile(self.invertedIndex, "./cache/invertIndex.json")
        self.writeToFile(self.wordList, "./cache/wordList.json")
        self.writeToFile(self.dict, "./cache/doc2docID.json")
        self.writeToFile(sorted(self.wholeDocList), "./cache/wholeDocList.json")

EstablishIndex().createIndex()
