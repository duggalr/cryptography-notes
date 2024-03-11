import base64
import os
import warnings
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


class OneTimePad(object):
    """
    """
    
    def __init__(self, key: str) -> None:
        """
        """
        try:
            key = key.strip()
        except:
            raise ValueError("Key must be a valid string.")
    
        if len(key) == 0:
            raise Exception("Key must have length > 0.")

        self.key = key

        # if plaintext is not None and len(plaintext.strip()) == 0:
        #     raise Exception("Plaintext must have length > 0.")
        
        # if key is not None and len(key.strip()) == 0:
        #     raise Exception("Key must have length > 0.")

        # if plaintext is not None and key is not None and len(key) < len(plaintext):
        #     raise Exception("The key must be equal to or greater than the length of the plaintext.")

        # if len(key) > len(plaintext):
        #     warnings.warn('Your key is is longer than your plaintext. Will truncate the key to exactly match the length of the plaintext...')
        #     length_of_plaintext = len(plaintext)
        #     self.key = key[:length_of_plaintext]
        #     self.plaintext = plaintext
        # else:
        #     self.plaintext = plaintext
        #     self.key = key

    @classmethod
    def generate_key(cls, key_length: int) -> str:
        """
        """
        if not isinstance(key_length, int):
            raise TypeError("key_length must be a valid integer.")

        return ''.join(secrets.choice(string.ascii_lowercase) for _ in range(key_length))

    def _encrypt_operate(self, m: str, c: str) -> str:
        """
        """
        return (string.ascii_lowercase.index(m) + string.ascii_lowercase.index(c)) % 26

    def _decrypt_operate(self, c: str, k: str) -> str:
        """
        """
        return (string.ascii_letters.index(c) - string.ascii_letters.index(k)) % 26

    def encrypt(self, plaintext: str) -> str:
        """
        """
        if not isinstance(plaintext, str):
            raise TypeError("plaintext must be a valid string.")

        msg_num_of_characters = len(plaintext)
        if len(self.key) < len(plaintext):
            raise Exception("The key must be equal to or greater than the length of the plaintext.")
        
        encrypted_msg = ""
        for idx in range(0, msg_num_of_characters):
            m = plaintext[idx]
            c = self.key[idx]
            e_idx = self._encrypt_operate(m, c)
            e_char = string.ascii_lowercase[e_idx]
            encrypted_msg += e_char
        return encrypted_msg

    def decrypt(self, ciphertext: str) -> str:
        """
        """
        if not isinstance(ciphertext, str):
            raise TypeError("ciphertext must be a valid string.")
        
        ciphertext_num_of_characters = len(ciphertext)
        if len(self.key) < len(ciphertext):
            raise Exception("The key must be equal to or greater than the length of the plaintext.")

        decrypted_msg = ""
        for idx in range(0, ciphertext_num_of_characters):
            c = ciphertext[idx]
            k = self.key[idx]
            e_idx = self._decrypt_operate(c, k)
            e_char = string.ascii_lowercase[e_idx]
            decrypted_msg += e_char
        return decrypted_msg

# TODO:
    # leverage AI to refactor above code and generate documentation
    # do same for other implementation
    # auto-generate docs and see how it looks in html

data = 'This is a class method.'
key_length = len(data)
cipher_key = OneTimePad.generate_key(key_length)
print(cipher_key)

otp = OneTimePad(key = cipher_key)
enc_data = otp.encrypt(data)
print(enc_data)


# def generate_one_time_pad(key_length):
#     return ''.join(secrets.choice(string.ascii_letters) for _ in range(key_length))

# def _encrypt_operate(m: str, c: str) -> str:
#     """
#     """
#     return (string.ascii_lowercase.index(m) + string.ascii_lowercase.index(c)) % 26

# def _decrypt_operate(c: str, k: str) -> str:
#     return (string.ascii_letters.index(c) - string.ascii_letters.index(k)) % 26

# def encrypt(key: str, plaintext: str):
#     msg_num_of_characters = len(plaintext)
#     encrypted_msg = ""
#     for idx in range(0, msg_num_of_characters):
#         m = plaintext[idx]
#         c = key[idx]
#         e_idx = _encrypt_operate(m, c)
#         e_char = string.ascii_lowercase[e_idx]
#         encrypted_msg += e_char
#     return encrypted_msg

# def decrypt(key: str, ciphertext: str):
#     ciphertext_num_of_characters = len(ciphertext)
#     decrypted_msg = ""
#     for idx in range(0, ciphertext_num_of_characters):
#         c = ciphertext[idx]
#         k = key[idx]
#         e_idx = _decrypt_operate(c, k)
#         e_char = string.ascii_lowercase[e_idx]
#         decrypted_msg += e_char
#     return decrypted_msg


# message = "attackatdawn"
# key = "lemonlemonle"
# ciphertext = encrypt(key, message)
# print(ciphertext)
# decrypted_message = decrypt(key, ciphertext)
# print(decrypted_message)

