# several lines taken / motivated from Keith's answer from
# https://stackoverflow.com/questions/20852664/python-pycrypto-encrypt-decrypt-text-files-with-aes

import hmac
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from json import dumps, loads
from time import time
from base64 import b64encode

import pdb

def encrypt_file(filename, data, key):
    """
    Encrypts a file given a key.

    Arguments:
    filename -- string containing file (including path) to encrypt
    data -- file data (string)
    key -- plaintext key used used to generate a AES key for (symmetric) encryption of file

    Returns: None
    """
    data = pad(str.encode(data))    # convert data into padded bytes

    # get key
    digest = hmac.new(str.encode(key + filename), digestmod=hashlib.sha256).digest()

    # encrypt data
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(digest, AES.MODE_CBC, iv)
    enc = iv + cipher.encrypt(data)

    # save data
    with open(filename + '.qf2', 'wb') as f:
        f.write(enc)


def encrypt_filesystem(dirname, data, key):
    """
    Encrypts and saves a filesystem given a key.

    Arguments:
    dirname -- string containing the path of where to save the encrypted root.qf2 file.
    data -- filesystem json
    key -- plaintext key used used to generate a AES key for (symmetric) decryption of file

    Returns: None
    """
    data = ('\0' * 32) + dumps(data)
    encrypt_file(dirname + '/root', data, key)


def decrypt_file(filename, key):
    """
    Decrypts a file given a key.

    Arguments:
    filename -- string containing file (including path) to decrypt
    key -- plaintext key used used to generate a AES key for (symmetric) decryption of file

    Returns: Decrypted string of file given key. Returns None is decode fails
    """
    # load ciphertext
    with open(filename + '.qf2', 'rb') as f:
        ciphertext = f.read()

    # get key
    digest = hmac.new(str.encode(key + filename), digestmod=hashlib.sha256).digest()

    # decrypt file
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(digest, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])

    # return None is decode fails
    try:
        return bytes.decode(plaintext.rstrip(b"\0"))
    except Exception:
        return None


def decrypt_filesystem(dirname, key):
    """
    Decrypts a filesystem given a key.

    Arguments:
    dirname -- string containing directory (including path) to decrypt.
    key -- plaintext key used used to generate a AES key for (symmetric) decryption of file

    Returns: JSON object containing filesystem information
    """
    plaintext = decrypt_file(dirname + '/root', key)

    if plaintext is None or plaintext[:32] != '\0' * 32:
        return None

    return loads(plaintext[32:0])


def change_password(new_pass):
    """
    Changes the master password of the filesystem.

    Arguments:
    new_pass -- New password for filesysyem

    Returns: None
    """
    # TODO: implement this (add some confirmation process)
    pass


def pad(s):
    """Pads byte string with 0s"""
    return s + b'\0' * (AES.block_size - len(s) % AES.block_size)


def get_file_hash(filename):
    """
    Creates a hashed filename. Uses the current system time and filename.

    Arguments
    filename -- Name of file to get hash of

    Returns: 20 digits of base64 encoded hash, along with a '.qf2' file tag.
    """
    time_string = str(time()).encode('utf-8')
    dig = hashlib.sha1(time_string).digest()
    return bytes.decode(b64encode(dig)[:20]) + '.qf2'