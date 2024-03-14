import secrets


class Salsa20(object):
    """
    Specification --> https://cr.yp.to/snuffle/spec.pdf
    
    - Message
    - Generate 32-byte key
    - Generate 8-byte nonce
    - Generate keystream --> doubleround^10(x) = rowround(columnround(x))
    - ciphertext --> message XOR keystream
    - decrypted-text --> ciphertext XOR keystream

    # 64-byte input
    # 64-byte output
    """
    def __init__(self, key_length, nonce_length) -> None:
        """
        """
        self.key = self._generate_secret(key_length)
        self.nonce = self._generate_secret(nonce_length)
        self.constant = "expand 32-byte k"
        self.counter = 0

        self.expansion_sequence = []
        self.initial_state_matrix = []
        self.state_matrix = []
        self.state_matrix_elements = []
        self.keystream = None

    def _generate_secret(self, l):
        """
        """
        return secrets.token_bytes(l)

    def _create_expansion_sequence(self):
        """
        """
        # TODO: right now this is hardcoded but need to make this dynamic
        key_first_half = self.key[:16]
        key_second_half = self.key[16:]
        constant_bytes = self.constant.encode('utf-8')
        counter_bytes = (self.counter).to_bytes(8, byteorder='little')

        self.expansion_sequence = [
            key_first_half,
            constant_bytes,
            key_second_half,
            self.nonce + counter_bytes
        ]
        expansion_sequence_bytes = b''.join(self.expansion_sequence)
        
        assert len(expansion_sequence_bytes) * 8 == 512  # TODO: error here? also, should handle dynamic length, not just 512


    def _create_initial_state_matrix(self):
        """
        """
        for p in self.expansion_sequence:
            byte_size = int(len(p) / 4)  # TODO: handle dynamic lengths here? right now, hardcoded at 4
            li = []
            for idx in range(0, len(p), byte_size):
                bt = p[idx:idx+byte_size]
                bt_int = int.from_bytes(bt, byteorder='little')
                li.append(bt_int)

            self.initial_state_matrix.append(li)
            self.state_matrix.append(li)
        
        self.state_matrix_elements = [e for l in self.state_matrix for e in l]


    def _update_state_matrix(self, state_sequence_elements):
        """
        """
        c = 0
        for idx in range(0, len(state_sequence_elements), 4):  # TODO: hardcoded at 4 right now?
            rw = state_sequence_elements[idx:idx+4]
            self.state_matrix[c] = rw
            c += 1

    def _quarter_round(self, a, b, c, d):
        """
        """
        b = b ^ ((a + d) << 7)
        c = c ^ ((b + a) << 9)
        d = d ^ ((c + b) << 13)
        a = a ^ ((d + c) << 18)
        return a, b, c, d


    def _columnround(self):
        """
        """
        self.state_matrix_elements[0], self.state_matrix_elements[4], self.state_matrix_elements[8], self.state_matrix_elements[12] = self._quarter_round(
            self.state_matrix_elements[0], self.state_matrix_elements[4], self.state_matrix_elements[8], self.state_matrix_elements[12]
        )
        self.state_matrix_elements[5], self.state_matrix_elements[9], self.state_matrix_elements[13], self.state_matrix_elements[1] = self._quarter_round(
            self.state_matrix_elements[5], self.state_matrix_elements[9], self.state_matrix_elements[13], self.state_matrix_elements[1]
        )
        self.state_matrix_elements[10], self.state_matrix_elements[14], self.state_matrix_elements[2], self.state_matrix_elements[6] = self._quarter_round(
            self.state_matrix_elements[10], self.state_matrix_elements[14], self.state_matrix_elements[2], self.state_matrix_elements[6]
        )
        self.state_matrix_elements[15], self.state_matrix_elements[3], self.state_matrix_elements[7], self.state_matrix_elements[11] = self._quarter_round(
            self.state_matrix_elements[15], self.state_matrix_elements[3], self.state_matrix_elements[7], self.state_matrix_elements[11]
        )

    def _rowround(self):
        """
        """
        self.state_matrix_elements[0], self.state_matrix_elements[1], self.state_matrix_elements[2], self.state_matrix_elements[3] = self._quarter_round(
            self.state_matrix_elements[0], self.state_matrix_elements[1], self.state_matrix_elements[2], self.state_matrix_elements[3]
        )

        self.state_matrix_elements[4], self.state_matrix_elements[5], self.state_matrix_elements[6], self.state_matrix_elements[7] = self._quarter_round(
            self.state_matrix_elements[4], self.state_matrix_elements[5], self.state_matrix_elements[6], self.state_matrix_elements[7]
        )

        self.state_matrix_elements[8], self.state_matrix_elements[9], self.state_matrix_elements[10], self.state_matrix_elements[11] = self._quarter_round(
            self.state_matrix_elements[8], self.state_matrix_elements[9], self.state_matrix_elements[10], self.state_matrix_elements[11]
        )

        self.state_matrix_elements[12], self.state_matrix_elements[13], self.state_matrix_elements[14], self.state_matrix_elements[15] = self._quarter_round(
            self.state_matrix_elements[12], self.state_matrix_elements[13], self.state_matrix_elements[14], self.state_matrix_elements[15]
        )

    def doubleround(self):
        """
        """
        for _ in range(0, 1):  # TODO: make this 10 rounds
            self._columnround()
            self._update_state_matrix(
                self.state_matrix_elements
            )
            self._rowround()
            self._update_state_matrix(
                self.state_matrix_elements
            )

        # state_matrix_elements = [e for l in self.state_matrix for e in l]
        initial_state_matrix_elements = [e for l in self.initial_state_matrix for e in l]
        
        keystream_output = []
        for idx in range(0, len(initial_state_matrix_elements)):
            modified_elem, initial_elem = self.state_matrix_elements[idx], initial_state_matrix_elements[idx]
            sm = modified_elem + initial_elem
            keystream_output.append(sm)
        
        self.keystream = keystream_output


    def encrypt(self, plaintext):
        """
        """

        try:
            # most cryptographic algorithms, operates on bytes, not text.
            plaintext_bytes = plaintext.encode('utf-8')
        except:
            raise ValueError("Plaintext must be a valid string.")
        
        self._create_expansion_sequence()
        self._create_initial_state_matrix()        
        self.doubleround()
        
        assert len(self.keystream) == 16  # TODO: raise any error here?

        ciphertext = [p ^ k for p, k in zip(plaintext_bytes, self.keystream)]
        return ciphertext

    
    def decrypt(self, ciphertext):
        """
        """
        decrypted_message = ''.join([chr(c^k) for c, k in zip(ciphertext, self.keystream)])
        # print('Dec:', dec_message)
        return decrypted_message


salsa_20 = Salsa20(
    key_length = 32,
    nonce_length = 8
)
# plaintext = "Hello, Salsa20!"

# TODO: 
    # handle arbitrary length input, like below
    # add all errors, abstractions, docstrings, tests
    # publish on documentation and go from there...
        # really want to focus on building some applications with crypto
plaintext = "The dog ran to the park."
ciphertext = salsa_20.encrypt(plaintext)
print(ciphertext)
decrypted_message = salsa_20.decrypt(ciphertext)
print(decrypted_message)





# # original_string = "the dog was running at the park."
# # # Convert the string to bytes
# # bytes_representation = original_string.encode('utf-8')
# # # Convert bytes to hexadecimal
# # hex_representation = bytes_representation.hex()
# # print(hex_representation)

# # key = "00112233445566778899aabbccddeeff" # 16-byte key
# # nonce = "0001020304050607" # 8-byte nonce
# # [
# # ["expa", K0, K1, K2],
# # [“nd 1”, K3, N0, N1],
# # [“6-by”, K0, K1, K2],
# # [“te k”, K3, "00000000", "00000000"]
# # ]

# # key_matrix = []
# # for idx in range(0, len(key), 8):
# #     s = key[idx:idx+8]
# #     key_matrix.append(s)

# # nonce_matrix = []
# # for idx in range(0, len(nonce), 8):
# #     n = nonce[idx:idx+8]
# #     nonce_matrix.append(n)

# # print(nonce_matrix)



# key = secrets.token_bytes(32)
# nonce = secrets.token_bytes(8)
# # message = "The dog ran to the park."
# message = "Hello, Salsa20!"
# # most cryptographic algorithms, operates on bytes, not text.
# message_bytes = message.encode('utf-8')
# # print(message_bytes)

# constant = "expand 32-byte k"
# constant_bytes = constant.encode('utf-8')

# counter = 0
# counter_bytes = (counter).to_bytes(8, byteorder='little')

# expansion_sequence = []
# key_first_half = key[0:16]
# key_second_half = key[16:]
# expansion_sequence = [
#     key_first_half,
#     constant_bytes,
#     key_second_half,
#     nonce + counter_bytes
# ]

# expansion_sequence_bytes = b''.join(expansion_sequence)
# assert len(expansion_sequence_bytes) * 8 == 512

# # quarter-round function
# def quarter_round(a, b, c, d):
#     b = b ^ ((a + d) << 7)
#     c = c ^ ((b + a) << 9)
#     d = d ^ ((c + b) << 13)
#     a = a ^ ((d + c) << 18)
#     return a, b, c, d

# # 64-byte state matrix
# # | | 0 | 1 | 2 | 3 |
# # |---|----|----|----|----|
# # | 0 | k0 | k1 | k2 | k3 |
# # | 1 | c0 | c1 | c2 | c3 |
# # | 2 | n0 | n1 | n2 | n3 |
# # | 3 | v0 | v1 | p0 | p1 |

# state_matrix = []
# for p in expansion_sequence:
#     byte_size = int(len(p) / 4)
#     li = []
#     for idx in range(0, len(p), byte_size):
#         bt = p[idx:idx+byte_size]
#         # print(bt)
#         bt_int = int.from_bytes(bt, byteorder='little')
#         li.append(bt_int)
#     state_matrix.append(li)

# print(f"Initial Matrix:", state_matrix)

# state_matrix_elements = [e for l in state_matrix for e in l]
# print(len(state_matrix_elements))

# # column-wise insertion (columnround(x))
# state_matrix_elements[0], state_matrix_elements[4], state_matrix_elements[8], state_matrix_elements[12] = quarter_round(
#     state_matrix_elements[0], state_matrix_elements[4], state_matrix_elements[8], state_matrix_elements[12]
# )

# state_matrix_elements[5], state_matrix_elements[9], state_matrix_elements[13], state_matrix_elements[1] = quarter_round(
#     state_matrix_elements[5], state_matrix_elements[9], state_matrix_elements[13], state_matrix_elements[1]
# )

# state_matrix_elements[10], state_matrix_elements[14], state_matrix_elements[2], state_matrix_elements[6] = quarter_round(
#     state_matrix_elements[10], state_matrix_elements[14], state_matrix_elements[2], state_matrix_elements[6]
# )

# state_matrix_elements[15], state_matrix_elements[3], state_matrix_elements[7], state_matrix_elements[11] = quarter_round(
#     state_matrix_elements[15], state_matrix_elements[3], state_matrix_elements[7], state_matrix_elements[11]
# )

# print()
# print(f"Modified Matrix:", state_matrix_elements)
# print()
# c = 0
# for idx in range(0, len(state_matrix_elements), 4):
#     rw = state_matrix_elements[idx:idx+4]
#     print(rw)
#     state_matrix[c] = rw
#     c += 1
# print()

# print(state_matrix)

# # row-wise (rowround(x))
# state_matrix_elements[0], state_matrix_elements[1], state_matrix_elements[2], state_matrix_elements[3] = quarter_round(
#     state_matrix_elements[0], state_matrix_elements[1], state_matrix_elements[2], state_matrix_elements[3]
# )

# state_matrix_elements[4], state_matrix_elements[5], state_matrix_elements[6], state_matrix_elements[7] = quarter_round(
#     state_matrix_elements[4], state_matrix_elements[5], state_matrix_elements[6], state_matrix_elements[7]
# )

# state_matrix_elements[8], state_matrix_elements[9], state_matrix_elements[10], state_matrix_elements[11] = quarter_round(
#     state_matrix_elements[8], state_matrix_elements[9], state_matrix_elements[10], state_matrix_elements[11]
# )

# state_matrix_elements[12], state_matrix_elements[13], state_matrix_elements[14], state_matrix_elements[15] = quarter_round(
#     state_matrix_elements[12], state_matrix_elements[13], state_matrix_elements[14], state_matrix_elements[15]
# )

# initial_state_matrix = []
# for p in expansion_sequence:
#     byte_size = int(len(p) / 4)
#     li = []
#     for idx in range(0, len(p), byte_size):
#         bt = p[idx:idx+byte_size]
#         bt_int = int.from_bytes(bt, byteorder='little')
#         li.append(bt_int)
#     initial_state_matrix.append(li)  

# initial_state_matrix_elements = [e for l in initial_state_matrix for e in l]

# enc_output = []
# for idx in range(0, len(initial_state_matrix_elements)):
#     modified_elem, initial_elem = state_matrix_elements[idx], initial_state_matrix_elements[idx]
#     sm = modified_elem + initial_elem
#     enc_output.append(sm)

# print(enc_output)

# ciphertext = [p ^ k for p, k in zip(message_bytes, enc_output)]
# print('Cipher', ciphertext)

# dec_message = ''.join([chr(c^k) for c, k in zip(ciphertext, enc_output)])
# print('Dec:', dec_message)


# # # Convert the state to bytes
# # enc_result = b''
# # for word in enc_output:
# #     enc_result += word.to_bytes(4, 'little')

# # state_matrix_elements = [e for l in state_matrix for e in l]
# # print(len(state_matrix_elements))

# # ciphertext = [p ^ k for p, k in zip(plaintext, keystream_block)]

# ## Decrypt

# # TODO:
#     # Class for Salsa20
#     # Handle arbitrary message lengths
