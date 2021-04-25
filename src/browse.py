import json
import re

# add some global JSON object here
# also some stack to keep track of directory location

# Rember:
# - double-check that directories and stuff (like root.qf2) exists before calling security.py functions
# - strip all '.qf2' tags from inputs to security.py functions

def main_user_loop(filesystem, password):
    """
    Main user interface loop. Commands are:
    - up:        Go up one directory layer (i.e., 'cd ..')
    - down _:    Enter selected directory
    - list:      Show contents of current directory
    - get _:     Decrypt and print selected file (no qf2 tag needed)
    - newfile _: Create new file with selected name
    - newdir _:  Create new directory with selected name
    - exit:      Exit porgram
    - help:      Show these commands

    Arguments:
    filesystem -- JSON object containing filesystem info

    Returns: None
    """
    done = False
    list_dir = True
    dir_stack = []
    cur_dir = filesystem

    while not done:

        if list_dir:
            list_directory(cur_dir)

        list_dir = False
        bad_input = False
        
        # requesting user input
        user_input = input('> ')

        # parse input
        user_input = user_input.split()

        if len(user_input) == 0:
            bad_input = True

        # find command
        elif user_input[0] == 'up':
            pass

        elif user_input[0] == 'down':
            pass

        elif user_input[0] == 'list':
            pass

        elif user_input[0] == 'get':
            pass

        elif user_input[0] == 'newfile':
            pass

        elif user_input[0] == 'newdir':
            pass

        elif user_input[0] == 'exit':
            pass

        elif user_input[0] == 'help':
            pass

        else:
            bad_input = True

        # print error if command not recognized
        if bad_input:
            print('Error: Command not recognized.')

    dec_json_str = json.dumps(cur_dir, indent=4)

    print(dec_json_str)


    # control flow
    # - print contents of wd
    # - print '>' to imply command input
    # - get command
    # - parse command
    # - map command to one of the above options, or print error

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
    # empty flag
    if len(dir) == 0:
        print('{{Empty}}')
        return

    # print contents
    for name, item in dir.items():
        
        if isinstance(item, dict):
            print(f'[{name}]')
        else:
            print(name)

    # TODO: make this printing more pretty.
    # - maybe add sizes of each dir.
    # - make the printing a grid system (check if i'm able to know console size)
    # - make the character limit ~20 for each thing printed. if this is exceeded, append '...' to the first 17 chars of the item
    # - if there are more than ~100 items in the directory, print the distribution of letters and ask for a starting letter or something
    #       - with this ^, entering in nothing will just print everything
    #       - add a 'summary = False' argument if I need to just print a summary of the dir based on the directory being
    #         automatically printed due to a directory change


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