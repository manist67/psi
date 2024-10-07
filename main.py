"""
PSI 동형 암호 로직 구현

Author : Minsung Kim
Since : 2024-10-05

"""
import random
import numpy as np



def generate_random_binary_polynomial(degree):
    """이진 계수로 구성된 무작위 다항식 생성 (계수는 0 또는 1)"""
    return np.poly1d([random.choice([0, 1]) for _ in range(degree)])



def encrypt(plain_set, public_key, q, t, n):
    (p0, p1) = public_key

    u = generate_random_binary_polynomial(n)

    cipher_set = []

    for plain in plain_set:
        m_polynomial = convert_message_to_polynomial(plain, t)
        c0 = np.poly1d([ i % q for i in (p0 * u + m_polynomial).c ])
        c1 = np.poly1d([ i % q for i in (p1 * u).c ])

        cipher_set.append((c0, c1))

    return cipher_set

def convert_message_to_polynomial(m, t):
    poly = []

    while m != 0:
        poly.append(m % t)
        m //= t

    poly.reverse()

    return np.poly1d(poly)


def decrypt(cipher_set, secret_key, q, t):
    plain_set = []
    for cipher_value in cipher_set:
        (c0, c1) = cipher_value
        m = np.poly1d( [ coeff % q for coeff in (c0 + secret_key * c1).c] )
        plain_set.append( m )
    
    return plain_set

def convert_polynomial_to_message(p, t):
    message = 0
    degree = len(p) - 1
    for coeff in p.c:
        message += coeff * ( t ** degree )
        degree -= 1

    return message

def homomorphic_sub(encrypt_poly1d1, encrypt_poly1d2):
    return (encrypt_poly1d1[0] - encrypt_poly1d2[0], encrypt_poly1d1[1] - encrypt_poly1d2[1])


def find_intersection(cipher_client_set, server_set, public_key, params):
    result_set = []
    cipher_server_set = encrypt(server_set, public_key, params["q"], params["t"], params["n"])

    for cipher_client_value in cipher_client_set:
        for cipher_server_value in cipher_server_set:
            encrypt_diff = homomorphic_sub(cipher_client_value, cipher_server_value)

            result_set.append(encrypt_diff)
    return result_set


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
    print(convert_message_to_polynomial(37128, 256).c)

    client_set = [ 37128 ]
    client_cipher_set = encrypt(client_set, public_key, params["q"], params["t"], params["n"])

    """ server 구현 부 """

    server_set = [ 37128, 273845, 382391, 283467, 374959 ]
    results = find_intersection(client_cipher_set, server_set, public_key, params)

    """ client 구현 부 """
    plain_set = decrypt(results, secret_key, params["q"], params["t"])
    print(plain_set)
