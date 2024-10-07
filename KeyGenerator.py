import random
import numpy as np

class KeyGenerator:
    def __init__(self, params):
        self.q = params['q']  # 큰 소수 (모듈러스 값)
        self.t = params['t']  # 평문 공간의 크기
        self.n = params['n']  # 다항식 차수

    def generate_secret_key(self):
        # 비밀키는 이진 다항식 (계수는 0 또는 1)
        secret_key = self.generate_random_binary_polynomial(self.n)
        return secret_key

    def generate_public_key(self, secret_key):
        # 공개키는 (p0, p1)로 구성됨
        # 무작위 이진 다항식 u, 작은 잡음 다항식 e 생성
        u = self.generate_random_binary_polynomial(self.n)
        e = self.generate_small_noise_polynomial(self.n)

        # 공개키 계산: p0 = - (s * u + e) mod q, p1 = u
        p0 = np.poly1d([ -c % self.q for c in (secret_key * u + e).c]) 
        p1 = u

        return (p0, p1)

    def generate_keys(self):
        secret_key = self.generate_secret_key()
        public_key = self.generate_public_key(secret_key)

        return public_key, secret_key

    def generate_random_binary_polynomial(self, degree):
        # 이진 다항식 생성 (계수는 0 또는 1)
        return np.poly1d([random.choice([0, 1]) for _ in range(degree)])

    def generate_small_noise_polynomial(self, degree):
        # 작은 잡음 다항식 생성 (계수는 -1, 0, 1과 같은 작은 정수)
        return np.poly1d([random.randint(-1, 1) for _ in range(degree)])
