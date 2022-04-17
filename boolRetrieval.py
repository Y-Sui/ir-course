import queue
from operateDocList import *
import json
from spellingCheck import SpellingCheck
from compressIndex import CompressedPostings

def getData(filePath):
    # 读取数据
    file = open(filePath, 'r')
    lines = file.read()
    result = json.JSONDecoder().decode(lines)
    return result

def indexDecoder(data):
    # 索引解压
    return CompressedPostings.decode(data)

invertedIndex = getData('./cache/invertIndex.json')
wordList = getData('./cache/wordList.json')
wholeDocList = getData('./cache/wholeDocList.json')
doc2docID = getData('./cache/doc2docID.json')

class BoolRetrieval:
    def __init__(self):
        pass
    def boolOperator(self, oper):
        # 布尔检索操作数
        precedence = ['OR', 'AND', 'NOT']
        for i in range(3):
            if oper == precedence[i]:
                return i
        return -1
    def inf2Profix(self, inputList):
        # 中序表达式转换为后序表达式，将操作符放在表达式后
        precedence = {}
        precedence['OR'] = 0
        precedence['AND'] = 1
        precedence['NOT'] = 2
        profix_res = []
        temp = []
        queries = []
        for word in inputList:
            if word == '(':
                temp.append('(')
            elif word == ')':
                if len(queries) > 0:
                    profix_res.append(queries)
                    queries = []
                sym = temp.pop()
                while sym != '(':
                    profix_res.append(sym)
                    if len(temp) == 0:
                        print("Incorrect Query")
                        exit(1)
                        break
                    sym = temp.pop()
            elif word == 'NOT' or word == "OR" or word == 'AND':
                if len(queries) > 0:
                    profix_res.append(queries)
                    queries = []
                if (len(temp) <= 0):
                    temp.append(word)
                else:
                    sym = temp[len(temp) - 1]
                    # 弹出到左括号为止
                    while len(temp) > 0 and sym != '(' and precedence[sym] >= precedence[word]:
                        # pop out
                        profix_res.append(temp.pop())
                        if (len(temp) == 0):
                            break
                        sym = temp[len(temp) - 1]
                    # push in
                    temp.append(word)
            else:
                queries.append(word)
        if len(queries) > 0:
            profix_res.append(queries)
        while len(temp) > 0:
            profix_res.append(temp.pop())
        return profix_res

    def searchOneWord(self,index, word):
        if word not in index:
            return []
        else:
            # 将所有文档id变为数字
            docList = [int(key) for key in index[word].keys()]
            # 将文档的id排序
            docList.sort()
            return docList

    def serarchPhraseForBool(self,index, wordList, flag):
        if len(wordList) == 0:
            return []
        docQueue = queue.Queue()
        for word in wordList:
            docQueue.put(self.searchOneWord(index, word))

        while docQueue.qsize() > 1:
            list1 = docQueue.get()
            list2 = docQueue.get()
            docQueue.put(andTwoList(list1, list2))
        doclist = docQueue.get()

        if len(wordList) == 1:
            if flag:
                return doclist
            else:
                return listNotcontain(wholeDocList, doclist)

        reslist = []

        for docid in doclist:
            docid = str(docid)
            locList = []
            x = index[wordList[0]][docid]
            for loc in index[wordList[0]][docid]:
                # print(index[inputList[0]][docid])
                floc = loc
                n = len(wordList)
                hasFind = True
                for word in wordList[1:n]:
                    floc += 1
                    try:
                        # print(index[word][docid])
                        index[word][docid].index(floc)
                    except:
                        hasFind = False
                        break
                if hasFind:
                    reslist.append(int(docid))
                    break
        if flag:
            return reslist
        else:
            return listNotcontain(wholeDocList, reslist)

    def query_to_search(self, query, index):
        pofix = self.inf2Profix(query)
        result = []
        print(pofix)
        # queryArray = []
        # notTrue = ['1']
        # notFalse = ['0']
        nullReturn = []
        limit = len(pofix)
        i = 0
        while i < limit:
            item = pofix[i]
            if item != 'AND' and item != 'OR':
                if i < limit - 1:
                    if pofix[i + 1] == "NOT":
                        i = i + 1
                        result.append(self.serarchPhraseForBool(index, item, flag=False))
                    else:
                        result.append(self.serarchPhraseForBool(index, item, flag=True))
                else:
                    result.append(self.serarchPhraseForBool(index, item, flag=False))
            elif item == 'AND':
                if len(result) < 2:
                    print("illegal query")
                    return nullReturn
                else:
                    list1 = result.pop()
                    list2 = result.pop()
                    result.append(andTwoList(list1, list2))
            elif item == 'OR':
                if len(result) < 2:
                    print("illegal query")
                    return nullReturn
                else:
                    list1 = result.pop()
                    list2 = result.pop()
                    result.append(mergeTwoList(list1, list2))
            i += 1
        if len(result) != 1:
            print("illegal query")
            return nullReturn
        else:
            return result.pop()
    def answer(self, query, answer):
        if answer == "需要":
            correct_input = [SpellingCheck().spellingCheck(i) for i in query]
            result = BoolRetrieval().query_to_search(correct_input, invertedIndex)
        # docID转换为doc目录
            re_result = [doc2docID[str(i)] for i in result]
            return re_result
        else:
            result = BoolRetrieval().query_to_search(query, invertedIndex)
            return [doc2docID[str(i)] for i in result]




# # input = ["(", "americn", "AND", "china", ")"]
# input = ["(", "americn", "OR", "china", ")"]
# input = ["(", "americn", "AND", "china", ")"]
# input = ["americn", "AND", "china"]
# input = ["NOT", "english", "AND", "china"]
#
# # 拼写校正
# correct_input = [SpellingCheck().spellingCheck(i) for i in input]
# result = BoolRetrieval().query_to_search(correct_input, invertedIndex)
# # docID转换为doc目录
# re_result = [doc2docID[str(i)] for i in result]
# print(re_result)
# x = BoolRetrieval().answer(input)