class IdMap:
    """IdMap: 用于将字符串和数字ID进行相互映射,以满足term和termID,doc和docID之间的转换需求."""

    def __init__(self):
        self.str_to_id = {}
        self.id_to_str = []

    def __len__(self):
        # 返回存储在IdMap中的词的数量
        return len(self.id_to_str)

    def _get_str(self, i):
        # 返回i：ID对应的字符串.
        return self.id_to_str[i]

    def _get_id(self, s):
        # 返回s: doc对应的ID
        if s not in self.str_to_id.keys():  # 没有在字典中，就分别在字典和list中添加
            self.str_to_id[s] = len(self.id_to_str)
            self.id_to_str.append(s)
        return self.str_to_id[s]

    def __getitem__(self, key):
        # 如果key是一个整数，使用_get_str
        # 如果key是字符，使用use _get_id
        if type(key) is int:
            return self._get_str(key)
        elif type(key) is str:
            return self._get_id(key)
        else:
            raise TypeError

# 测试代码
# testIdMap = IdMap()
# testIdMap._get_id('adwwd')
# print(testIdMap._get_id('asdwd'))
# testIdMap._get_id('dawd')
# print(testIdMap._get_str(0))
