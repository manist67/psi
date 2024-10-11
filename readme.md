# Implements PSI using FHE

## Installation
```
pip install -r requirements.txt
```

## Required dependency
1. numpy
2. Flask ( used for the demonstration )


## How to Run
1. test PSI
```
python main.py
```

2. test homomorphic operation 
```
python operate_test.py
```

3. run demonstration
```
flask run --debug
```


## Demonstration
http://manist67.iptime.org:5000/


# What is PSI
## Homomorphic Encryption
Homomorphic Encryption is an encryption algorithm that uses a public key.

Homomorphic Encryption allows operations on encrypted values without decrypting them.


### Generate keys
Homomorphic Encryption uses a public key and a secret key. The secret key is a randomly generated polynomial, and the public key consists of two parts (a, P).

The key generation process is as follows
```
SK = randomly generated polynomial 
a = randomly generated polynomial

e = random noise polynomial

P = -SK * a + e
(Sk, (a, P))
```

Using Public key to encrypt plain messages, Secret key to decrypt cipher messages.

### Encrypt Message
When encrypting a message, only the public key is needed.

```
(a, P) = public_key
e1, e2 = random noise polynomial
u = randomly generated polynomial

m = message polynomial

c1 = u * a + e1
c2 = u * P + m + e2

(c1, c2)
``` 

### Decrypt Message
You can decrypt the message using the secret.
```
(c1, c2) = cipher_message

m = c1 + c2 * secret_key
```

### Operation
You can compute two Cipher Messages like add, subtract, multiply
You perform operations on the matching cipher pairs as shown below.
```
(c1, c2) = cipher_message_1
(c`1, c`2) = cipher_message_2

(c1 + c`1, c2 + c`2)
```
The result of the operation can be decrypted like a plain message.


## PSI ( Private Set Intersection )
Now, we talk about PSI (Private Set Intersection).

PSI is compared two sets without knowing what values are in the set.

Client just send cipher message to server for compute, then Client get computed results.

Server can't know what elements in the client set.

### How PSI works
Alice and Bob each have a set of elements. 
 
The goal is for both to find the common elements in their sets, but without revealing the rest of their data.

1. Set Representation

    Alice and Bob encrypt their sets using homomorphic encryption.

2. Computation

    - Alice sends her encrypted set to Bob.
    - Bob computes the intersection of his own set with Alice's encrypted set without decrypting the values.
    - The computation only reveals the elements that exist in both sets.

3. Privacy Preservation
    
    - Alice receives the set of computed elements from Bob.
    - She decrypts the set to know which elements are part of the intersection.