import base64
import os
import string
import secrets

# class OneTimePad(object):
#     """
#     Implementation of Basic One Time Pad

#     The one-time pad cipher is an unbreakable cipher. It is a Vigenère cipher where:

#     1. The key is exactly as long as the message that is encrypted.
#     2. The key is made up of truly random symbols.
#     3. The key is used one time only, and never used again for any other message.

#     By following these three rules, your encrypted message will be invulnerable to any cryptanalyst’s attack.
#     Even with literally an infinite amount of computing power, the cipher cannot be broken.

#     Notes Source: https://inventwithpython.com/hacking/chapter22.html
#     """
    
#     def __init__(self, msg: str) -> None:
#         """
#         """
#         if len(msg) == 0:
#             raise Exception("Message must have length > 0.")
        
#         # self.message = msg
#         # self.one_time_pad = "lemonlemonle"
#         # self.encrypted_message = None

#     # def set_message(self, msg: str) -> None:
#     #     """
#     #     """
#     #     self.message = msg
    
#     # def get_message(self) -> str:
#     #     """
#     #     """
#     #     return self.message
    
#     def _operate(self, m: str, c: str) -> str:
#         """
#         """
#         return (string.ascii_lowercase.index(m) + string.ascii_lowercase.index(c)) % 26


#     def generate_one_time_pad(self, length) -> str:
#         """
#         """
#         pass

#     def encrypt(self, message: str, ) -> str:
#         """
#         # TODO: display the math formula properly
#         C = E(M) = (M + K) % 26
#         """
#         msg_num_of_characters = len(self.message)
#         encrypted_msg = ""
#         for idx in range(0, msg_num_of_characters):
#             m = self.message[idx]
#             c = self.one_time_pad[idx]
#             e_idx = self._operate(m, c)
#             e_char = string.ascii_lowercase[e_idx]
#             encrypted_msg += e_char
        
#         self.encrypted_message = encrypted_msg
#         return encrypted_msg

#     def decrypt(self) -> None:
#         """
#         """
#         encrypted_msg_num_of_characters = len(self.encrypted_message)
#         for idx in range(0, encrypted_msg_num_of_characters):
#             m = self.message[idx]
#             c = self.one_time_pad[idx]
#             e_idx = self._operate(m, c)
#             e_char = string.ascii_lowercase[e_idx]
#             encrypted_msg += e_char





# ex = base64.urlsafe_b64encode(os.urandom(32))
# print(ex)
# print( base64.urlsafe_b64decode(ex))

# TODO: 
    # add tests
    # add doc-string generation

    # compare with existing prod implementations

# print((20 + 24) % 26)
    
# message = "attackatdawn"
# one_time_pad = OneTimePad(message)
# encrypted_message = one_time_pad.encrypt()
# print(encrypted_message)


def generate_one_time_pad(key_length):
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(key_length))

def _encrypt_operate(m: str, c: str) -> str:
    """
    """
    return (string.ascii_lowercase.index(m) + string.ascii_lowercase.index(c)) % 26

def _decrypt_operate(c: str, k: str) -> str:
    return (string.ascii_letters.index(c) - string.ascii_letters.index(k)) % 26

def encrypt(key: str, plaintext: str):
    msg_num_of_characters = len(plaintext)
    encrypted_msg = ""
    for idx in range(0, msg_num_of_characters):
        m = plaintext[idx]
        c = key[idx]
        e_idx = _encrypt_operate(m, c)
        e_char = string.ascii_lowercase[e_idx]
        encrypted_msg += e_char
    return encrypted_msg

def decrypt(key: str, ciphertext: str):
    ciphertext_num_of_characters = len(ciphertext)
    decrypted_msg = ""
    for idx in range(0, ciphertext_num_of_characters):
        c = ciphertext[idx]
        k = key[idx]
        e_idx = _decrypt_operate(c, k)
        e_char = string.ascii_lowercase[e_idx]
        decrypted_msg += e_char
    return decrypted_msg


message = "attackatdawn"
key = "lemonlemonle"
ciphertext = encrypt(key, message)
print(ciphertext)
decrypted_message = decrypt(key, ciphertext)
print(decrypted_message)

