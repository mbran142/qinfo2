# add imports

def encrypt_file(filename, key):
    """
    Encrypts a file given a key.

    Arguments:
    filename -- string containing file (including path) to encrypt
    key -- plaintext key used used to generate a sha256 key for (symmetric) encryption of file

    Returns: None
    """
    pass


def encrypt_filesystem(dirname, key):
    """
    Decrypts a filesystem given a key.

    Arguments:
    dirname -- string containing directory (including path) to decrypt.
    key -- plaintext key used used to generate a sha256 key for (symmetric) decryption of file

    Returns: None
    """
    pass


def decrypt_file(filename, key):
    """
    Decrypts a file given a key.

    Arguments:
    filename -- string containing file (including path) to decrypt
    key -- plaintext key used used to generate a sha256 key for (symmetric) decryption of file

    Returns: Decrypted bytes of file given key. Does not check ascii validity
    """
    pass


def decrypt_filesystem(dirname, key):
    """
    Decrypts a filesystem given a key.

    Arguments:
    dirname -- string containing directory (including path) to decrypt.
    key -- plaintext key used used to generate a sha256 key for (symmetric) decryption of file

    Returns: JSON object containing filesystem information
    """
    pass


def change_password(new_pass):
    """
    Changes the master password of the filesystem.

    Arguments:
    new_pass -- New password for filesysyem

    Returns: None
    """
    pass