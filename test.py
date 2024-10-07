import numpy as np

# 다항식 정의 (p_0, p_1, u, e_0, e_1, m_polynomial)
p_0 = np.poly1d([2, 1])  # 공개키 다항식 p_0 (2x + 1)
p_1 = np.poly1d([1, 2])  # 공개키 다항식 p_1 (x + 2)
u = np.poly1d([1, 1])    # 무작위 다항식 u (x + 1)
e_0 = np.poly1d([1])     # 작은 잡음 e_0
e_1 = np.poly1d([2])     # 작은 잡음 e_1
m_polynomial = np.poly1d([3, 0, 1])  # 평문 다항식 m_polynomial (3x^2 + 1)

# 모듈러 값 설정
q = 5

# c_0 계산: (p_0 * u + e_0 + m_polynomial) % q
c_0 = (np.polyadd(np.polymul(p_0, u), np.polyadd(e_0, m_polynomial))) % q

# c_1 계산: (p_1 * u + e_1) % q
c_1 = (np.polyadd(np.polymul(p_1, u), e_1)) % q

# 결과 출력
print("c_0 (암호화된 다항식):", c_0)
print("c_1 (암호화된 다항식):", c_1)
