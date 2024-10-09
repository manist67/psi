"""
Author: minsung kim

RLWE를 이용한 동형 암호 구현

"""
import numpy as np
from Rq import Rq
from utils import discrete_uniform, discrete_gaussian


class RLWE:
    def __init__(self, n, p, t, std):
        assert np.log2(n) == int(np.log2(n))
        self.n = n
        self.p = p
        self.t = t
        self.std = std

    def generate_keys(self):
        """
            public, secret key 공식
            S(x), A(x) = 무작위 다항식
            e = 무작위 노이즈 다항식

            secret_key = S(x)
            public_key = ( -A(x) * S(x) + e, A(x) )
        """
        s = Rq(discrete_gaussian(self.n, std=self.std), self.p)
        e = Rq(discrete_gaussian(self.n, std=self.std), self.p)

        a1 = Rq(discrete_uniform(self.n, self.p), self.p)
        a0 = -1 * (a1 * s + self.t * e)

        return (s, (a0, a1))  # (secret, public)

    def encrypt(self, m, public_key):
        """
            암호화 알고리즘
            (a0, a1) = public_key
            m = 메세지 => ring-polynomial 로 변환
            e0, e1 = 무작위 노이즈 다항식
            u = 무작위 다항식

            암호화 시 2가지 값 output
            c0 = m + a0 * u + e0
            c1 = a1 * u + e1
        """
        a0, a1 = public_key
        # 작은 오차값 t
        e0 = self.t * Rq(discrete_gaussian(self.n, std=self.std), self.p)
        # 작은 오차값 t
        e1 = self.t * Rq(discrete_gaussian(self.n, std=self.std), self.p)
        u = Rq(discrete_gaussian(self.n, std=self.std), self.p)

        m = Rq(m.poly.coeffs, self.p)

        return (
            m + a0 * u + e0, 
            a1 * u + e1
        )
    
    def encrypt_set(self, plain_set, public_key):
        return [ self.encrypt(message, public_key) for message in plain_set ]

    def decrypt_set(self, cipher_set, secret_key):
        return [ self.decrypt(c, secret_key) for c in cipher_set ]

    def decrypt(self, c, s):
        '''
            복호화 알고리즘
            
            m = c0 + c1 * s
        '''
        m = c[0] + c[1] * s
        m = Rq(m.poly.coeffs, self.t)

        return m

    def add(self, c0, c1):
        c = ()

        k0 = len(c0)
        k1 = len(c1)

        for _ in range(abs(k0 - k1)):
            c0 += (Rq([0], self.p),) 

        for i in range(len(c0)):
            c += (c0[i] + c1[i],)

        return c
    
    
    def sub(self, c0, c1):
        c = ()

        k0 = len(c0)
        k1 = len(c1)

        for _ in range(abs(k0 - k1)):
            c0 += (Rq([0], self.p),) 

        for i in range(len(c0)):
            c += (c0[i] - c1[i],)

        return c

    def mul(self, c0, c1):
        c = ()

        k0 = len(c0) - 1
        k1 = len(c1) - 1

        for _ in range(k1):
            c0 += (Rq([0], self.p),)

        for _ in range(k0):
            c1 += (Rq([0], self.p),)

        for i in range(k0 + k1 + 1):
            _c = Rq([0], self.p)
            for j in range(i+1):
                _c += c0[j] * c1[i-j]
            c += (_c,)

        return c
