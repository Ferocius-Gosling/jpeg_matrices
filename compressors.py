from bitarray import bitarray, util
from matrix import Matrix
import copy


length_freqs = {3: 3497, 1: 15113, 2: 3199, 4: 1351, 15: 2688, 12: 3135, 25: 6142, 17: 1300, 19: 4730, 21: 7832,
                10: 5518, 20: 6381, 6: 5382, 7: 1532, 22: 660, 16: 277, 13: 4227, 29: 197, 28: 565, 18: 3086, 23: 2092,
                36: 569, 26: 1829, 14: 3093, 5: 2438, 44: 683, 35: 788, 34: 1133, 24: 2830, 9: 3353, 33: 1022, 42: 332,
                41: 189, 43: 728, 27: 428, 30: 211, 54: 246, 8: 2093, 32: 967, 39: 685, 31: 461, 40: 646, 45: 179,
                38: 259, 47: 284, 11: 2502, 46: 54, 52: 40, 37: 138, 53: 33, 48: 191, 51: 75, 61: 57, 60: 18, 55: 409,
                64: 8, 59: 35, 58: 37, 49: 134, 56: 20, 50: 69, 62: 14, 63: 8, 57: 24}
huffman = util.huffman_code(length_freqs, endian='big')


class ExpGolombCompressor:
    def __init__(self):
        pass

    def compress(self, matrix, first=False):     # пусть возвращает массив битов. а не матрицу.
        matrix_bits = bitarray()
        index = 0
        for i in matrix.values:
            if i:
                b_number = bin(abs(i))
                length = len(b_number) - 2
                if first and index == 0:
                    length = 8 - length
                sign = 0 if i < 0 else 1
                matrix_bits.extend('1' * length + '0')
                matrix_bits.append(sign)
                matrix_bits.extend(b_number[3:])
            else:
                matrix_bits.append(0)
            index += 1
        return matrix_bits


class AdvancedExpGolombCompressor:
    def __init__(self):
        self.window = Matrix([0 for _ in range(64)])
        self.compressor = ExpGolombCompressor()

    def compress(self, matrix):     # ищем S. S = A - W
        shift_bits = bitarray()
        matrix_bits = bitarray()
        final_bits = bitarray()
        shifts = matrix - self.window
        self.window = copy.deepcopy(matrix)
        erase_zero(shifts)
        erase_zero(matrix)

        bin_s_length = huffman[shifts.length]
        bin_m_length = huffman[matrix.length]
        shift_bits.extend(bin_s_length)
        shift_bits.extend(self.compressor.compress(shifts))
        matrix_bits.extend(bin_m_length)
        matrix_bits.extend(self.compressor.compress(matrix, True))

        if len(shift_bits) > len(matrix_bits):
            final_bits.append(1)
            final_bits.extend(matrix_bits)
        else:
            final_bits.append(0)
            final_bits.extend(shift_bits)

        return final_bits


def erase_zero(matrix):
    pos = 0
    for i in range(matrix.length): # нужен индекс последнего ненулевого прикола
        if matrix[i]:
            pos = i
    matrix.values = matrix.values[:pos + 1]


