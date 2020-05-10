import numpy as np
import random


class MagicSquare():
    def __init__(self, n):
        self.n = n
        self.square = self.generate()
        self.magic_number = self.calculate_magic_number()

    def generate(self):
        # see https://blogs.mathworks.com/cleve/2012/11/05/magic-squares-part-2-algorithms/
        if self.n % 4 == 0:
            square = np.arange(1, self.n*self.n + 1).reshape(self.n, self.n)
            I, J = np.mgrid[1:self.n+1, 1:self.n+1]
            K = np.floor(np.mod(I,4)/2) == np.floor(np.mod(J,4)/2)
            square[K] = self.n*self.n + 1 - square[K]
        elif self.n % 4  != 0 and self.n % 2 == 0:
            # TODO: singly-even
            raise NotImplementedError
        else:
            # odd
            I, J = np.mgrid[1:self.n+1, 1:self.n+1]
            A = np.mod(I + J + (self.n - 3)/2, self.n)
            B = np.mod(I + 2*J - 2, self.n)
            square = self.n * A + B + 1

        return square

    def calculate_magic_number(self):
        return self.n/2 * (self.n * self.n + 1)

    def swap_rows(self, row_1, row_2):
        self.square[[row_1, row_2]] = self.square[[row_2, row_1]]

    def swap_cols(self, col_1, col_2):
        self.square[:, [col_1, col_2]] = self.square[:, [col_2, col_1]]

    def roll(self, direction, axis):
        self.square = np.rolls(self.square, direction, axis)

    def roll_vertical(self, no_rolls = 1):
        self.square = np.roll(self.square, no_rolls * -1, axis=0)

    def roll_horizontal(self, no_rolls = 1):
        self.square = np.roll(self.square, no_rolls * -1, axis=1)

    def complement(self):
        self.square = self.n*self.n+1 - self.square

    def check_magic(self):
        rows = self.check_magic_rows()
        cols = self.check_magic_cols()
        diag = self.check_magic_diag()
        anti_diag = self.check_magic_anti_diag()
        return rows == cols == diag == anti_diag

    def check_magic_rows(self):
        for row in self.square:
            total = sum(row)
            if total != self.magic_number:
                return False

        return True

    def check_magic_cols(self):
        for col in self.square.T:
            total = sum(col)
            if total != self.magic_number:
                return False

        return True

    def check_magic_diag(self):
        return sum(self.square.diagonal()) == self.magic_number

    def check_magic_anti_diag(self):
        return sum(np.fliplr(self.square).diagonal()) == self.magic_number
            
    def __repr__(self):
        return np.array_repr(self.square)
        

class PanDiagonalMagicSquare(MagicSquare):
    def __init__(self, n):
        self.n = n
        self.magic_number = MagicSquare.calculate_magic_number(self)
        self.square = self.generate()
        
    def generate(self):
        if self.n == 4:
            # could also use these seeds to generate order-4 squares:
            # http://www.magic-squares.net/order4list.htm#Group%20I
            # see https://en.wikipedia.org/wiki/Pandiagonal_magic_square
            a = 1
            seed = [1, 2, 4, 8]
            random.shuffle(seed)
            b, c, d, e = [i for i in seed]
            return np.array([
                [a, a+b+c+e, a+c+d, a+b+d+e],
                [a+b+c+d, a+d+e, a+b, a+c+e],
                [a+b+e, a+c, a+b+c+d+e, a+d],
                [a+c+d+e, a+b+d, a+e, a+b+c]
            ])
        else:
            raise NotImplementedError

    def shuffle(self):
        horizontal_no = random.randrange(1,4)
        vertical_no = random.randrange(1,4)
        self.roll_horizontal(horizontal_no)
        self.roll_vertical(vertical_no)

    def check_pan_magic(self):
        diagonals = self.check_pan_diagonals()
        return MagicSquare.check_magic(self) == diagonals

    def check_pan_diagonals(self):
        for diag in range(1, self.n):
            opposite_diag = diag - self.n

            # get indices
            diag_indeces = self.kth_diag_indeces(diag)
            opposite_diag_indeces = self.kth_diag_indeces(opposite_diag)

            diag_total = sum(self.square[diag_indeces]) + sum(self.square[opposite_diag_indeces])
            if diag_total != self.magic_number:
                return False

        return True

    def kth_diag_indeces(self, k):
        rows, cols = np.diag_indices_from(self.square)
        if k < 0:
            return rows[-k:], cols[:k]
        elif k > 0:
            return rows[:-k], cols[k:]
        else:
            return rows, cols

    def magic_trick_representation(self):
        str_repr = self.square.astype(str)
        str_repr[str_repr == '13'] = 'n - 21'
        str_repr[str_repr == '14'] = 'n - 20'
        str_repr[str_repr == '15'] = 'n - 19'
        str_repr[str_repr == '16'] = 'n - 18'
        print(str_repr)

