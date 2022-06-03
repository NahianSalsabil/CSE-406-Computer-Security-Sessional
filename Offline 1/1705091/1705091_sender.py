import socket     
import f1_1705091
import f2_1705091       
import os
import numpy as np
import json

s = socket.socket()        
port = 9999
s.bind(('', port))
 

s.listen(10)    

if not os.path.exists("Don't Open This"):
    os.mkdir("Don't Open This")

while True:
    connection, addr = s.accept()    
    
    plain_text = input("Enter your text: ")
    print(plain_text)
    no_of_strip_char = 16 - (len(plain_text) % 16)
    AES_key = input("Enter key: ")
    key = AES_key[:16]
    while len(key) < 16:
        key = key + '#'
    print(key)
    
    K = input("Enter k: ")

    # Convert the plain text and key to hex
    hex_plaintext = f1_1705091.convert_to_hex(plain_text)
    print("hex plain text: ", hex_plaintext)
    hex_key = f1_1705091.convert_to_hex(key)


    #convert to a 4*4 matrix
    key_matrix = f1_1705091.convert_to_matrix(hex_key)

    print("key matrix: \n", key_matrix)

    # Construct word from the matrix
    word0 = np.array(key_matrix[:,0])
    word1 = np.array(key_matrix[:,1])
    word2 = np.array(key_matrix[:,2])
    word3 = np.array(key_matrix[:,3])


    ## All Round Key Generation
    All_Round_Key = f1_1705091.All_Round_Key_Gen(key_matrix, word0, word1, word2, word3)  

    ##AES Encryption
    All_Cipher_Text_matrix = []
    All_Cipher_Text_matrix = f1_1705091.encryption(hex_plaintext, All_Round_Key)
    
    #key generation
    e,d,n = f2_1705091.Key_generation(int(K))
    
    #RSA key encryption
    Encrypted_key = f2_1705091.Encryption(AES_key, e, n)
    
    #write key in file
    f = open("Don't Open This/key.txt", "w")
    f.write(str(d))
    f.close()
    
    public_key = str(d) + " " + str(n)
    
    full_matrix = ""
    for i in range (len(All_Cipher_Text_matrix)):
        for k in range(0,4):
            for l in range(0,4):
                full_matrix += All_Cipher_Text_matrix[i][k][l] + ","
        full_matrix += "\n"
    
    ##Send data
    data = {
        "All_Cipher_Text_matrix": full_matrix,
        "Encrypted_key" : Encrypted_key,
        "Public_key": public_key
    }
    
    data = json.dumps(data)
    
    connection.sendall(data.encode())
    
    # while True:
    # if os.path.exists("Don't Open This/text.txt"):
    f1 = open("Don't Open This/text.txt", "r")
    decrypted_text = f1.read()
    print(decrypted_text)
    if plain_text == decrypted_text:
        print("Received Successfully!!")
            # break
    
    
    