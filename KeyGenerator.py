import random
import numpy as np
from utils import get_divider, mod_q, generate_random_binary_polynomial, generate_random_polynomaial

class KeyGenerator:
    def __init__(self, params):
        self.q = params['q']  # 큰 소수 (모듈러스 값)
        self.t = params['t']  # 평문 공간의 크기
        self.n = params['n']  # 다항식 차수

    def generate_secret_key(self):
        # 비밀키는 이진 다항식 (계수는 0 또는 1)
        secret_key = generate_random_binary_polynomial(self.n)
        return secret_key

    def generate_public_key(self, secret_key):
        # 공개키는 (p0, p1)로 구성됨
        # 무작위 이진 다항식 u, 작은 잡음 다항식 e 생성
        a = generate_random_polynomaial(self.n, self.q)

        # 공개키 계산: p = (-a * s + e) mod q
        e = self.generate_small_noise_polynomial(self.n)

        p = np.polymul(a, -1)
        p = np.polymul(p, secret_key)
        p = np.polyadd(p, e)
        p = np.polydiv(p,  get_divider(self.n))[1] #np.poly1d([ (-int(c % self.q)) for c in (secret_key * u + e).c])
        p = mod_q(p, self.q)

        return (a, p)

    def generate_keys(self):
        secret_key = self.generate_secret_key()
        public_key = self.generate_public_key(secret_key)
        
        return (public_key, secret_key)

    def generate_small_noise_polynomial(self, degree):
        # 작은 잡음 다항식 생성 (계수는 -1, 0, 1과 같은 작은 정수)
        return np.poly1d([random.randint(-1, 1) for _ in range(degree)])
