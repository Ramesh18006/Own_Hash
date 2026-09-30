#Implement a simple hashing algorithm of your own. Combining the components learnt.
#(Rotation, Shift bits, permutation, Substitution) Ensure Determinism, Pre Image Resistance
MASK32 = 0xFFFFFFFF

# Fixed initial state
INITIAL_STATE = [
    0x243F6A88,
    0x85A308D3,
    0x13198A2E,
    0x03707344
]

# Fixed round constants
ROUND_CONSTANTS = [
    0xA4093822,
    0x299F31D0,
    0x082EFA98,
    0xEC4E6C89,
    0x452821E6,
    0x38D01377,
    0xBE5466CF,
    0x34E90C6C
]

ROTATION_AMOUNTS = [5, 11, 17, 23]


# Substitute each byte using a fixed mathematical rule
def substitute(value):
    result = 0

    for shift in (24, 16, 8, 0):
        byte = (value >> shift) & 0xFF
        substituted_byte = (197 * byte + 123) % 256
        result = (result << 8) | substituted_byte

    return result


# Shift bits and combine the result with XOR
def shift_mix(value):
    left_shift = (value << 7) & MASK32
    right_shift = value >> 9

    return (value ^ left_shift ^ right_shift) & MASK32


# Rearrange the four bytes
def permute(value):
    b0 = (value >> 24) & 0xFF
    b1 = (value >> 16) & 0xFF
    b2 = (value >> 8) & 0xFF
    b3 = value & 0xFF

    return (b1 << 24) | (b3 << 16) | (b0 << 8) | b2


# Rotate bits to the left
def rotate_left(value, amount):
    value &= MASK32

    return (
        (value << amount) |
        (value >> (32 - amount))
    ) & MASK32


# Add padding and the original message length
def pad_message(message):
    message_bytes = message.encode("utf-8")
    original_bit_length = len(message_bytes) * 8

    padded = bytearray(message_bytes)
    padded.append(0x80)

    while len(padded) % 16 != 8:
        padded.append(0x00)

    padded.extend(original_bit_length.to_bytes(8, byteorder="big"))

    return padded


# Main hashing function
def rsph128(message):
    padded_message = pad_message(message)
    state = INITIAL_STATE.copy()

    # Process the message in 16-byte blocks
    for block_start in range(0, len(padded_message), 16):
        block = padded_message[block_start:block_start + 16]

        # Divide each block into four 32-bit words
        block_words = [
            int.from_bytes(block[i:i + 4], byteorder="big")
            for i in range(0, 16, 4)
        ]

        # Perform eight rounds of mixing
        for round_number in range(8):
            old_state = state.copy()
            new_state = [0, 0, 0, 0]

            for i in range(4):
                value = (
                    old_state[i]
                    ^ block_words[(i + round_number) % 4]
                    ^ ROUND_CONSTANTS[round_number]
                    ^ ((round_number + 1) * 0x9E3779B9)
                ) & MASK32

                value = substitute(value)
                value = shift_mix(value)
                value = permute(value)
                value = rotate_left(value, ROTATION_AMOUNTS[i])

                new_state[i] = (
                    value
                    + old_state[(i + 1) % 4]
                    + block_words[(i + 2) % 4]
                ) & MASK32

            state = new_state

    # Combine four 32-bit words into a 128-bit hash
    digest = "".join(f"{word:08x}" for word in state)

    return digest


# Get input and display its hash
message = input("Enter your message: ")

hash_value = rsph128(message)

print("RSPH-128 Hash:", hash_value)