"""
demo application for PSI
"""
from flask import Flask, render_template, jsonify, request, abort


from RLWE import RLWE
from utils import convert_message_to_coeffs, convert_coeffs_to_message, check_is_exists
from Rq import Rq

n = 8  # 차수
q = 67108289 
t = 37  
std = 3  # 가우시안 분포
rlwe = RLWE(n, q, t, std)
key = None
cipher_client_set = []
cipher_server_set = []
intersections = []


app = Flask(__name__)


@app.route("/keys")
def keys():
    global key
    key = rlwe.generate_keys()
    res = {
        "secret_key": key[0].serialize(),
        "public_key": [ key[1][0].serialize(), key[1][1].serialize() ]
    }
    return jsonify(res)

@app.route("/encrypt_client", methods=[ "POST" ])
def enc_client():
    global key, cipher_client_set
    if key is None:
        abort(400)
    params = request.get_json()

    (sec, pub) = key

    print(params["data"])
    client_poly_set = [ Rq(convert_message_to_coeffs(m, t, n), q) for m in params["data"] ]
    cipher_client_set = rlwe.encrypt_set(client_poly_set, pub)

    poly_serialized = [ 
        [cipher[0].serialize(), cipher[1].serialize()] for cipher in cipher_client_set  
    ]
    
    return jsonify(poly_serialized)

@app.route("/encrypt_server", methods=[ "POST" ])
def enc_server():
    global key, cipher_server_set
    if key is None:
        abort(400)
    params = request.get_json()

    (sec, pub) = key

    print(params["data"])
    server_poly_set = [ Rq(convert_message_to_coeffs(m, t, n), q) for m in params["data"] ]
    cipher_server_set = rlwe.encrypt_set(server_poly_set, pub)

    poly_serialized = [ 
        [cipher[0].serialize(), cipher[1].serialize()] for cipher in cipher_server_set  
    ]
    
    return jsonify(poly_serialized)

@app.route("/intersection", methods=[ "GET" ])
def intersection():
    global cipher_client_set, cipher_server_set, intersections
    if len(cipher_client_set) == 0 or len(cipher_server_set) == 0:
        abort(400)
    
    intersections = []
    for client_message in cipher_client_set:
        for server_message in cipher_server_set:
            c_sub = rlwe.sub(client_message, server_message)
            intersections.append(c_sub)

    poly_serialized = [ 
        [cipher[0].serialize(), cipher[1].serialize()] for cipher in intersections  
    ]
    
    return jsonify(poly_serialized)

@app.route("/decrypt_client", methods=[ "POST" ])
def decrypt():
    global key, intersections
    if key is None or len(intersections) == 0:
        abort(400)

    (sec, pub) = key
    intersection_dec = rlwe.decrypt_set(intersections, sec)
    decrypted_messages = [ int(convert_coeffs_to_message(id.poly.c, t)) for id in intersection_dec ]
    
    params = request.get_json()
    exists = check_is_exists(decrypted_messages, params["data"])

    res = {
        "exists": exists,
        "decrypted": decrypted_messages
    }
    return jsonify(res) 


@app.route("/")
def index():
    global key, cipher_client_set, cipher_server_set, intersections
    key = None
    cipher_client_set = []
    cipher_server_set = []
    intersections = []

    return render_template('index.html')