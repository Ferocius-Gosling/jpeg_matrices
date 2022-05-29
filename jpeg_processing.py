from typing import List
from matrix import Matrix
from compressors import AdvancedExpGolombCompressor
from decompressors import ExpGolombDecompressor
from bitarray import bitarray, util
import os.path

length_freqs = {3: 3497, 1: 15113, 2: 3199, 4: 1351, 15: 2688, 12: 3135, 25: 6142, 17: 1300, 19: 4730, 21: 7832,
                10: 5518, 20: 6381, 6: 5382, 7: 1532, 22: 660, 16: 277, 13: 4227, 29: 197, 28: 565, 18: 3086, 23: 2092,
                36: 569, 26: 1829, 14: 3093, 5: 2438, 44: 683, 35: 788, 34: 1133, 24: 2830, 9: 3353, 33: 1022, 42: 332,
                41: 189, 43: 728, 27: 428, 30: 211, 54: 246, 8: 2093, 32: 967, 39: 685, 31: 461, 40: 646, 45: 179,
                38: 259, 47: 284, 11: 2502, 46: 54, 52: 40, 37: 138, 53: 33, 48: 191, 51: 75, 61: 57, 60: 18, 55: 409,
                64: 8, 59: 35, 58: 37, 49: 134, 56: 20, 50: 69, 62: 14, 63: 8, 57: 24}
huffman = util.huffman_code(length_freqs, endian='big')


def process():
    shifts_compressor = AdvancedExpGolombCompressor()
    exp_gol_decompressor = ExpGolombDecompressor()

    bits = bitarray(endian='big')

    n, size = read()

    for m in n:
        bits.extend(shifts_compressor.compress(m))

    print(size)
    print(len(n))
    print(len(bits))
    bs = make_byte_array_from_bits(bits)
    decompressed = exp_gol_decompressor.decompress(bits)

    if len(n) != len(decompressed):
        print(f'length different, before compress {len(n)}, after compress {len(decompressed)}')

    first = 0
    for i in range(len(n)):
        n[i].values.extend([0 for _ in range(64 - n[i].length)])
        if n[i] == decompressed[i]:
            continue
        else:
            if not first:
                first = i
            else:
                continue
            print(f'wrong compress at matrix {i}')
    print('end of decompressing')

    advanced_shifts = write_file('adv_shifts.txt', bs)
    exp_gol_size = os.path.getsize('exp_golomb.txt')     # вот это надо улучшить.
    print(f'size exp_golomb = {exp_gol_size}, advanced shifts = {advanced_shifts}, k = {exp_gol_size / advanced_shifts}')
    return


def erase_zero(matrix):
    pos = 0
    for i in range(matrix.length): # нужен индекс последнего ненулевого прикола
        if matrix[i]:
            pos = i
    matrix.values = matrix.values[:pos + 1]


def write_file(name: str, byte_line: bytes):
    size = 0
    with open(name, 'wb') as file:
        file.write(byte_line)
        size = file.tell()
    return size


def read():
    size = 0
    matrices = []
    with open('matrices.txt') as matr_raw:
        lines = matr_raw.readlines()    # прочитали все строчки.
        raw_matr = []
        outer_index = 0
        for raw_line in lines:
            if len(raw_line) == 1:  # момент когда новую строку читаем
                matrices.append(Matrix(zigzag(raw_matr)))
                raw_matr = []
                outer_index = 0
                continue
            raw_matr.append([])
            symbols = raw_line.split(' ')
            for sym in symbols:
                if sym == '\n':
                    continue
                raw_matr[outer_index].append(int(sym))
            outer_index += 1
        size = matr_raw.tell()
    return matrices, size


def zigzag(matrix: List[List[int]]):
    m = []
    for index in range(1, len(matrix) + 1):
        m_slice = [i[:index] for i in matrix[:index]]
        m_diag = [m_slice[i][len(m_slice) - i - 1] for i in range(len(m_slice))]
        if len(m_diag) % 2:
            m_diag.reverse()
        m += m_diag
    for index in range(1, len(matrix)):
        m_slice = [i[index:] for i in matrix[index:]]
        m_diag = [m_slice[i][len(m_slice) - i - 1] for i in range(len(m_slice))]
        if len(m_diag) % 2 == 1:
            m_diag.reverse()
        m += m_diag
    return m


def make_byte_array_from_bits(bits: bitarray):
    return bits.tobytes()


def get_max_value(nums: list):
    return max(nums)


def get_min_value(nums: list):
    return min(nums)
