"""
    Author: minsung kim
    since: 2024-10-01

    ring polynomial 구현
"""
import numpy as np
from utils import crange

class Rq(object):
    '''
        Ring-Polynomial: Fq[x] / (x^n + 1)
        계수 범위 => (−q/2, q/2]
    '''
    def __init__(self, coeffs, q):
        '''
        # Args
            coeffs: 계수
        '''
        n = len(coeffs)

        f = np.zeros((n+1), dtype=np.int64)  # x^n + 1
        f[0] = f[-1] = 1
        f = np.poly1d(f)
        self.f = f

        self.q = q
        coeffs = np.array(coeffs, dtype=np.int64) % q
        coeffs = crange(coeffs, q)
        self.poly = np.poly1d(np.array(coeffs, dtype=np.int64))

    def __len__(self):
        return len(self.poly)  # degree of a polynomial

    def __add__(self, other):
        coeffs = np.polyadd(self.poly, other.poly).coeffs
        return Rq(coeffs, self.q)
    
    def __sub__(self, other):
        coeffs = np.polysub(self.poly, other.poly).coeffs
        return Rq(coeffs, self.q)

    def __mul__(self, other):
        q, r = np.polydiv(np.polymul(self.poly, other.poly), self.f)
        coeffs = r.coeffs
        return Rq(coeffs, self.q)

    def __rmul__(self, integer):
        coeffs = (self.poly.coeffs * integer)
        return Rq(coeffs, self.q)

    def __pow__(self, integer):
        if integer == 0:
            return Rq([1], self.q)
        ret = self
        for _ in range(integer-1):
            ret *= ret
        return ret
