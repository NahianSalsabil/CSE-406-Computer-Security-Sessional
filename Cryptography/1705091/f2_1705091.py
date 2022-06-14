import math
from BitVector import *
import time


def Generate_e(PHI_n):
    e = 2
    while math.gcd(PHI_n, e) != 1:
        e += 1
    return e

def Key_generation(k):
    check = 0
    count = 0
    while count < 2:
        bv = BitVector(intVal = 0)
        bv = bv.gen_rand_bits_for_prime(int(k/2))
        check = bv.test_for_primality()
        if check >= 0.999 and count == 0:
            p = bv
            count = 1
        elif check >= 0.999 and count == 1 and bv != p:
            q = bv
            count = 2
    
    p = p.intValue()
    q = q.intValue()
    p = 11
    q = 13
    
    n = p * q
    PHI_n = (p-1) * (q-1)
    
    e = Generate_e(PHI_n)
    
    d = pow(e, -1, PHI_n)
    
    return e,d,n
   
                                            #### Encryption ####
def Encryption(plain_text, e, n):
    length = 0
    cipher_text = []

    while length < len(plain_text):
        P = ord(plain_text[length])
        C = pow(P, e, n)
        # print(C)
        cipher_text.append(C)
        length += 1
        
    print(cipher_text)
    return cipher_text

                                            #### Decryption ####
def Decryption(cipher_text, d, n):
    length = 0
    decrypted_text = ""
    while length < len(cipher_text):
        C = cipher_text[length]
        P = pow(C, d, n)
        # print(P)
        decrypted_text += chr(P)
        length += 1

    print(decrypted_text)
    return decrypted_text


def main():
    plain_text = input("Enter your text: ")
    print("plain text: ", plain_text)

    k = input("Enter K: ")
    print("k: ", k)

    start_key = time.time()
    e, d, n = Key_generation(int(k))
    stop_key = time.time()

    start_enc = time.time()
    cipher_text = Encryption(plain_text, e, n)
    stop_enc = time.time()
    
    start_dec = time.time()
    decrypted_text = Decryption(cipher_text, d, n)
    stop_dec = time.time()
    
    print("\nExecution time:")
    print("key Generation: ", stop_key-start_key)
    print("Encryption time: ", stop_enc-start_enc) 
    print("Decryption time: ", stop_dec-start_dec) 

    if decrypted_text == plain_text:
        print("Decryption Successful!!")

if __name__ == "__main__":
    main()
