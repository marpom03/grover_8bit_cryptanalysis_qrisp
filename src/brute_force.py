def rotl4(value):
    """Rotate a 4-bit value left by one position."""
    return ((value << 1) | (value >> 3)) & 0xF


def round_function(right, subkey):
    """MiniFeistel-8 round function."""
    return (right & rotl4(right)) ^ subkey


def encrypt(plaintext, key):
    """Encrypt an 8-bit plaintext using an 8-bit key."""

    if not 0 <= plaintext <= 0xFF:
        raise ValueError("Plaintext must be an 8-bit value")

    if not 0 <= key <= 0xFF:
        raise ValueError("Key must be an 8-bit value")

    # Split plaintext into two 4-bit halves
    left = (plaintext >> 4) & 0xF
    right = plaintext & 0xF

    # Generate three round keys
    key_high = (key >> 4) & 0xF
    key_low = key & 0xF

    round_keys = [
        key_high,
        key_low,
        key_high ^ key_low,
    ]

    # Perform three Feistel rounds
    for subkey in round_keys:
        left, right = right, left ^ round_function(right, subkey)

    # Combine the halves without an additional swap
    return (left << 4) | right


def brute_force(plaintext, expected_ciphertext):
    """Return all keys matching the known plaintext-ciphertext pair."""

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