import numpy as np
import random

# 초기 파라미터 설정
def initialize_parameters():
    q = 32767      # 큰 소수 (모듈러 값)
    t = 10         # 평문 공간 크기
    n = 10          # 다항식 차수
    noise_bound = 1 # 노이즈 크기 제한
    return q, t, n, noise_bound

# 모듈러 연산 함수 (각 계수를 q로 나눈 나머지를 구함)
def mod_q_polynomial(poly, q):
    coeffs = [int(coeff % q) for coeff in poly.coeffs]
    return np.poly1d(coeffs)

# 메시지를 다항식으로 변환하는 함수
def convert_message_to_polynomial(m, t, n):
    poly_coeffs = []
    while m > 0:
        poly_coeffs.append(m % t)
        m //= t
    while len(poly_coeffs) < n:
        poly_coeffs.append(0)
    return np.poly1d(poly_coeffs[::-1])

# 메시지를 평문으로 변환하는 함수
def convert_polynomial_to_message(poly, t):
    m = 0
    t_power = 1
    for coeff in reversed(poly.coeffs):
        m += int(coeff) * t_power
        t_power *= t
    return m

# 암호화 함수 (노이즈 관리 및 모듈러 연산 추가)
def encrypt(plain_message, public_key, params):
    (p0, p1) = public_key
    q, t, n, noise_bound = params

    u = generate_random_binary_polynomial(n)
    e0 = generate_small_noise_polynomial(n, noise_bound)
    e1 = generate_small_noise_polynomial(n, noise_bound)

    m_polynomial = convert_message_to_polynomial(plain_message, t, n)

    c0 = np.polymul(p0, u)
    c0 = np.polyadd(c0, e0)
    c0 = np.polyadd(c0, m_polynomial)
    c0 = mod_q_polynomial(c0, q)  # 모듈러 연산 적용

    c1 = np.polymul(p1, u)
    c1 = np.polyadd(c1, e1)
    c1 = mod_q_polynomial(c1, q)  # 모듈러 연산 적용

    return (c0, c1)

# 비밀키와 암호문을 사용하여 복호화하는 함수 (노이즈 제어 추가)
def decrypt(ciphertext, secret_key, params):
    (c0, c1) = ciphertext
    q, t, n, _ = params

    # 복호화 연산: p(x) = (c0(x) + s(x) * c1(x)) mod q
    decrypt_poly = np.polymul(c1, secret_key)  # s(x) * c1(x)
    decrypt_poly = mod_q_polynomial(decrypt_poly, q)  # 모듈러 연산 적용
    decrypt_poly = np.polyadd(c0, decrypt_poly)  # c0(x) + s(x) * c1(x)
    decrypt_poly = mod_q_polynomial(decrypt_poly, q)  # 모듈러 연산 적용

    # 다항식을 메시지로 변환 (t-진법)
    message = convert_polynomial_to_message(decrypt_poly, t)
    
    # 노이즈 제거를 위해 평문 값에 t로 다시 모듈러 연산을 적용
    # 이 과정에서 평문 공간에 노이즈가 남아있다면 이를 처리할 수 있음
    return message % t

# 무작위 이진 다항식 생성 함수
def generate_random_binary_polynomial(n):
    return np.poly1d([random.choice([0, 1]) for _ in range(n)])

# 작은 잡음 다항식 생성 함수
def generate_small_noise_polynomial(n, noise_bound=1):
    return np.poly1d([random.randint(-noise_bound, noise_bound) for _ in range(n)])

# 공개키 출력 함수
def print_polynomial(poly, name):
    print(f"{name}(x) = ", end="")
    print(" + ".join([f"{int(coeff)}x^{i}" for i, coeff in enumerate(reversed(poly.coeffs))]))

# 메인 실행
if __name__ == "__main__":
    # 초기 파라미터 설정
    q, t, n, noise_bound = initialize_parameters()
    params = (q, t, n, noise_bound)

    # 공개키와 비밀키 생성 (간단한 임의 다항식으로 대체)
    secret_key = np.poly1d([random.choice([-1, 0, 1]) for _ in range(n)])
    public_key = (
        np.poly1d([random.randint(0, q-1) for _ in range(n)]),  # p0(x)
        np.poly1d([random.randint(0, q-1) for _ in range(n)])   # p1(x)
    )

    # 암호화할 평문 메시지
    plain_message = 2318  # 예시 평문 메시지

    # 암호화
    ciphertext = encrypt(plain_message, public_key, params)
    print("Ciphertext:")
    print_polynomial(ciphertext[0], "c0")
    print_polynomial(ciphertext[1], "c1")

    # 복호화
    decrypted_message = decrypt(ciphertext, secret_key, params)
    print("\nDecrypted message:", decrypted_message)
