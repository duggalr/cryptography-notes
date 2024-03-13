

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
counter_bytes = (counter).to_bytes(8, byteorder='big')

expansion_sequence = []
key_frst_half = key[0:16]
key_second_half = key[16:]
expansion_sequence = [
    key_frst_half,
    constant_bytes,
    nonce,
    key_second_half,
    counter_bytes
]
# print(expansion_sequence)

expansion_sequence_bytes = b''.join(expansion_sequence)
print(len(expansion_sequence_bytes))
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

for idx in range(0, len(expansion_sequence_bytes), 4):
    s = expansion_sequence_bytes[idx:idx+4]
    print(s)


# TODO: 
    # continue with implementation here

