import array
class CompressedPostings:

    @staticmethod
    def vbcode(n):
        # vb编码：一种可变长的字节编码
        byte = []
        while True:
            byte.append(n % 128)
            if n < 128:
                break
            n = n // 128
        byte[0] += 128
        byte = list(reversed(byte))
        return byte

    @staticmethod
    def encode(postings_list):
        # gap-encoding 压缩差值gap = posting - last
        bytestream = []
        last = 0
        for posting in postings_list:
            gap = posting - last
            last = posting
            byte = CompressedPostings.vbcode(gap)
            bytestream.extend(byte)
        return array.array('B', bytestream).tobytes()

    @staticmethod
    def decode(encoded_postings_list):
        decoded_postings_list = array.array('B')
        decoded_postings_list.frombytes(encoded_postings_list)
        numbers = []
        n = 0
        for i, byte in enumerate(decoded_postings_list):
            if byte < 128:
                n = 128 * n + byte
            else:
                n = 128 * n + byte - 128
                numbers.append(n)
                n = 0
        prefix_sum = 0
        res = []
        for num in numbers:
            prefix_sum += num
            res.append(prefix_sum)
        return res
# a = CompressedPostings.encode([1,2,3])
# print(a)
# b = CompressedPostings.decode(a)
# print(b)


