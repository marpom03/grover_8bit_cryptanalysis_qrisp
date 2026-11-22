BLOCK_SIZE = 8
KEY_SIZE = 8
NUM_ROUNDS = 3

MAX_VALUE = 0xFF
HALF_MASK = 0xF


def rotl4(value: int) -> int:
    """Rotate a 4-bit value left by one position."""
    return ((value << 1) | (value >> 3)) & HALF_MASK


def round_function(right: int, round_key: int) -> int:
    """Compute the Feistel round function."""
    return (right & rotl4(right)) ^ round_key


def generate_round_keys(key: int) -> tuple[int, int, int]:
    """Generate three 4-bit round keys from an 8-bit key."""
    if not 0 <= key <= MAX_VALUE:
        raise ValueError("Key must be an 8-bit integer.")

    key_high = (key >> 4) & HALF_MASK
    key_low = key & HALF_MASK

    return (
        key_high,
        key_low,
        key_high ^ key_low,
    )


def encrypt(plaintext: int, key: int) -> int:
    """Encrypt an 8-bit plaintext using an 8-bit key."""
    if not 0 <= plaintext <= MAX_VALUE:
        raise ValueError("Plaintext must be an 8-bit integer.")

    round_keys = generate_round_keys(key)

    left = (plaintext >> 4) & HALF_MASK
    right = plaintext & HALF_MASK

    for round_key in round_keys:
        left, right = right, left ^ round_function(right, round_key)

    return (left << 4) | right


def decrypt(ciphertext: int, key: int) -> int:
    """Decrypt an 8-bit ciphertext using an 8-bit key."""
    if not 0 <= ciphertext <= MAX_VALUE:
        raise ValueError("Ciphertext must be an 8-bit integer.")

    round_keys = generate_round_keys(key)

    left = (ciphertext >> 4) & HALF_MASK
    right = ciphertext & HALF_MASK

    for round_key in reversed(round_keys):
        left, right = right ^ round_function(left, round_key), left

    return (left << 4) | right


if __name__ == "__main__":
    plaintext = 0b10110010
    key = 0b01101101

    ciphertext = encrypt(plaintext, key)
    recovered = decrypt(ciphertext, key)

    print(f"Plaintext:   {plaintext:08b}")
    print(f"Key:         {key:08b}")
    print(f"Ciphertext:  {ciphertext:08b}")
    print(f"Decrypted:   {recovered:08b}")