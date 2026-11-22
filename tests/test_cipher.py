import unittest

from src.cipher import (
    decrypt,
    encrypt,
    generate_round_keys,
    rotl4,
    round_function,
)


class TestMiniFeistel8(unittest.TestCase):

    def test_rotation(self):
        self.assertEqual(rotl4(0b0010), 0b0100)
        self.assertEqual(rotl4(0b1001), 0b0011)

    def test_round_function(self):
        self.assertEqual(
            round_function(0b0010, 0b0110),
            0b0110,
        )

    def test_round_keys(self):
        self.assertEqual(
            generate_round_keys(0x6D),
            (0x6, 0xD, 0xB),
        )

    def test_encryption(self):
        self.assertEqual(encrypt(0xB2, 0x6D), 0x62)

    def test_decryption(self):
        self.assertEqual(decrypt(0x62, 0x6D), 0xB2)

    def test_all_plaintexts_and_keys(self):
        for key in range(256):
            for plaintext in range(256):
                ciphertext = encrypt(plaintext, key)
                recovered = decrypt(ciphertext, key)

                self.assertEqual(recovered, plaintext)

    def test_invalid_plaintext(self):
        with self.assertRaises(ValueError):
            encrypt(256, 0)

    def test_invalid_key(self):
        with self.assertRaises(ValueError):
            encrypt(0, 256)

    def test_invalid_ciphertext(self):
        with self.assertRaises(ValueError):
            decrypt(-1, 0)


if __name__ == "__main__":
    unittest.main()