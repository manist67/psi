from utils import convert_message_to_coeffs, convert_coeffs_to_message, check_is_exists
from RLWE import RLWE
from Rq import Rq

if __name__ == '__main__':
    n = 8  # 차수
    q = 67108289 
    t = 37  
    std = 3  # 가우시안 분포

    rlwe = RLWE(n, q, t, std)
    (sec, pub) = rlwe.generate_keys()

    """ 클라이언트 구축 부 """
    print(">>> client encrypt")
    client_set = [ 30, 50, 70, 9867 ]
    client_poly_set = [ Rq(convert_message_to_coeffs(m, t, n), q) for m in client_set ]
    cipher_client_set = rlwe.encrypt_set(client_poly_set, pub)
    
    """ 서버 구축 부 """
    print(">>> server encrypt")
    server_set = [ 9867, 3124, 1253, 5523, 4213, 53418, 4489, 9711, 30 ]
    server_poly_set = [ Rq(convert_message_to_coeffs(m, t, n), q) for m in server_set]
    cipher_server_set = rlwe.encrypt_set(server_poly_set, pub)

    print(">>> server homomorphic intersection")
    intersections = []
    for client_message in cipher_client_set:
        for server_message in cipher_server_set:
            c_sub = rlwe.sub(client_message, server_message)
            intersections.append(c_sub)


    """ 클라이언트 구축 부 """
    print(">>> client decrypt")
    intersection_dec = rlwe.decrypt_set(intersections, sec)
    decrypted_messages = [ convert_coeffs_to_message(id.poly.c, t) for id in intersection_dec ]
    
    exists = check_is_exists(decrypted_messages, client_set)
    print(exists)
