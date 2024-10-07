"""
PSI 동형 암호 로직 구현

Author : Minsung Kim
Since : 2024-10-05

"""
import random
import numpy as np


"""
암호화를 위한 무작이 이진 다항식 생성
"""
def generate_random_binary_polynomial(degree):
    """이진 계수로 구성된 무작위 다항식 생성 (계수는 0 또는 1)"""
    random.seed("TEST_SEED") # 서버쪽 encrpt, client 측 encrtpt를 정확하게 하기 위해서 공통 시드 사용
    return np.poly1d([random.choice([0, 1]) for _ in range(degree)])


"""
암호화
암호화 시 두 가지 다항식이 생성 됨
p0, p1 퍼블릭 키
c0: (p0 + 무작위 다항식 + 오류 + 데이터 다항식)  % q
c1: (p1 + 무작위 다항식 + 오류) % q
"""
def encrypt(plain_set, public_key, q, t, n):
    (p0, p1) = public_key

    u = generate_random_binary_polynomial(n)

    cipher_set = []

    for plain in plain_set:
        m_polynomial = convert_message_to_polynomial(plain, t)
        # 간단한 구현을 위해서 e 값을 뺏음
        c0 = np.poly1d([ i % q for i in (p0 * u + m_polynomial).c ])
        c1 = np.poly1d([ i % q for i in (p1 * u).c ])

        cipher_set.append((c0, c1))

    return cipher_set

"""
데이터를 다항식 형태로 변경
"""
def convert_message_to_polynomial(m, t):
    poly = []

    while m != 0:
        poly.append(m % t)
        m //= t

    poly.reverse()

    return np.poly1d(poly)

"""
복호화 함수
복호화는 다음과 같은 수식으로 만들어짐
p = (c0 + secret_key * c1) % q
"""
def decrypt(cipher_set, secret_key, q, t):
    plain_set = []
    for cipher_value in cipher_set:
        (c0, c1) = cipher_value
        # 복호화 + 평문 공간 변화
        # 복호확 수식 p = (c0 + secret_key * c1) % q
        # 평문 공간 변환 message = p % t
        decrypt_poly = np.poly1d( [ coeff % q for coeff in (c0 + secret_key * c1).c] )
        plain_message = np.poly1d([coeff % t for coeff in decrypt_poly.c])
        plain_set.append( convert_polynomial_to_message(plain_message, t) )
    
    return plain_set

"""
다항식을 데이터로 변환하는 함수
"""
def convert_polynomial_to_message(p, t):
    message = 0
    degree = len(p) - 1
    for coeff in p.c:
        message += coeff * ( t ** degree )
        degree -= 1

    return message

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
    cipher_server_set = encrypt(server_set, public_key, params["q"], params["t"], params["n"])

    for cipher_client_value in cipher_client_set:
        for cipher_server_value in cipher_server_set:
            # 서버, 클라이언트를 둘다 암호화 하여 다항식 빼기를 함
            encrypt_diff = homomorphic_sub(cipher_client_value, cipher_server_value)

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
        'q': 65537,  # 큰 소수
        't': 256,    # 평문 공간 크기
        'n': 1024    # 다항식 차수
    }

    key_generator = KeyGenerator(params)
    public_key, secret_key = key_generator.generate_keys()


    """ client 구현 부 """
    client_set = [ 37128, 231, 3245, 49423 ]
    client_cipher_set = encrypt(client_set, public_key, params["q"], params["t"], params["n"])

    """ server 구현 부 """
    server_set = [ 37128, 273845, 382391, 283467, 231, 374959, 1234235 ]
    results = find_intersection(client_cipher_set, server_set, public_key, params)

    """ client 구현 부 """
    plain_set = decrypt(results, secret_key, params["q"], params["t"])
    print(check_exists(client_set, plain_set))
