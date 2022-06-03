import socket           
import json
import f2_1705091
import f1_1705091
import numpy as np

def convert_to_matrix(All_matrix):
    c1 = All_matrix.split(",")
    c1 = c1[:-1]
    c1 = np.array(c1)
    print(len(c1))
    state_matrix = np.reshape(c1, (4, 4), order='C')
    print("state: ", state_matrix)
    return state_matrix

s = socket.socket()        
port = 9999
s.connect(('127.0.0.1', port))



while True:
    data = s.recv(1024).decode()
    data = json.loads(data)
    
    encrypted_key = data.get("Encrypted_key")
    
    All_Cipher_Text_matrix = []
    All_matrix = data.get("All_Cipher_Text_matrix")
    All_matrix = All_matrix.split("\n")
    
    All_matrix = All_matrix[:-1]
    
    state_matrix = [[""]*4 for i in range(4)]
    for i in range(len(All_matrix)):
        state_matrix = convert_to_matrix(All_matrix[i])
        All_Cipher_Text_matrix.append(state_matrix)
    
    public_key = data.get("Public_key")
    
    e = int(public_key.split(" ")[0])
    n = int(public_key.split(" ")[1])
    
    key_file = open("Don't Open This/key.txt", "r")
    d = key_file.read()
    
    #RSA Decryption
    decrypted_key = f2_1705091.Decryption(encrypted_key, int(d), n)
    print("decrypted key: ", decrypted_key)
    
    key = decrypted_key[:16]
    while len(key) < 16:
        key = key + '#'
    print(key)
    

    # Convert the plain text and key to hex
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
    
    print(All_Round_Key)
    
    plain_text = f1_1705091.Decryption(All_Cipher_Text_matrix, All_Round_Key)
    print(plain_text)
    
    f = open("Don't Open This/text.txt", "w")
    f.write(plain_text)
    f.close()
    
    