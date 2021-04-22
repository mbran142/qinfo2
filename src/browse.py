# add imports

# add some global JSON object here
# also some stack to keep track of directory location

def main_user_loop(filesystem):
    """
    Main user interface loop. Commands are:
    - up:        Go up one directory layer (i.e., 'cd ..')
    - down _:    Enter selected directory
    - list:      Show contents of current directory
    - get _:     Decrypt and print selected file (no qf2 tag needed)
    - newfile _: Create new file with selected name
    - newdir _:  Create new directory with selected name
    - help:      Show these commands

    Arguments:
    filesystem -- JSON object containing filesystem info

    Returns: None
    """
    pass


def process_user_input(input):
    """
    Converts user input into a command.
    
    Arguments:
    input -- user input to be converted

    Returns: Processed user input. Empty string if invalid.
    """
    pass


def list_directory(dir):
    """
    Prints the contents of the current given directory JSON object

    Arguments:
    dir -- JSON directory object

    Returns: None
    """
    pass


def display_file(filename):
    """
    Prints the contents of selected encrypted file.

    Arguments: filename:
    filename -- name of file (with or without .qf2 extension)

    Returns: True if file was found and decrypted, otherwise False
    """
    pass


def create_new_file(filename):
    """
    Creates new file. Can use either file or command line input.

    Arguments:
    filename -- name of the new file (string)

    Returns: True or False depending on whether a file was created or not
    """
    # -> check if the file already exists
    # -> if yes, print an error and return false
    # -> append '.qf2' to filename if not already added
    # -> ask if user wants to convert an existing file or use command line input
    #   -> if an existing file, convert the file (replace the existing file
    #   -> else, use user input (end input on some DONE string or something)
    #   -> ask user if their input is okay
    #       -> if not, redo
    # -> use encrypt_file(filename, global_password + filename) to save file
    # return true
    pass


def create_new_directory(dirname):
    """
    Create new directory in the current directory.

    Arguments:
    dirname -- name of new directory (string)

    Returns: True or False depending on whether the directory was created
    """
    # if the directory exists, return false
    pass


def print_help():
    """Prints each available command and what they do"""
    pass