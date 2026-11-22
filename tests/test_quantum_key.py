import unittest
from qrisp import QuantumFloat, h, multi_measurement
from src.cipher import encrypt
from src.quantum_cipher import quantum_decrypt_with_key, quantum_encrypt_with_key


class TestQuantumKey(unittest.TestCase):

    def test_known_key(self):
        plaintext = 0b10110010
        key = 0b01101101

        key_register = QuantumFloat(8)
        key_register[:] = key

        left, right = quantum_encrypt_with_key(
            plaintext,
            key_register,
        )

        left_value = next(iter(left.get_measurement()))
        right_value = next(iter(right.get_measurement()))

        ciphertext = (left_value << 4) | right_value

        self.assertEqual(ciphertext, encrypt(plaintext, key))

    def test_multiple_keys(self):
        plaintext = 0b10110010

        test_keys = [
            0b00000000,
            0b00000001,
            0b01101101,
            0b10101010,
            0b11111111,
        ]

        for key in test_keys:
            with self.subTest(key=key):
                key_register = QuantumFloat(8)
                key_register[:] = key

                left, right = quantum_encrypt_with_key(
                    plaintext,
                    key_register,
                )

                left_value = next(iter(left.get_measurement()))
                right_value = next(iter(right.get_measurement()))

                ciphertext = (left_value << 4) | right_value

                self.assertEqual(
                    ciphertext,
                    encrypt(plaintext, key),
                )
    def test_key_superposition(self):
        plaintext = 0b10110010
        key_register = QuantumFloat(8)

        # Create an equal superposition of all 256 keys
        h(key_register)
        left, right = quantum_encrypt_with_key(
            plaintext,
            key_register,
        )

        # Measure the key register
        key_distribution = key_register.get_measurement()
        self.assertEqual(len(key_distribution), 256)
        for probability in key_distribution.values():
            self.assertAlmostEqual(probability, 1 / 256)
        # Verify that the key remains in superposition
        self.assertAlmostEqual(
            sum(key_distribution.values()),
            1.0,
        )

    def test_reversibility(self):
        plaintext = 0b10110010
        key = 0b01101101

        key_register = QuantumFloat(8)
        key_register[:] = key

        left, right = quantum_encrypt_with_key(
            plaintext,
            key_register,
        )

        left, right = quantum_decrypt_with_key(
            left,
            right,
            key_register,
        )

        left_value = next(iter(left.get_measurement()))
        right_value = next(iter(right.get_measurement()))

        recovered = (left_value << 4) | right_value

        self.assertEqual(recovered, plaintext)

    def test_superposition_reversibility(self):
        plaintext = 0b10110010

        key_register = QuantumFloat(8)
        h(key_register)

        left, right = quantum_encrypt_with_key(
            plaintext,
            key_register,
        )

        left, right = quantum_decrypt_with_key(
            left,
            right,
            key_register,
        )

        # Check that the plaintext is recovered
        left_distribution = left.get_measurement()
        right_distribution = right.get_measurement()

        self.assertEqual(
            left_distribution,
            {(plaintext >> 4) & 0xF: 1.0},
        )

        self.assertEqual(
            right_distribution,
            {plaintext & 0xF: 1.0},
        )

        # Check that all 256 keys remain equally probable
        key_distribution = key_register.get_measurement()

        self.assertEqual(len(key_distribution), 256)

        for probability in key_distribution.values():
            self.assertAlmostEqual(probability, 1 / 256)

    def test_superposition_encryption_consistency(self):
        plaintext = 0b10110010

        key_register = QuantumFloat(8)
        h(key_register)

        left, right = quantum_encrypt_with_key(
            plaintext,
            key_register,
        )

        # Joint measurement distribution of all three registers
        distribution = multi_measurement(
            [key_register, left, right]
        )

        self.assertEqual(len(distribution), 256)

        for (key, left_value, right_value), probability in distribution.items():
            ciphertext = (left_value << 4) | right_value

            self.assertEqual(
                ciphertext,
                encrypt(plaintext, key),
            )

            self.assertAlmostEqual(
                probability,
                1 / 256,
                delta=1e-6,
            )

    def test_superposition_phase_coherence(self):
        plaintext = 0b10110010

        key_register = QuantumFloat(8)
        h(key_register)

        left, right = quantum_encrypt_with_key(
            plaintext,
            key_register,
        )

        left, right = quantum_decrypt_with_key(
            left,
            right,
            key_register,
        )

        # Reverse the initial Hadamard transformation
        h(key_register)

        # All amplitudes should interfere at key value zero
        key_distribution = key_register.get_measurement()

        self.assertAlmostEqual(
            key_distribution.get(0, 0.0),
            1.0,
            delta=1e-6,
        )

        # Verify that the plaintext was recovered
        self.assertEqual(
            left.get_measurement(),
            {(plaintext >> 4) & 0xF: 1.0},
        )

        self.assertEqual(
            right.get_measurement(),
            {plaintext & 0xF: 1.0},
        )

if __name__ == "__main__":
    unittest.main()