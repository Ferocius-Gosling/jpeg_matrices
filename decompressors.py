import copy

from bitarray import bitarray, util
from matrix import Matrix


length_freqs = {3: 3497, 1: 15113, 2: 3199, 4: 1351, 15: 2688, 12: 3135, 25: 6142, 17: 1300, 19: 4730, 21: 7832,
                10: 5518, 20: 6381, 6: 5382, 7: 1532, 22: 660, 16: 277, 13: 4227, 29: 197, 28: 565, 18: 3086, 23: 2092,
                36: 569, 26: 1829, 14: 3093, 5: 2438, 44: 683, 35: 788, 34: 1133, 24: 2830, 9: 3353, 33: 1022, 42: 332,
                41: 189, 43: 728, 27: 428, 30: 211, 54: 246, 8: 2093, 32: 967, 39: 685, 31: 461, 40: 646, 45: 179,
                38: 259, 47: 284, 11: 2502, 46: 54, 52: 40, 37: 138, 53: 33, 48: 191, 51: 75, 61: 57, 60: 18, 55: 409,
                64: 8, 59: 35, 58: 37, 49: 134, 56: 20, 50: 69, 62: 14, 63: 8, 57: 24}
huffman = util.huffman_code(length_freqs, endian='big')


class ExpGolombDecompressor:
    def __init__(self):
        self.window = Matrix([0 for _ in range(64)])
        pass

    def decompress(self, bit_string: bitarray):
        matrices = []
        index = 0
        while index < len(bit_string):
            first_bit = bit_string[index]
            index += 1
            length = self.read_matrix_length(index, bit_string)
            index += len(huffman[length])
            matrix = Matrix([0] * 64)
            for i in range(length):
                n_length, index = self.read_number_length(index, bit_string, i, first_bit)
                if not n_length:
                    continue
                n_length -= 1
                n_sign = 1 if bit_string[index] else -1
                index += 1
                n_buff = bitarray('1')
                for j in range(n_length):
                    n_buff.append(bit_string[index])
                    index += 1
                n_number = int(n_buff.to01(), 2)
                matrix[i] = n_sign * n_number
            if not first_bit:
                final_matrix = self.window + matrix
                self.window = copy.deepcopy(final_matrix)
            else:
                self.window = copy.deepcopy(matrix)
                final_matrix = matrix
            matrices.append(final_matrix)
        self.window = Matrix([0 for _ in range(64)])
        return matrices

    def read_matrix_length(self, index: int, bit_string: bitarray):
        decoded_length = bit_string[index:index+14].iterdecode(huffman)
        return next(decoded_length)

    def read_number_length(self, index, bit_string, i, first_bit):
        length = 0
        try:
            while bit_string[index]:
                index += 1
                length += 1
        except IndexError:
            raise IndexError(f'Error at index {index}')
        index += 1
        if not i and first_bit and length != 0:
            length = 8 - length
        return length, index
