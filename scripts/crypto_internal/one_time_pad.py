import warnings
import secrets
import string

class OneTimePad(object):
    """
    Implementation of the One-Time Pad Cipher.

    The one-time pad cipher is a Vigenère cipher where:
    1. The key is exactly as long as the message that is encrypted.
    2. The key is made up of truly random symbols.
    3. The key is used only once for a single message.

    By following these rules, the one-time pad cipher is considered unbreakable.

    Additional Information: https://inventwithpython.com/hacking/chapter22.html
    """

    def __init__(self, key: str) -> None:
        """
        Initialize the OneTimePad object.

        Args:
            key (str): The key for encryption and decryption.

        Raises:
            ValueError: If the provided key is not a valid string.
            Exception: If the key length is 0.
        """
        try:
            key = key.strip()
        except:
            raise ValueError("Key must be a valid string.")
    
        if len(key) == 0:
            raise Exception("Key must have a length greater than 0.")

        self._key = key

    @property
    def key(self) -> str:
        return self._key

    def _check_str(self, name: str, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a valid string.")

    @classmethod
    def generate_key(cls, key_length: int) -> str:
        """
        Generate a cryptographically random one time pad/key for encryption.

        Args:
            key_length (int): The length of the key.

        Returns:
            str: A randomly generated key.

        Raises:
            TypeError: If key_length is not a valid integer.
        """
        if not isinstance(key_length, int):
            raise TypeError("key_length must be a valid integer.")

        return ''.join(secrets.choice(string.ascii_letters) for _ in range(key_length))

    def _operate(self, char1: str, char2: str, operation: str) -> str:
        """
        Perform the specified operation on two characters.

        Args:
            char1 (str): The first character.
            char2 (str): The second character.
            operation (str): The operation to perform ('encrypt' or 'decrypt').

        Returns:
            str: The result of the operation.
        """
        if (not isinstance(char1, str)) or (not isinstance(char2, str)) or len(char1) != 1 or len(char2) != 1:
            raise ValueError("Input characters must be single characters.")

        char1_ord = ord(char1) - 32
        char2_ord = ord(char2) - 32

        if operation == 'encrypt':
            result_ord = (char1_ord + char2_ord) % 95
        elif operation == 'decrypt':
            result_ord = (char1_ord - char2_ord) % 95
        else:
            raise ValueError("Invalid operation. Use 'encrypt' or 'decrypt'.")

        return chr(result_ord + 32)

    def _handle_key_length(self, key: str, text: str) -> str:
        """
        Ensure the key is of the same length as the provided text.

        Args:
            key (str): The key.
            text (str): The text.

        Returns:
            str: The processed key.
        """
        if len(key) < len(text):
            raise Exception("The key must be equal to or greater than the length of the text.")
        
        if len(key) > len(text):
            warnings.warn('Your key is is longer than your plaintext. Will truncate the key to exactly match the length of the text.')
            key = self.key[:len(text)]
            return key
        else:
            return key

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt the provided plaintext using the one-time pad cipher.

        Args:
            plaintext (str): The plaintext to be encrypted.

        Returns:
            str: The encrypted message.

        Raises:
            TypeError: If plaintext is not a valid string.
        
        Algebraic description: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
        """
        self._check_str('plaintext', plaintext)
        key = self._handle_key_length(self.key, plaintext)

        encrypted_msg = ""
        for m, c in zip(plaintext, key):
            e_char = self._operate(m, c, 'encrypt')
            encrypted_msg += e_char
        return encrypted_msg

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt the provided ciphertext using the one-time pad cipher.

        Args:
            ciphertext (str): The ciphertext to be decrypted.

        Returns:
            str: The decrypted message.

        Raises:
            TypeError: If ciphertext is not a valid string.
        
        Algebraic description: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
        """
        self._check_str('ciphertext', ciphertext)
        key = self._handle_key_length(self.key, ciphertext)
        
        decrypted_msg = ""
        for c, k in zip(ciphertext, key):
            d_char = self._operate(c, k, 'decrypt')
            decrypted_msg += d_char
        return decrypted_msg
