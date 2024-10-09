from utils import convert_message_to_coeffs, convert_coeffs_to_message, check_is_exists
from RLWE import RLWE
from Rq import Rq
import numpy as np

if __name__ == '__main__':
    n = 8  # 차수
    q = 67108289 
    t = 256
    std = 3  # 가우시안 분포

    rlwe = RLWE(n, q, t, std)
    (sec, pub) = rlwe.generate_keys()

    """ 클라이언트 구축 부 """
    print(">>> client encrypt")
    client_data = 100
    client_poly = Rq(convert_message_to_coeffs(client_data, t, n), t)
    print(">>> poly")
    print(client_poly)
    print()
    cipher_client = rlwe.encrypt(client_poly, pub)
    
    """ 서버 구축 부 """
    print(">>> server encrypt")
    server_set = [ 3333, 3124, 1253, 5523, 4213, 53418, 4489, 3711, 231, 1900 ]
    server_poly_set = [ Rq(convert_message_to_coeffs(m, t, n), t) for m in server_set]
    for i, rq in enumerate(server_poly_set):
        print(">>> ", server_set[i])
        print(rq)
        print()
    cipher_server_set = rlwe.encrypt_set(server_poly_set, pub)

    print(">>> server homomorphic intersection")
    add_set = []
    for server_message in cipher_server_set:
        c_sub = rlwe.sub(server_message, cipher_client)
        add_set.append(c_sub)


    """ 클라이언트 구축 부 """
    print(">>> client decrypt")
    decrypt_m = rlwe.decrypt_set(add_set, sec)
    for m in decrypt_m:
        print(m)
        print()
    decrypted_messages = [ convert_coeffs_to_message(id.poly.c, t) for id in decrypt_m ]
    print(">>> orig", np.array(server_set))
    print(">>> resl", np.array(server_set) - client_data)
    print(">>> decR", decrypted_messages)
