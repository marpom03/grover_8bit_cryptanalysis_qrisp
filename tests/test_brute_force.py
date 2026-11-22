import unittest

from src.brute_force import brute_force
from src.cipher import encrypt


class TestBruteForce(unittest.TestCase):

    def test_known_key_recovery(self):
        """Recover the key from the reference plaintext-ciphertext pair."""
        self.assertEqual(brute_force(0xB2, 0x62), [0x6D])

    def test_all_keys_recovery(self):
        """Verify that every key can be recovered."""
        plaintext = 0xB2

        for key in range(256):
            ciphertext = encrypt(plaintext, key)
            recovered_keys = brute_force(plaintext, ciphertext)

            self.assertIn(key, recovered_keys)

    def test_invalid_plaintext(self):
        """Reject plaintext values outside the 8-bit range."""
        with self.assertRaises(ValueError):
            brute_force(256, 0x62)

    def test_invalid_ciphertext(self):
        """Reject ciphertext values outside the 8-bit range."""
        with self.assertRaises(ValueError):
            brute_force(0xB2, 256)


if __name__ == "__main__":
    unittest.main()