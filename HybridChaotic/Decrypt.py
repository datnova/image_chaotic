import numpy as np
from copy import deepcopy

class DecryptImg:
    def __init__(self, p: int, q: int, l: int, x: int, len_mantissa = 3) -> None:
        self.p = p
        self.q = q
        self.l = l
        self.mantissa = 10 ** len_mantissa
        self.x = (x * self.mantissa) / self.mantissa
        self.MAX = 10079
    
    def Swap_pixel(self, img, first_coor: tuple[int, int], second_coor: tuple[int, int]) -> None:
        x_1, y_1 = first_coor
        x_2, y_2 = second_coor
        first_pixel = deepcopy(img[y_1][x_1])
        second_pixel = deepcopy(img[y_2][x_2])
        img[y_1][x_1] = second_pixel
        img[y_2][x_2] = first_pixel

    def Rev_cal_cordinate(self, coor: tuple[int, int], col: int, row: int) -> tuple[int, int]:
        '''
        [PQ + 1   -P]   [x']   [((PQ + 1) * x')  +  (-P * y')]   [x]
        [           ] * [  ] = [                             ] = [ ]
        [  -Q      1]   [y']   [    (Q * x')     +      y'   ]   [y]
        '''
        x, y = coor
        new_x = (self.p * self.q + 1) * x + (-self.p * y)
        new_y = (self.q * x) + y
        return new_x % col, new_y % row

    def Rev_ACM(self, img: np.ndarray) -> None:
        col, row, _ = img.shape
        for i in range(max(col, row)):
            for j in range(row - 1, -1, -1):
                for k in range(col - 1, -1, -1):
                    new_x, new_y = self.Rev_cal_cordinate((k, j), col, row)
                    self.Swap_pixel(img, (k, j), (new_x, new_y))

    def pixel_opposite(self, coor: tuple[int, int], max_x: int, max_y: int) -> tuple[int, int]:
        new_x = max_x - coor[0] - 1
        new_y = max_y - coor[1] - 1
        return new_x, new_y
    
    def Swap_next(self, shape: tuple[int, int], coor: tuple[int, int]) -> None:
        row, col = shape
        step = int(np.log2(max(row, col)))
        col_barrier = [col // (2 * i) for i in range(1, int(np.log2(col)))][::-1] + [col]
        row_barrier = [row // (2 * i) for i in range(1, int(np.log2(row)))][::-1] + [row]
        for _ in range(step):
            max_x = next(idx for idx, value in enumerate(col_barrier) if value > coor[0])
            max_y = next(idx for idx, value in enumerate(row_barrier) if value > coor[1])
            coor = self.pixel_opposite(coor, max_x, max_y)

        return coor
    
    def Shuffle_img(self, img: np.ndarray) -> None:
        row, col, _ = img.shape
        for i in range((row + 1) // 2):
            for j in range(col):
                x, y = self.Swap_next((row, col), (j, i))
                self.Swap_pixel(img, (x, y), (j, i))

    def Logistic_gen(self) -> int:
        while True:
            self.x = int(self.l * self.x * (1 - self.x) * self.mantissa) / self.mantissa
            yield self.x
    
    def Rev_diffusion(self, img: np.ndarray) -> np.ndarray:
        # create logistic map
        row, col, _ = img.shape
        logistic_gen = self.Logistic_gen() 
        S_x = sorted([next(logistic_gen) for _ in range((col + 1) // 2)])
        S_y = sorted([next(logistic_gen) for _ in range((col + 1) // 2)])
        res_img = np.zeros(shape=img.shape)
        
        # xor img with logistic map
        for i in range(1, row + 1):
            for j in range(1, col + 1):
                if (j % 2 == 0):
                    u = int((S_x[j // 2] * self.MAX) % 256)
                else:
                    u = int((S_y[j // 2] * self.MAX) % 256)
                # print(u)
                res_img[i - 1][j - 1][0] = int(img[i % row][j % col][0]) ^ u       
                res_img[i - 1][j - 1][1] = int(img[i % row][j % col][1]) ^ u
                res_img[i - 1][j - 1][2] = int(img[i % row][j % col][2]) ^ u
                
        return res_img   

    def Run(self, img: np.ndarray) -> np.ndarray:
        temp_img = deepcopy(img)
        temp_img = self.Rev_diffusion(temp_img)
        self.Shuffle_img(temp_img)
        self.Rev_ACM(temp_img)
        return temp_img
    