import numpy as np
from copy import deepcopy

MAX = 10079

class DecryptImg:
    def __init__(self, p: int, q: int, l: int, x: int, len_mantissa = 5) -> None:
        self.p = p
        self.q = q
        self.qp1 = None
        self.l = l
        self.len_mantissa = len_mantissa
        self.x = round(x, len_mantissa)
    
    def Optimize_pq(self, n):
        self.q %= n
        self.p %= n
        self.qp1 = (self.p * self.q + 1) % n

    def Rev_ACM(self, img: np.ndarray) -> np.ndarray:
        '''
        [PQ + 1   -P]   [x']   [((PQ + 1) * x')  +  (-P * y')]   [x]
        [           ] * [  ] = [                             ] = [ ]
        [  -Q      1]   [y']   [    (-Q * x')    +      y'   ]   [y]
        '''
        row = img.shape[0]
        x,y = np.meshgrid(range(row),range(row))
        xmap = (self.qp1 * x + (-self.p * y)) % row
        ymap = ((-self.q * x) + y) % row
        for _ in range(row // 2):
            img = img[ymap, xmap]
        return img

    def Logistic_gen(self) -> int:
        while True:
            self.x = round(self.l * self.x * (1 - self.x), self.len_mantissa)
            yield int(self.x * MAX) % 256
    
    def Rev_diffusion(self, img: np.ndarray) -> np.ndarray:
        # create logistic map
        row, col, _ = img.shape
        logistic_gen = self.Logistic_gen() 
        S_x = sorted([next(logistic_gen) for _ in range((col + 2) // 2)])
        S_y = sorted([next(logistic_gen) for _ in range((col + 2) // 2)])
        # res_img = np.zeros(shape=img.shape)
        res_img = np.empty(shape=img.shape, dtype=np.uint8)
        
        # xor img with logistic map
        for i in range(1, row + 1):
            for j in range(1, col + 1):
                if (j % 2 == 0):
                    u = S_x[j // 2]
                else:
                    u = S_y[j // 2]
                res_img[i - 1][j - 1][0] = int(img[i % row][j % col][0]) ^ u       
                res_img[i - 1][j - 1][1] = int(img[i % row][j % col][1]) ^ u
                res_img[i - 1][j - 1][2] = int(img[i % row][j % col][2]) ^ u
                
        return res_img   

    def Run(self, img: np.ndarray) -> np.ndarray:
        # copy img
        temp_img = deepcopy(img)
        
        # optimize value
        self.Optimize_pq(temp_img.shape[0])
        
        # decrypt img
        temp_img = self.Rev_diffusion(temp_img)
        temp_img = self.Rev_ACM(temp_img)

        return temp_img
    