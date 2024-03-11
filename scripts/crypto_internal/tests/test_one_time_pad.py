import os
import sys
# Credit for below line: https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
# from scripts.crypto_internal.one_time_pad import OneTimePad
from one_time_pad import OneTimePad


class TestOneTimePad(unittest.TestCase):
    """
    Test cases for the OneTimePad class.

    Usage:
        python -m unittest test_one_time_pad.py
    """
    def test_encrypt_decrypt(self):
        data = 'This is a class method.'
        key = OneTimePad.generate_key(len(data))
        otp = OneTimePad(key = key)
        enc_data = otp.encrypt(data)
        dec_data = otp.decrypt(enc_data)
        self.assertEqual(dec_data, data)

    def test_generate_key(self):
        key_length = 15
        key = OneTimePad.generate_key(key_length)
        self.assertEqual(len(key), key_length)

    def test_key_truncation(self):
        data = 'Short message.'
        key = OneTimePad.generate_key(20)
        otp = OneTimePad(key=key)

        with self.assertWarns(Warning):
            enc_data = otp.encrypt(data)
            dec_data = otp.decrypt(enc_data)
            self.assertEqual(dec_data, data)

    def test_invalid_plaintext(self):
        with self.assertRaises(TypeError):
            otp = OneTimePad()
            otp.encrypt(123)

    def test_invalid_ciphertext(self):
        with self.assertRaises(TypeError):
            otp = OneTimePad()
            otp.decrypt(123)

    def test_none_key(self):
        with self.assertRaises(ValueError):
            otp = OneTimePad(key=None)

    def test_key_length_zero(self):
        with self.assertRaises(Exception):
            otp = OneTimePad(key='')

        
if __name__=='__main__':
	unittest.main()
