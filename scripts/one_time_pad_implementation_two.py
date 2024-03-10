import secrets
import string



def generate_one_time_pad(key_length):
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(key_length))

def _encrypt_operate(m, k):
    m_ord = ord(m)
    k_ord = ord(k)
    enc_ord = ((m_ord - 32 + k_ord - 32) % 95) + 32
    return chr(enc_ord)

def _decrypt_operate(c, k):
    c_ord = ord(c)
    k_ord = ord(k)
    dec_ord = (((c_ord - 32) - (k_ord - 32)) % 95) + 32
    return chr(dec_ord)

def encrypt(key, plaintext):
    msg_num_of_characters = len(plaintext)
    encrypted_msg = ""
    for idx in range(0, msg_num_of_characters):
        m = plaintext[idx]
        c = key[idx]
        e_char = _encrypt_operate(m, c)
        encrypted_msg += e_char
    return encrypted_msg

def decrypt(key, ciphertext):
    ciphertext_num_of_characters = len(ciphertext)
    decrypted_msg = ""
    for idx in range(0, ciphertext_num_of_characters):
        c = ciphertext[idx]
        k = key[idx]
        d_char = _decrypt_operate(c, k)
        decrypted_msg += d_char
    return decrypted_msg



key = generate_one_time_pad(12)
message = 'attackatdawn'
print(f"Message: {message}")
print(f"Key: {key}")

enc_message = encrypt(key, message)
dec_message = decrypt(key, enc_message)
print(f"Encrypted Message: {enc_message}")
print(f"Decrypted Message: {dec_message}")


# TODO:
    # create classes for both
    # add a few basic unit tests <-- asking gpt here would be nice (use vscode AI based extension)
    # autogenerate documentation
        # host on site (these are my notes for this site) <-- documentation of the classes should be main
            # dynamic input available on site?
 
    
