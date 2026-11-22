from qrisp import QuantumFloat, cx, mcx, x


def xor_constant(register, value):
    """XOR a 4-bit classical constant into a quantum register."""
    for bit in range(4):
        if (value >> bit) & 1:
            x(register[bit])


def quantum_round(left, right, round_key):
    """Apply one reversible MiniFeistel-8 round."""

    # Nonlinear part: R AND ROTL4(R, 1)
    for bit in range(4):
        previous_bit = (bit - 1) % 4

        mcx(
            [right[bit], right[previous_bit]],
            left[bit],
        )

    # XOR with the round key
    xor_constant(left, round_key)

    # Logical swap of the Feistel halves
    return right, left


def quantum_encrypt(plaintext, key):
    """Encrypt an 8-bit plaintext with a classical 8-bit key."""

    if not 0 <= plaintext <= 0xFF:
        raise ValueError("Plaintext must be an 8-bit integer.")

    if not 0 <= key <= 0xFF:
        raise ValueError("Key must be an 8-bit integer.")

    left = QuantumFloat(4)
    right = QuantumFloat(4)

    left[:] = (plaintext >> 4) & 0xF
    right[:] = plaintext & 0xF

    key_high = (key >> 4) & 0xF
    key_low = key & 0xF

    round_keys = (
        key_high,
        key_low,
        key_high ^ key_low,
    )

    for round_key in round_keys:
        left, right = quantum_round(left, right, round_key)

    return left, right

def quantum_round_with_key(left, right, key_bits):
    """Apply a reversible Feistel round with quantum key bits."""

    # Nonlinear part of the round function
    for bit in range(4):
        previous_bit = (bit - 1) % 4

        mcx(
            [right[bit], right[previous_bit]],
            left[bit],
        )

    # XOR with quantum round key
    for bit in range(4):
        for key_bit in key_bits[bit]:
            cx(key_bit, left[bit])

    return right, left


def quantum_encrypt_with_key(plaintext, key_register):
    """Encrypt an 8-bit plaintext using a quantum key register."""

    if not 0 <= plaintext <= 0xFF:
        raise ValueError("Plaintext must be an 8-bit integer.")

    if len(key_register) != 8:
        raise ValueError("Key register must contain 8 qubits.")

    left = QuantumFloat(4)
    right = QuantumFloat(4)

    left[:] = (plaintext >> 4) & 0xF
    right[:] = plaintext & 0xF

    # QuantumFloat uses little-endian bit indexing:
    # indices 0-3: low nibble
    # indices 4-7: high nibble

    key_high = [
        [key_register[bit + 4]]
        for bit in range(4)
    ]

    key_low = [
        [key_register[bit]]
        for bit in range(4)
    ]

    key_xor = [
        [key_register[bit + 4], key_register[bit]]
        for bit in range(4)
    ]

    round_keys = (
        key_high,
        key_low,
        key_xor,
    )

    for round_key in round_keys:
        left, right = quantum_round_with_key(
            left,
            right,
            round_key,
        )

    return left, right

def quantum_decrypt_with_key(left, right, key_register):
    """Reverse MiniFeistel-8 encryption without measurement."""

    if len(key_register) != 8:
        raise ValueError("Key register must contain 8 qubits.")

    key_high = [
        [key_register[bit + 4]]
        for bit in range(4)
    ]

    key_low = [
        [key_register[bit]]
        for bit in range(4)
    ]

    key_xor = [
        [key_register[bit + 4], key_register[bit]]
        for bit in range(4)
    ]

    round_keys = (
        key_high,
        key_low,
        key_xor,
    )

    for round_key in reversed(round_keys):
        left, right = right, left

        for bit in range(4):
            for key_bit in round_key[bit]:
                cx(key_bit, left[bit])

        for bit in reversed(range(4)):
            previous_bit = (bit - 1) % 4

            mcx(
                [right[bit], right[previous_bit]],
                left[bit],
            )

    return left, right

if __name__ == "__main__":
    plaintext = 0b10110010
    key = 0b01101101

    left, right = quantum_encrypt(plaintext, key)

    left_value = next(iter(left.get_measurement()))
    right_value = next(iter(right.get_measurement()))

    ciphertext = (left_value << 4) | right_value

    print(f"Plaintext:   {plaintext:08b}")
    print(f"Key:         {key:08b}")
    print()
    print(f"Left:        {left_value:04b}")
    print(f"Right:       {right_value:04b}")
    print(f"Ciphertext:  {ciphertext:08b}")