import collections
import re


class SpellingCheck:
    def __init__(self):
        # Corpus: Big.txt: http://norvig.com/big.txt
        # Gutenberg语料库数据, 维基词典, 英国国家语料库中最常用单词列表
        with open('cache/big.txt', 'r') as f:
            WORDS = self.tokens(f.read())

        self.WORD_COUNTS = collections.Counter(WORDS)

    # 基于字符串的编辑距离进行拼写校正(动态规划算法)
    # Or NLTK模块中edit_distance()函数
    def tokens(self, text):
        """
        Get all words from the corpus
        """
        return re.findall('[a-z]+', text.lower())

    def known(self, words):
        # 返回实际在我们的WORD_COUNTS字典中的单词子集
        return {w for w in words if w in self.WORD_COUNTS}

    def edits0(self, word):
        # 返回所有与输入词相差0个编辑的字符串的所有字符串
        return {word}

    def edits1(self, word):
        # 返回所有与输入词相差1个编辑的字符串的所有字符串
        alphabet = ''.join([chr(ord('a') + i) for i in range(26)])

        def splits(word):
            return [(word[:i], word[i:])
                    for i in range(len(word) + 1)]

        pairs = splits(word)
        deletes = [a + b[1:] for (a, b) in pairs if b]
        transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
        replaces = [a + c + b[1:] for (a, b) in pairs for c in alphabet if b]
        inserts = [a + c + b for (a, b) in pairs for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        # 返回所有与输入词相差2个编辑的字符串的所有字符串
        return {e2 for e1 in self.edits1(word) for e2 in self.edits1(e1)}

    def correct(self, word):
        # 返回正确拼写
        # 优先级为编辑距离0，然后是1，然后是2
        candidates = (self.known(self.edits0(word)) or
                      self.known(self.edits1(word)) or
                      self.known(self.edits2(word)) or
                      {word})

        return max(candidates, key=self.WORD_COUNTS.get)

    def correctMatch(self, match):
        word = match.group()

        def case_of(text):
            return (str.upper if text.isupper() else
                    str.lower if text.islower() else
                    str.title if text.istitle() else
                    str)

        return case_of(word)(self.correct(word.lower()))

    def spellingCheck(self, text):
        return re.sub('[a-zA-Z]+', self.correctMatch, text)

    def reSub(self, text):
        remove_chars = '[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        return re.sub(remove_chars, '', text)


original_word = 'fianlly'
# original_word = 'correcat'
# original_word = 'digitl'
# original_word = 'firea'
correct_word = SpellingCheck().spellingCheck(original_word)
# print('Original word:%s\nCorrect word:%s' % (original_word, correct_word))
