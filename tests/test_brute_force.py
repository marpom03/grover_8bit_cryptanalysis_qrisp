import unittest

from src.brute_force import encrypt, brute_force, rotl4


class TestMiniFeistel8(unittest.TestCase):

    def test_rotation(self):
        self.assertEqual(rotl4(0b0010), 0b0100)
        self.assertEqual(rotl4(0b1101), 0b1011)

    def test_known_encryption(self):
        self.assertEqual(encrypt(0xB2, 0x6D), 0x62)

    def test_brute_force(self):
        self.assertEqual(brute_force(0xB2, 0x62), [0x6D])

    def test_key_recovery(self):
        plaintext = 0xB2

        for key in range(256):
            ciphertext = encrypt(plaintext, key)
            recovered_keys = brute_force(plaintext, ciphertext)

            self.assertIn(key, recovered_keys)

    def test_invalid_key(self):
        with self.assertRaises(ValueError):
            encrypt(0xB2, 256)

    def test_invalid_plaintext(self):
        with self.assertRaises(ValueError):
            encrypt(256, 0x6D)


if __name__ == "__main__":
    unittest.main()