import numpy as np
from copy import deepcopy

class HybridChaotic:
    def __init__(self, p: int, q: int, l: int, x: int, len_mantissa = 3) -> None:
        self.p = p
        self.q = q
        self.l = l
        self.mantissa = 10 ** len_mantissa
        self.x = (x * self.mantissa) / self.mantissa
        self.MAX = 10079
        
    def Cal_cordiante(self, coor: tuple(int. int), col: int, row: int) -> tuple(int, int):
        '''
        [1    P  ]   [x]   [(1 * x)      (P * y)   ]   [x']
        [        ] * [ ] = [                       ] = [  ]
        [Q PQ + 1]   [y]   [(Q * x)  ((PQ + 1) * y)]   [y']
        '''
        x, y = coor
        new_x = (x + self.p * y) % col
        new_y = (x * self.q + (self.p * self.q + 1) * y) % row
        
        return new_x, new_y 
    
    def ACM(self, img: np.ndarray) -> None:
        col, row, _ = img.shape
        for i in range(col + row):
            for j in range(row):
                for k in range(col):
                    new_x, new_y = self.cal_cordiante((k, j), col, row)
                    img[new_y][new_x], img[j][k] = img[j][k], img[new_y][new_x]
    
    def pixel_opposite(self, coor: tuple(int, int), max_x: int, max_y: int) -> tuple(int, int):
        new_x = max_x - coor[0] - 1
        new_y = max_y - coor[1] - 1
        return new_x, new_y
    
    def Swap_next(self, shape: tuple(int, int), coor: tuple(int, int)) -> None:
        row, col = shape
        step = np.log2(max(row, col))
        col_barrier = [col // (2 * i) for i in range(1, np.log2(col))][::-1] + [col]
        row_barrier = [row // (2 * i) for i in range(1, np.log2(row))][::-1] + [row]
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
                img[i][j], img[y][x] = img[y][x], img[i][j]
        
    def Logistic_gen(self) -> int:
        while True:
            self.x = int(self.l * self.x * (1 - self.x) * self.mantissa) / self.mantissa
            yield self.x
    
    def Diffusion(self, img: np.ndarray) -> np.ndarray:
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
                    u = int((S_x[j // 2] * self.MAX) % 255)
                else:
                    u = int((S_y[j // 2] * self.MAX) % 255)
                res_img[i % row][j % col][0] = img[(i - 1) % row][(j - 1) % col][0] ^ u       
                res_img[i % row][j % col][1] = img[(i - 1) % row][(j - 1) % col][1] ^ u
                res_img[i % row][j % col][2] = img[(i - 1) % row][(j - 1) % col][2] ^ u
                
        return res_img   
    
    def Run(self, img: np.ndarray) -> np.ndarray:
        temp_img = deepcopy(img)
        self.ACM(temp_img)
        self.Shuffle_img(temp_img)
        return self.Diffusion(temp_img)
    
    