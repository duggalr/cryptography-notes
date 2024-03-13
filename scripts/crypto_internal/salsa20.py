

# 64-byte input
# 64-byte output


class Salsa20(object):
    """
    """
    pass



# original_string = "the dog was running at the park."
# # Convert the string to bytes
# bytes_representation = original_string.encode('utf-8')
# # Convert bytes to hexadecimal
# hex_representation = bytes_representation.hex()
# print(hex_representation)

# key = "00112233445566778899aabbccddeeff" # 16-byte key
# nonce = "0001020304050607" # 8-byte nonce
# [
# ["expa", K0, K1, K2],
# [“nd 1”, K3, N0, N1],
# [“6-by”, K0, K1, K2],
# [“te k”, K3, "00000000", "00000000"]
# ]

# key_matrix = []
# for idx in range(0, len(key), 8):
#     s = key[idx:idx+8]
#     key_matrix.append(s)

# nonce_matrix = []
# for idx in range(0, len(nonce), 8):
#     n = nonce[idx:idx+8]
#     nonce_matrix.append(n)

# print(nonce_matrix)

import secrets

key = secrets.token_bytes(32)
nonce = secrets.token_bytes(8)
message = "The dog ran to the park."
# most cryptographic algorithms, operates on bytes, not text.
message_bytes = message.encode('utf-8')

constant = "expand 32-byte k"
constant_bytes = constant.encode('utf-8')

counter = 0
counter_bytes = (counter).to_bytes(8, byteorder='little')

expansion_sequence = []
key_first_half = key[0:16]
key_second_half = key[16:]
expansion_sequence = [
    key_first_half,
    constant_bytes,
    key_second_half,
    nonce + counter_bytes
]
# print(expansion_sequence)

expansion_sequence_bytes = b''.join(expansion_sequence)
# print(len(expansion_sequence_bytes))
# # print(expansion_sequence_bytes)
# if len(expansion_sequence_bytes) * 8 == 512:
#     print('correct')

# quarter-round function
def quarter_round(a, b, c, d):
    b = b ^ ((a + d) << 7)
    c = c ^ ((b + a) << 9)
    d = d ^ ((c + b) << 13)
    a = a ^ ((d + c) << 18)
    return a, b, c, d

# 64-byte state matrix
# | | 0 | 1 | 2 | 3 |
# |---|----|----|----|----|
# | 0 | k0 | k1 | k2 | k3 |
# | 1 | c0 | c1 | c2 | c3 |
# | 2 | n0 | n1 | n2 | n3 |
# | 3 | v0 | v1 | p0 | p1 |

state_matrix = []
for p in expansion_sequence:
    byte_size = int(len(p) / 4)
    li = []
    for idx in range(0, len(p), byte_size):
        bt = p[idx:idx+byte_size]
        # print(bt)
        bt_int = int.from_bytes(bt, byteorder='little')
        li.append(bt_int)
    state_matrix.append(li)

print(f"Initial Matrix:", state_matrix)

state_matrix_elements = [e for l in state_matrix for e in l]
print(len(state_matrix_elements))

# column-wise insertion (columnround(x))
state_matrix_elements[0], state_matrix_elements[4], state_matrix_elements[8], state_matrix_elements[12] = quarter_round(
    state_matrix_elements[0], state_matrix_elements[4], state_matrix_elements[8], state_matrix_elements[12]
)

state_matrix_elements[5], state_matrix_elements[9], state_matrix_elements[13], state_matrix_elements[1] = quarter_round(
    state_matrix_elements[5], state_matrix_elements[9], state_matrix_elements[13], state_matrix_elements[1]
)

state_matrix_elements[10], state_matrix_elements[14], state_matrix_elements[2], state_matrix_elements[6] = quarter_round(
    state_matrix_elements[10], state_matrix_elements[14], state_matrix_elements[2], state_matrix_elements[6]
)

state_matrix_elements[15], state_matrix_elements[3], state_matrix_elements[7], state_matrix_elements[11] = quarter_round(
    state_matrix_elements[15], state_matrix_elements[3], state_matrix_elements[7], state_matrix_elements[11]
)

print()
print(f"Modified Matrix:", state_matrix_elements)
print()
c = 0
for idx in range(0, len(state_matrix_elements), 4):
    rw = state_matrix_elements[idx:idx+4]
    print(rw)
    state_matrix[c] = rw
    c += 1
print()

print(state_matrix)

# row-wise (rowround(x))
state_matrix_elements[0], state_matrix_elements[1], state_matrix_elements[2], state_matrix_elements[3] = quarter_round(
    state_matrix_elements[0], state_matrix_elements[1], state_matrix_elements[2], state_matrix_elements[3]
)

state_matrix_elements[4], state_matrix_elements[5], state_matrix_elements[6], state_matrix_elements[7] = quarter_round(
    state_matrix_elements[4], state_matrix_elements[5], state_matrix_elements[6], state_matrix_elements[7]
)

state_matrix_elements[8], state_matrix_elements[9], state_matrix_elements[10], state_matrix_elements[11] = quarter_round(
    state_matrix_elements[8], state_matrix_elements[9], state_matrix_elements[10], state_matrix_elements[11]
)

state_matrix_elements[12], state_matrix_elements[13], state_matrix_elements[14], state_matrix_elements[15] = quarter_round(
    state_matrix_elements[12], state_matrix_elements[13], state_matrix_elements[14], state_matrix_elements[15]
)

# # after doubleround function, add the state_matrix back to original input
# # print(message_bytes)
# # print(len(message_bytes))
# print(expansion_sequence_bytes)
# print(len(expansion_sequence_bytes))
# print(len(state_matrix_elements))

initial_state_matrix = []
for p in expansion_sequence:
    byte_size = int(len(p) / 4)
    li = []
    for idx in range(0, len(p), byte_size):
        bt = p[idx:idx+byte_size]
        bt_int = int.from_bytes(bt, byteorder='little')
        li.append(bt_int)
    initial_state_matrix.append(li)  

# print(f"Initial Matrix:", initial_state_matrix)
initial_state_matrix_elements = [e for l in initial_state_matrix for e in l]
# print(f"Initial Matrix Elements:", initial_state_matrix_elements)

enc_output = []
for idx in range(0, len(initial_state_matrix_elements)):
    modified_elem, initial_elem = state_matrix_elements[idx], initial_state_matrix_elements[idx]
    sm = modified_elem + initial_elem
    enc_output.append(sm)

print(enc_output)

# Convert the state to bytes
enc_result = b''
for word in enc_output:
    enc_result += word.to_bytes(4, 'little')

# state_matrix_elements = [e for l in state_matrix for e in l]
# print(len(state_matrix_elements))

# TODO:
    # implement the decrypt method and go from there...

