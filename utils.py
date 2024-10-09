"""
    Author: minsung kim
    
    필수 유틸들 작성
"""
def convert_message_to_coeffs(message, t, n):
    poly = []
    while message != 0:
        poly.append(message % t)
        message //= t
    
    while n > len(poly):
        poly.append(0)
    
    poly.reverse()

    return poly


def convert_coeffs_to_message(c, t):
    m = 0
    for i, cof in enumerate(c):
        m += (cof * (t ** i))

    return m


def crange(coeffs, q):
    coeffs = np.where((coeffs >= 0) & (coeffs <= q//2),
                      coeffs,
                      coeffs - q)

    return coeffs

def split(li, n):
    k, m = divmod(len(li), n)
    return (li[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def check_is_exists(decrypt_set , client_set):
    parts = split(decrypt_set, len(client_set))
    exists = []
    for i, items in enumerate(parts):
        if 0 in items:
            exists.append(client_set[i])

    return exists
    
import numpy as np

def discrete_gaussian(n, std=1):
    coeffs = np.round(std * np.random.randn(n))
    return coeffs


def discrete_uniform(n, max=None, min=0 ):
    coeffs = np.random.randint(min, max, size=n)
    return coeffs

if __name__ == "__main__":
    print("이산 가우스 분포 함수")
    print(discrete_gaussian(10, 1))
