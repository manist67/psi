"""
Fully Homomorphic Encryption / Fan-Vercauteren
PSI 동형 암호 로직 구현

Author : Minsung Kim
Since : 2024-10-05

"""
import random
import numpy as np
from utils import mod_q, generate_random_binary_polynomial, get_divider

"""
잡음 함수
"""
def generate_small_noise_polynomial(degree=4, noise_bound=1):
    noise_poly = [random.randint(-noise_bound, noise_bound) for _ in range(0, degree)]
    return np.poly1d(noise_poly)

"""
암호화
암호화 시 두 가지 다항식이 생성 됨
p0, p1 퍼블릭 키
c0: (p0 + 무작위 다항식 + 오류 + 데이터 다항식)  % q
c1: (p1 + 무작위 다항식 + 오류) % q
"""
def encrypt(plain_set, public_key, params):
    (a, p) = public_key

    u = generate_random_binary_polynomial(params["n"])

    cipher_set = []
    e0 = generate_small_noise_polynomial(params["n"])
    e1 = generate_small_noise_polynomial(params["n"])

    for plain in plain_set:
        m_polynomial = convert_message_to_polynomial(plain, params["t"])
        
        c0 = np.polymul(p, u)
        c0 = np.polyadd(c0, e1)
        c0 = np.polydiv(c0, get_divider(params['n']))[1]
        c0 = mod_q(c0, params['q'])
        
        c1 = np.polymul(a, u)
        c1 = np.polyadd(c1, e0)
        c1 = np.polyadd(c1, m_polynomial)
        c1 = np.polydiv(c1, get_divider(params['n']))[1]
        c1 = mod_q(c1, params['q'])
        
        print(">>> encrply ", plain, c0.c, c1.c)

        cipher_set.append((c0, c1))

    return cipher_set

"""
데이터를 다항식 형태로 변경
"""
def convert_message_to_polynomial(m, t, degree_limit=4):
    poly = []

    while m != 0 and len(poly) < degree_limit:
        poly.append(m % t)
        m //= t

    while len(poly) < degree_limit:
        poly.append(0)

    return np.poly1d(poly[::-1])

"""
복호화 함수
복호화는 다음과 같은 수식으로 만들어짐
p = (c0 + secret_key * c1) % q
"""
def decrypt(cipher_set, secret_key, params):
    plain_set = []
    for cipher_value in cipher_set:
        print(">>> plain_poly", cipher_value[0].c, cipher_value[1].c)

    for cipher_value in cipher_set:
        (c0, c1) = cipher_value
        # 복호화 + 평문 공간 변화
        # 복호확 수식 p = (c0 + secret_key * c1) % q
        # 평문 공간 변환 message = p % t
        decrypt_poly = np.polymul(c1, secret_key)
        decrypt_poly = np.polydiv(decrypt_poly, get_divider(params["n"]))[1]
        decrypt_poly = np.polyadd(c0, decrypt_poly)
        decrypt_poly = mod_q(decrypt_poly, params["q"])  # 모듈러 연산
        print(">>> decrtpy_poly", decrypt_poly.c)
        plain_set.append( convert_polynomial_to_message(decrypt_poly, params["t"]) )
    
    return plain_set

"""
다항식을 데이터로 변환하는 함수
"""
def convert_polynomial_to_message(p, t):
    # message = 0
    # degree = len(p) - 1
    # for coeff in p.c:
    #     message += (coeff * ( t ** degree ))
    #     degree -= 1

    # return message
    m = 0
    current_t_power = 1  # t^0부터 시작 (1로 초기화)
    
    for coeff in reversed(p.c):
        # if m > 100000: return -1
        m += coeff * current_t_power
        current_t_power *= t  # t의 거듭제곱을 다음으로 업데이트
    
    return m

"""
    다항식 빼기
"""
def homomorphic_sub(encrypt_poly1d1, encrypt_poly1d2):
    return (encrypt_poly1d1[0] - encrypt_poly1d2[0], encrypt_poly1d1[1] - encrypt_poly1d2[1])

"""
    client와 server의 비교
"""
def find_intersection(cipher_client_set, server_set, public_key, params):
    result_set = []
    cipher_server_set = encrypt(server_set, public_key, params)

    for cipher_client_value in cipher_client_set:
        for cipher_server_value in cipher_server_set:
            # 서버, 클라이언트를 둘다 암호화 하여 다항식 빼기를 함
            encrypt_diff = homomorphic_sub(cipher_client_value, cipher_server_value)
            print(">>> encr diff", encrypt_diff[0].c, encrypt_diff[1].c)
            # 해당 결과 저장
            result_set.append(encrypt_diff)

    return result_set


"""
복호화된 결과는 client n개 server m개 가 합쳐져서
n*m개로 출력됨
이때 결과를 m개로 나눠서 그 공간안에 0이 있는지 확인
"""
def check_exists(my_set, plain_message_set):
    exists = [] 
    my_set_len = len(my_set)
    server_set_len = len(plain_message_set) // my_set_len

    idx = 0
    for i in range(0, len(plain_message_set), server_set_len):
        data_range = plain_message_set[i:i + server_set_len]
        if check_if_zero(data_range): exists.append(my_set[idx])
        idx += 1

    return exists


"""
결과안에 0이 있는지 확인
"""
def check_if_zero(data_set):
    for val in data_set:
        if val == 0: return True
    return False

from KeyGenerator import KeyGenerator
if __name__ == "__main__":
    params = {
        'q': 32767,  # 큰 소수
        't': 10,    # 평문 공간 크기
        'n': 6,    # 다항식 차수
        "noise": 128
    }

    key_generator = KeyGenerator(params)
    (public_key, secret_key) = key_generator.generate_keys()
    """ client 구현 부 """
    client_set = [ 3 ]
    client_cipher_set = encrypt(client_set, public_key, params)
    
    """ server 구현 부 """
    server_set = [ 3, 5, 21, 24, 78 ]
    results = find_intersection(client_cipher_set, server_set, public_key, params)

    """ client 구현 부 """
    plain_set = decrypt(results, secret_key, params)
    print(">>>plain", plain_set)
    # print(check_exists(client_set, plain_set))
