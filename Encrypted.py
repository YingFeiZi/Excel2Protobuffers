import pickle
import sys

# 定义密钥
KEY_LENGTH = "fbframework"
XOR_KEY = bytearray(KEY_LENGTH.encode('utf-8'))

def serialize_to_byte(obj):
    serialized_data = pickle.dumps(obj)
    encrypted_data = xor_cipher(serialized_data, XOR_KEY)
    return encrypted_data

def deserialize_from_byte(encrypted_data):
    decrypted_data = xor_cipher(encrypted_data, XOR_KEY)
    obj = pickle.loads(decrypted_data)
    return obj

def xor_cipher_default(input_bytes):
    return encrypt_xor(input_bytes, XOR_KEY)

def encrypt_xor(input_bytes, key):
    if input_bytes is None or key is None:
        raise ValueError("Input bytes or key cannot be None.")
    
    encrypted_bytes = bytearray(len(input_bytes))
    for i in range(len(input_bytes)):
        encrypted_bytes[i] = input_bytes[i] ^ key[i % len(key)]
    
    return bytes(encrypted_bytes)


def xor_cipher(input_bytes, key):
    """
    对输入的字节串应用XOR操作，使用给定的密钥。
    密钥会循环使用以匹配输入的长度。
    
    :param input_bytes: 原始字节串
    :param key: XOR操作使用的密钥字节串
    :return: 经过XOR操作后的字节串
    """
    if input_bytes is None or key is None:
        raise ValueError("Input and key cannot be None")
    
    key_length = len(key)
    return bytes(b ^ key[i % key_length] for i, b in enumerate(input_bytes))

# 示例使用
# obj = {"data": "example data"}
# encrypted = serialize_to_byte(obj)
# print("Encrypted:", encrypted)
# obj_restored = deserialize_from_byte(encrypted)
# print("Restored Object:", obj_restored)