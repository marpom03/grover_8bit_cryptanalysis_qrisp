from src.cipher import encrypt


def brute_force(plaintext, expected_ciphertext):
    """Return all keys matching the known plaintext-ciphertext pair."""

    if not 0 <= plaintext <= 0xFF:
        raise ValueError("Plaintext must be an 8-bit value")

    if not 0 <= expected_ciphertext <= 0xFF:
        raise ValueError("Ciphertext must be an 8-bit value")

    matching_keys = []

    for key in range(256):
        ciphertext = encrypt(plaintext, key)

        if ciphertext == expected_ciphertext:
            matching_keys.append(key)

    return matching_keys


if __name__ == "__main__":
    plaintext = 0xB2
    expected_ciphertext = 0x62

    matching_keys = brute_force(plaintext, expected_ciphertext)

    print(f"Plaintext:  0x{plaintext:02X}")
    print(f"Ciphertext: 0x{expected_ciphertext:02X}")

    print(f"\nMatching keys: {len(matching_keys)}")

    for key in matching_keys:
        print(f"Key: 0x{key:02X} ({key:08b})")