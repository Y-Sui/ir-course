# 信息检索系统（IR）
## 实验要求: 基于给定的数据集,实现一个检索系统。
1. 基于给定数据集建立倒排索引
2. 进行布尔检索
3. 实现检索结果排序
4. 添加拼写校对
5. 进行索引压缩
6. 实现快速检索
7. 索引更新策略

## 模块：
1. 语言分析器（preProcess.py)：对原始文档信息进行处理，完成去除数字、标点符号、停用词，提取题干等操作，并返回文档经过预处理后的分词列表。
2. 索引器（establishIndex.py）：使用层次型位置倒排索引方法生成索引表，获得倒排索引表以及词项列表，并将结果储存到./cache文件下，方便后续查询中直接从磁盘调用到内存上，用空间换取时间效率。
3. 文本查询分析器（boolRetrieval.py）：使用布尔检索在索引表中查找与用户查询最接近的结果，并调用（operateDocList.py）完成索引的交、并、差等操作。
4. 拼写校对（spellingCheck.py）：对文本查询分析器的结果做进一步的拼写校对后再在索引表中进行检索并返回与用户查询最接近的结果，使用基于字符串的编辑距离进行拼写校正（使用Big.txt作为单词列表）。
5. 索引压缩器（compressIndex.py）：使用可变长字节编码和gap-encoding的方法对索引列表进行encode处理，在结果输出时再通过decode模块还原到真实结果，实现空间压缩。
6. 评分排序：用于实现检索结果的排序，已知的评分函数有余弦相似度、静态得分、近邻性等，采用机器学习的方法将这些评分组合得到最优组合。

## 模块优化:
1. 查询分析器：查询分析器除了可以对用户输入的查询字符串堪称一个短语进行查询外，还应当考虑短语对应文档篇目较少的情况：
    1. 如果包含短语ABC的文档数目少于10篇，那么将原始查询看成AB和BC两个查询短语，同样使用向量空间的方法进行计算。
    2. 如果查询结果仍然少于10个，重新利用向量空间模型进行求解，认为三个查询词项A，B，C是相互独立的。
2. 查询分析器：查询分析时希望得到处理查询的最佳顺序，原则是按照文档频率的顺序进行处理：先处理文档频率小的，再处理文档频率大的，按照结果从小到大执行AND操作。

## 运行
```python
pip install nltk
nltk.download('stopwords')
```

```python
python establishIndex.py # 构建倒排索引表
python boolRetrieval.py # 进行布尔检索
```


