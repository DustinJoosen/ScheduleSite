
KEY = "********"
OFFSET = 32


def substitution_encryption(value: str) -> str:
    # Make the key large enough to fit the whole plaintext.
    key: str = KEY
    while len(key) < len(value):
        key += key

    cipher_text: str = ""

    # Encrypt everything letter by letter. using XOR
    for i in range(len(value)):
        # Encrypt both the value and the key to ascii, then binary.
        value_bin: str = bin(ord(value[i]))[2:]
        key_bin: str = bin(ord(key[i]))[2:]

        # Ensure both values are of the same length by adding zeroes in front
        while len(value_bin) != len(key_bin):
            if len(value_bin) > len(key_bin):
                key_bin = "0" + key_bin
            if len(key_bin) > len(value_bin):
                value_bin = "0" + value_bin

        # Xor the value and key bin characters.
        encrypted_bin: str = ""
        for j in range(len(value_bin)):
            encrypted_bin += str(int(value_bin[j] != key_bin[j]))

        # Convert bin to ascii and then to chr
        encrypted_ascii = int(encrypted_bin, 2) + OFFSET
        cipher_text += chr(encrypted_ascii)

    return cipher_text


def substitution_decryption(cipher_text: str) -> str:
    # Make the key large enough to fit the whole plaintext.
    key: str = KEY
    while len(key) < len(cipher_text):
        key += key

    plain_text: str = ""

    for i in range(len(cipher_text)):
        cipher_bin: str = bin(ord(cipher_text[i]))[2:]
        key_bin: str = bin(ord(key[i]))[2:]

        # Ensure both values are of the same length by adding zeroes in front
        while len(cipher_bin) != len(key_bin):
            if len(cipher_bin) > len(key_bin):
                key_bin = "0" + key_bin
            if len(key_bin) > len(cipher_bin):
                cipher_bin = "0" + cipher_bin

        # Decrypt using XOR
        decrypted_bin: str = ""
        for j in range(len(cipher_bin)):
            decrypted_bin += str(int(cipher_bin[j] != key_bin[j]))

        # Convert bin back to ascii and then chars
        decrypted_ascii = int(decrypted_bin, 2) + OFFSET
        plain_text += chr(decrypted_ascii)

    return plain_text


def transposition_encryption(value: str) -> str:
    return value


def transposition_decryption(value: str) -> str:
    return value
