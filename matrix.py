class Matrix:                   # по факту здесь не матрицы а числа, не считая нули после финала.
    def __init__(self, nums):   # сначала конечно с нулями. потом без. но здесь уже после зигзагового обхода.
        # self.length = len(nums)
        self.values = nums

    def __getitem__(self, index):
        return self.values[index]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __add__(self, other):
        if type(other) != Matrix:
            raise TypeError
        m = Matrix([0 for i in range(64)])
        for i in range(max(self.length, other.length)):
            m[i] = self[i] + other[i]
        return m

    def __sub__(self, other):
        if type(other) != Matrix:
            raise TypeError
        m = Matrix([0 for i in range(64)])
        for i in range(max(self.length, other.length)):
            m[i] = self[i] - other[i]
        return m

    def __eq__(self, other):
        if type(other) != Matrix:
            raise TypeError
        if other.length != self.length:
            return False
        for i in range(self.length):
            if self[i] != other[i]:
                return False
        return True

    def __str__(self):
        anti_zigzag = self.anti_zigzag()
        string = [[str(y) for y in x] for x in anti_zigzag]
        new_line = ''
        for i in range(8):
            for j in range(8):
                new_line += f'{string[i][j]} '
            new_line += '\n'
        new_line += '\n'
        # print(new_line)
        return new_line

    @property
    def length(self):
        return len(self.values)

    def anti_zigzag(self):
        m = []
        for i in range(8):
            m.append([0, 0, 0, 0, 0, 0, 0, 0])
        n = 8
        index = 0
        border_0 = 0
        for t in range(n, 0, -1): # идём от [n-t][t-1] до [t-1][n-t]
            border_n_t = n - t
            if t % 2:
                index = self.diag_i_0(border_n_t, border_0, m, index, True)
            else:
                index = self.diag_j_0(border_n_t, border_0, m, index, True)
        border_0 = 7
        for t in range(n-1, 0, -1):
            border_n_t = n - t
            if t % 2:
                index = self.diag_i_0(border_n_t, border_0, m, index, False)
            else:
                index = self.diag_j_0(border_n_t, border_0, m, index, False)
        return m

    def diag_j_0(self, border_n_t, border_0, m, index, is_upper):
        j = 0
        i = border_n_t
        if is_upper:
            while j <= border_n_t and i >= border_0:
                m[i][j] = self[index]
                j += 1
                i -= 1
                index += 1
        else:
            i = border_n_t
            j = 7      # это 1            # а это 7 должно быть
            while j >= border_n_t and i <= border_0:
                m[i][j] = self[index]
                j -= 1
                i += 1
                index += 1
        return index

    def diag_i_0(self, border_n_t, border_0, m, index, is_upper):
        i = 0
        j = border_n_t
        if is_upper:
            while i <= border_n_t and j >= border_0:
                m[i][j] = self[index]
                i += 1
                j -= 1
                index += 1
        else:
            i = 7
            j = border_n_t
            while i >= border_n_t and j <= border_0:
                m[i][j] = self[index]
                j += 1
                i -= 1
                index += 1
        return index
