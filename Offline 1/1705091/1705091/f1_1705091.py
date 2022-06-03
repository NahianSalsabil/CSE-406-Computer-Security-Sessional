from pydoc import plain
from BitVector import *
import numpy as np
import time

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

Round_Constant = [
    ["01", "00", "00", "00"],
    ["02", "00", "00", "00"],
    ["04", "00", "00", "00"],
    ["08", "00", "00", "00"],
    ["10", "00", "00", "00"],
    ["20", "00", "00", "00"],
    ["40", "00", "00", "00"],
    ["80", "00", "00", "00"],
    ["1B", "00", "00", "00"],
    ["36", "00", "00", "00"]
]
column = row = 4

AES_modulus = BitVector(bitstring='100011011')

total_round = 11


def convert_to_hex(value):    # Convert ASCII to HEX
    i = 0
    hex_array = []
    for c in value:
        hex_array.append(format(ord(c), "x") )
        i += 1
    return hex_array

def convert_to_matrix(oneD_array):   # Convert to a 4*4 matrix
    arr = np.array(oneD_array)
    array_2d = np.reshape(arr, (4, 4), order='F')
    return array_2d


##Byte Substitution
def byte_substitution(element, mode):    # Byte Substitution
    b = BitVector(hexstring=element)
    int_val = b.intValue()
    if mode == 1:
        s = Sbox[int_val]
    else:
        s = InvSbox[int_val]
    s = BitVector(intVal=s, size=8)
    return s.get_bitvector_in_hex()

## Shift Row Encryption
def Shift_Row_Encryption(state_matrix):
    for i in range(0,4):
        if i == 1:
            temp = state_matrix[1][0]
            state_matrix[i][0] = state_matrix[i][1]
            state_matrix[i][1] = state_matrix[i][2]
            state_matrix[i][2] = state_matrix[i][3]
            state_matrix[i][3] = temp
        if i == 2:
            temp = state_matrix[i][0]
            state_matrix[i][0] = state_matrix[i][2]
            state_matrix[i][2] = temp
            temp = state_matrix[i][1]
            state_matrix[i][1] = state_matrix[i][3]
            state_matrix[i][3] = temp
        if i == 3:
            temp = state_matrix[i][3]
            state_matrix[i][3] = state_matrix[i][2]
            state_matrix[i][2] = state_matrix[i][1]
            state_matrix[i][1] = state_matrix[i][0]
            state_matrix[i][0] = temp
    return state_matrix

## Shift Row Decryption
def Shift_Row_Decryption(state_matrix):
    for i in range(0,4):
        if i == 1:
            temp = state_matrix[1][3]
            state_matrix[i][3] = state_matrix[i][2]
            state_matrix[i][2] = state_matrix[i][1]
            state_matrix[i][1] = state_matrix[i][0]
            state_matrix[i][0] = temp
        if i == 2:
            temp = state_matrix[i][2]
            state_matrix[i][2] = state_matrix[i][0]
            state_matrix[i][0] = temp
            temp = state_matrix[i][3]
            state_matrix[i][3] = state_matrix[i][1]
            state_matrix[i][1] = temp
        if i == 3:
            temp = state_matrix[i][0]
            state_matrix[i][0] = state_matrix[i][1]
            state_matrix[i][1] = state_matrix[i][2]
            state_matrix[i][2] = state_matrix[i][3]
            state_matrix[i][3] = temp
    return state_matrix


## Mix Column
def Mix_Column(state_matrix, mode):
    result = [[""]*column for i in range(row)]
    for i in range(len(Mixer)):   #iteration by row of mixer
        for j in range(len(state_matrix[0])):    # iterating by column of state matrix
            for k in range(len(state_matrix)):             # iterating by rows of state matrix
                if mode == 1:      ## Encryption
                    mult = Mixer[i][k].gf_multiply_modular(BitVector(hexstring=state_matrix[k][j]), AES_modulus, 8)
                else:
                    mult = InvMixer[i][k].gf_multiply_modular(BitVector(hexstring=state_matrix[k][j]), AES_modulus, 8)
                result[i][j] = (BitVector(hexstring=result[i][j]) ^ (mult)).get_bitvector_in_hex()
    result = np.array(result)
    return result
     
## Add Round Key
def Add_RoundKey(state_matrix,round_key_matrix):
    for i in range(0,row):
        for j in range(0,column):
            state_matrix[i][j] = (BitVector(hexstring=state_matrix[i][j]) ^ BitVector(hexstring = round_key_matrix[i][j])).get_bitvector_in_hex()
    return state_matrix


## g function for key expansion
def g_function(word, round_constant):   
    # Circular Byte Shift
    word = np.roll(word, -1)
    # byte substitution
    for i in range(0,4):
        word[i] = byte_substitution(word[i], 1)
    #Add round constant
    for i in range(0,4):
        word[i] = (BitVector(hexstring=round_constant[i]) ^ BitVector(hexstring = word[i])).get_bitvector_in_hex()
    return word

## Key Expansion
def key_expansion(word0, word1, word2, word3, round):   # Key Expansion
    g_word3 = g_function(word3, Round_Constant[round-1])
    for i in range(0,4):
        word0[i] = (BitVector(hexstring=g_word3[i]) ^ BitVector(hexstring = word0[i])).get_bitvector_in_hex()
    for i in range(0,4):
        word1[i] = (BitVector(hexstring=word0[i]) ^ BitVector(hexstring = word1[i])).get_bitvector_in_hex()
    for i in range(0,4):
        word2[i] = (BitVector(hexstring=word1[i]) ^ BitVector(hexstring = word2[i])).get_bitvector_in_hex()
    for i in range(0,4):
        word3[i] = (BitVector(hexstring=word2[i]) ^ BitVector(hexstring = word3[i])).get_bitvector_in_hex()
    return word0, word1, word2, word3

def convert_to_cipher_text(state_matrix):
    cipher_text = ""
    for i in range(len(state_matrix[0])):
        for j in range(len(state_matrix)):
            cipher_text += str(state_matrix[j][i])
    return cipher_text


def All_Round_Key_Gen(key_matrix, word0, word1, word2, word3):
    All_Round_Key = [None] * total_round
    intermediate_round_key = np.empty((4,4), dtype=str)
    All_Round_Key[0] = key_matrix

    for round in range(1, total_round):
        word0, word1, word2, word3 = key_expansion(word0, word1, word2, word3, round)
        intermediate_round_key = np.concatenate((word0, word1, word2, word3))
        intermediate_round_key = np.reshape(intermediate_round_key, (4,4))
        intermediate_round_key = np.transpose(intermediate_round_key)
        All_Round_Key[round] = intermediate_round_key
    All_Round_Key = np.array(All_Round_Key)
    # print("All Round Key: \n", All_Round_Key) 
    return All_Round_Key
    
    
                                                    ##### Encryption #####
def encryption(hex_plaintext, All_Round_Key):
    All_Cipher_matrix = []
    
    ## Round 1- 10 for 128 bits
    mode = 1
    while len(hex_plaintext) != 0:
        
        # take the first 128 bits of the plain text and construct the state matrix
        state_array_1D = hex_plaintext[0:16]
        while len(state_array_1D) < 16:
            state_array_1D.append(format(ord('#'), "x"))
        state_matrix = convert_to_matrix(state_array_1D)
        print("State matrix: \n", state_matrix)
        del hex_plaintext[0:16]
        
        ## Round 0: Add Round Key
        state_matrix = Add_RoundKey(state_matrix, All_Round_Key[0])
        
        ## For Round 1-10
        for round in range(1,total_round):
            
                                    #### 4 steps of encryption ####     
            #First step: Substution Bytes
            for i in range(0,row):
                for j in range(0,column):
                    state_matrix[i][j] = byte_substitution(state_matrix[i][j], mode)
                    
            #Second Step: Shift Row
            state_matrix = Shift_Row_Encryption(state_matrix)
            
            #Third Step: Mix Column
            if round != 10:
                state_matrix = Mix_Column(state_matrix, mode)
            
            #Fourth Step: Add Round Key
            state_matrix = Add_RoundKey(state_matrix, All_Round_Key[round])
        
        All_Cipher_matrix.append(state_matrix)    
        block_cipher = convert_to_cipher_text(state_matrix)   
        print("Cipher Text:")
        print(block_cipher)
    print("All:\n", All_Cipher_matrix)
    return All_Cipher_matrix

                                                    ##### Decryption #####
def Decryption(All_Cipher_Text_matrix, All_Round_Key):
    mode = 0
    index = 0;
    full_text = ""
    while index < len(All_Cipher_Text_matrix):
        state_matrix = All_Cipher_Text_matrix[index]
        ## For Round 0-9
        for round in range(0,total_round-1):
            
                                    #### 4 steps of Decryption ####
            #First Step: Add Round Key
            state_matrix = Add_RoundKey(state_matrix, All_Round_Key[total_round - round - 1])
            
            # Second Step: Mix Column
            if round != 0:
                state_matrix = Mix_Column(state_matrix, mode)
                        
            #Third Step: Shift Row
            state_matrix = Shift_Row_Decryption(state_matrix)
            
            #Fourth step: Substution Bytes
            for i in range(0,row):
                for j in range(0,column):
                    state_matrix[i][j] = byte_substitution(state_matrix[i][j], mode)
        
        ## Round 10: Add Round Key
        state_matrix = Add_RoundKey(state_matrix, All_Round_Key[0])
        
        block_decipher = convert_to_cipher_text(state_matrix)   
        print("Decipher Text:")
        print(block_decipher)
        
        byte_array = bytearray.fromhex(block_decipher)
        text = byte_array.decode()
        if index == len(All_Cipher_Text_matrix) - 1:
            for i in range(len(text)):
                if text[i] == "#":
                    text = text[0:i]
                    break
        print(text)
        full_text += text
        
        index += 1
    return full_text


def main():
    plain_text = input("Enter your text: ")
    print(plain_text)
    no_of_strip_char = 16 - (len(plain_text) % 16)
    key = input("Enter key: ")
    key = key[:16]
    while len(key) < 16:
        key = key + '#'
    print(key)

    # Convert the plain text and key to hex
    hex_plaintext = convert_to_hex(plain_text)
    hex_key = convert_to_hex(key)


    #convert to a 4*4 matrix
    key_matrix = convert_to_matrix(hex_key)

    print("key matrix: \n", key_matrix)

    # Construct word from the matrix
    word0 = np.array(key_matrix[:,0])
    word1 = np.array(key_matrix[:,1])
    word2 = np.array(key_matrix[:,2])
    word3 = np.array(key_matrix[:,3])


    ## All Round Key Generation
    start_key = time.time()
    All_Round_Key = All_Round_Key_Gen(key_matrix, word0, word1, word2, word3)  
    stop_key = time.time()
    
    
    start_enc = time.time()
    All_Cipher_Text_matrix = encryption(hex_plaintext, All_Round_Key)
    stop_enc = time.time()
      

    start_dec = time.time()
    full_text = Decryption(All_Cipher_Text_matrix, All_Round_Key)
    stop_dec = time.time()
    
    print("\nExecution time:")
    print("key Scheduling: ", stop_key-start_key)
    print("Encryption time: ", stop_enc-start_enc) 
    print("Decryption time: ", stop_dec-start_dec) 

    ## Check Similarity
    if plain_text == full_text:
        print("Decryptoin Succesful!!")
        
        
if __name__ == "__main__":
    main()
    

    

