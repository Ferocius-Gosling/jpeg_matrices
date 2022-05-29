from copy import deepcopy
from typing import List
from jpeg_processing import read, erase_zero
from matrix import Matrix
from collections import defaultdict
from matplotlib import pyplot as plt
from bitarray import util

length_freqs = {3: 3497, 1: 15113, 2: 3199, 4: 1351, 15: 2688, 12: 3135, 25: 6142, 17: 1300, 19: 4730, 21: 7832,
                10: 5518, 20: 6381, 6: 5382, 7: 1532, 22: 660, 16: 277, 13: 4227, 29: 197, 28: 565, 18: 3086, 23: 2092,
                36: 569, 26: 1829, 14: 3093, 5: 2438, 44: 683, 35: 788, 34: 1133, 24: 2830, 9: 3353, 33: 1022, 42: 332,
                41: 189, 43: 728, 27: 428, 30: 211, 54: 246, 8: 2093, 32: 967, 39: 685, 31: 461, 40: 646, 45: 179,
                38: 259, 47: 284, 11: 2502, 46: 54, 52: 40, 37: 138, 53: 33, 48: 191, 51: 75, 61: 57, 60: 18, 55: 409,
                64: 8, 59: 35, 58: 37, 49: 134, 56: 20, 50: 69, 62: 14, 63: 8, 57: 24}
huffman = util.huffman_code(length_freqs, endian='big')


def analyze():
    matrices, size = read()
    name_view_data = 'diff'
    zigzag_matrix = analyze_length_after_zigzag(matrices)
    bit_length = dict()
    for i in range(1, 8):
        bit_length[i] = analyze_how_many_numbers_more_than_number(i, matrices)
    max_numbers = analyze_max_numbers(matrices)
    max_numbers = [max_numbers[i] for i in max_numbers]
    max_numbers_matrix = Matrix(max_numbers)
    diff_matrices = analyze_how_many_diff_matrix_are_more_then_original(matrices)
    choosing_data = {'zigzag': zigzag_matrix, 'diff' : diff_matrices}
    for i in range(1, 8):
        choosing_data[f'bit_length_{i}'] = bit_length[i]

    d = []
    for i in choosing_data[name_view_data]:
        d.append(i)

    x = d
    y = []

    for i in x:
        y.append(choosing_data[name_view_data][i])

    plt.bar(x, y)
    plt.show()

    print(max_numbers_matrix)


def analyze_max_numbers(matrices: List[Matrix]):
    max_numbers = defaultdict(int)
    for m in matrices:
        for i in range(64):
            max_numbers[i] = abs(m[i]) if abs(m[i]) > max_numbers[i] else max_numbers[i]
    print(max_numbers)
    return max_numbers


def analyze_length_after_zigzag(matrices: List[Matrix]):
    d = defaultdict(int)
    m_copy = deepcopy(matrices)
    for m in m_copy:
        erase_zero(m)
        d[m.length] += 1
    print(d)
    return d


def analyze_how_many_diff_matrix_are_more_then_original(matrices: List[Matrix]):
    d = defaultdict(int)
    m_copy = deepcopy(matrices)
    diff_length = 0
    current_length = 0
    prev = Matrix([0 for _ in range(64)])
    for m in m_copy:
        diff = m - prev
        prev = deepcopy(m)
        erase_zero(diff)
        for i in range(diff.length):
            if not diff[i]:
                diff_length += 1
                continue
            true_length = len(bin(abs(diff[i]))) - 2
            golomb_length = 1 + 2 * true_length
            diff_length += golomb_length
        diff_length += len(huffman[diff.length])
        erase_zero(m)
        for i in range(m.length):
            if not m[i]:
                current_length += 1
                continue
            true_length = len(bin(abs(m[i]))) - 2
            golomb_length = 1 + 2 * true_length
            if i == 0:
                golomb_length = 9
            current_length += golomb_length
        current_length += len(huffman[m.length])
        if diff_length > current_length:
            d['matrix'] += 1
        else:
            d['shifts'] += 1
        diff_length = 0
        current_length = 0
    print(d)
    return d


def analyze_how_many_numbers_more_than_number(n, matrices):
    d = defaultdict(int)
    m_copy = deepcopy(matrices)
    for m in m_copy:
        for i in range(m.length):
            if not m[i]:
                continue
            if len(bin(abs(m[i]))) - 2 == n:
                d[i] += 1
    print(f'n = {n}\n{d}')
    return d
