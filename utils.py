import numpy as np

def mod_q(poly, q):
    return np.poly1d([coeff % q for coeff in poly])

def mod_poly(poly, n):
    """
    다항식의 차수를 n으로 제한하는 폴리모듈러 연산.
    poly: np.poly1d 다항식
    n: 차수 제한 (예: 1024)
    """
    coeffs = poly.coeffs
    mod_coeffs = np.zeros(n)  # 차수 n에 맞춰 0으로 초기화된 계수 배열 생성

    # 각 항에 대해 차수를 n으로 나눈 나머지를 계산
    for i, coeff in enumerate(coeffs):
        degree = len(coeffs) - i - 1  # 계수의 차수 계산
        mod_degree = degree % n  # 차수를 n으로 나눈 나머지 (mod x^n)
        
        # 차수가 n보다 작은 항들에 대해 계수를 더함
        if mod_degree < n:
            mod_coeffs[mod_degree] += coeff

    # 결과를 np.poly1d로 변환하여 반환
    result_poly = np.poly1d(mod_coeffs)
    
    return result_poly


if __name__ == "__main__":
    # 테스트 다항식 (차수가 1024 이상인 경우)
    test_poly = np.poly1d([1, 0, 0, 0, 1])  # x^4 + 1

    # 차수 제한
    n = 4
    result = mod_poly(test_poly, n)

    print(result.c)  # 결과 다항식 출력


def get_divider(n):
    poly_mod = np.zeros(n-1)
    poly_mod[0] = 1
    poly_mod[-1] = 1
    poly_mod = np.poly1d(poly_mod)

    return poly_mod


import random

"""
암호화를 위한 무작이 이진 다항식 생성
"""
random_binary_poly = None
def generate_random_binary_polynomial(degree):
    """이진 계수로 구성된 무작위 다항식 생성 (계수는 0 또는 1)"""
    global random_binary_poly
    if random_binary_poly == None:
        random_binary_poly = np.poly1d([random.choice([0, 1]) for _ in range(degree)])
    return random_binary_poly

def generate_random_polynomaial(degree, q):
    return np.poly1d([ random.randint(0, q) for _ in range(0, degree) ])