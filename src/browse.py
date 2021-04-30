import json
from time import sleep
import os
from pandas import DataFrame    # for clipboard access
from security import decrypt_file, encrypt_file, encrypt_filesystem, get_file_hash

# add some global JSON object here
# also some stack to keep track of directory location

# Rember:
# - double-check that directories and stuff (like root.qf2) exists before calling security.py functions
# - strip all '.qf2' tags from inputs to security.py functions

dir_stack = []
cur_dir = None

def main_user_loop(location, filesystem, password):
    """
    Main user interface loop. Commands are:
    - up:        Go up one directory layer (i.e., 'cd ..')
    - down _:    Enter selected directory
    - list:      Show contents of current directory
    - get _:     Decrypt and copy selected file to clipboard (no qf2 tag needed)
    - newfile _: Create new file with selected name
    - newdir _:  Create new directory with selected name
    - delfile _: Delete a file entry along with the corresponding .qf2 file
    - deldir _:  Delete empty directory
    - exit:      Exit porgram
    - help:      Show these commands

    Arguments:
    location -- Directory name of the filesystem
    filesystem -- JSON object containing filesystem info
    password -- The successful password that decoded the filesystem

    Returns: None
    """
    global cur_dir
    global dir_stack

    done = False
    modified = False
    list_dir = 1        # 0 = nothing printed, 1 = small print, 2 = entire print
    cur_dir = filesystem

    print('Filesystem loaded. Enter \'help\' to see command list.')

    while not done:

        if list_dir:
            list_directory(cur_dir, list_dir)

        list_dir = 0
        error = None
        
        # requesting user input
        user_input = input('> ')

        # parse input
        user_input = user_input.split()

        if len(user_input) == 0:
            error = 'Command not recognized'
        else:
            # find command, evaluate errors case-by-case
            user_input[0] = user_input[0].lower()

            if user_input[0] == 'up':
                error = up_directory()
                list_dir = 1 if error is None else 0

            elif user_input[0] == 'down':
                error = down_directory(user_input)
                list_dir = 1 if error is None else 0

            elif user_input[0] == 'list':
                # set print flag to detailed
                list_dir = 2

            elif user_input[0] == 'get':
                error, temp_mod = file_to_clipboard(user_input, location, password)
                if temp_mod:
                    modified = True

            elif user_input[0] == 'newfile':
                error = create_new_file(user_input, location, password)
                if error is None:
                    modified = True

            elif user_input[0] == 'newdir':
                error = create_new_directory(user_input)
                if error is None:
                    modified = True

            elif user_input[0] == 'delfile':
                error = delete_file(user_input, location)
                if error is None:
                    modified = True

            elif user_input[0] == 'deldir':
                error = delete_directory(user_input)
                if error is None:
                    modified = True

            elif user_input[0] == 'exit':
                
                # save filesystem is necessary
                if modified:
                    print('Saving updated filesystem... ', end='')
                    encrypt_filesystem(location, filesystem, password)
                    print('success. The program will now exit.')

                done = True

            elif user_input[0] == 'help':
                print_help()

            else:
                error = 'Command not recognized'

        # print error if there is one
        if error is not None:
            print(f'Error: {error}')


def up_directory():
    """
    Go up one directory. Equivalent to 'cd ..'

    Returns: Error message if applicable, otherwise None
    """
    global cur_dir
    global dir_stack

    # at root already
    if len(dir_stack) == 0:
        return 'Cannot go above root directory.'

    # success
    cur_dir = dir_stack.pop()
    return None


def down_directory(user_input):
    """
    Enter the selected directory from the current one.

    Arguments
    user_input -- List of user provided arguments

    Returns: Error message if applicable, otherwise None
    """
    global cur_dir
    global dir_stack

    # no second arg provided
    if len(user_input) == 1:
        return "'down' command requires second argument."

    # second arg not in current directory
    if user_input[1] not in cur_dir:
        return f"'{user_input[1]}' not found in current directory."

    # second arg is not directory
    if not isinstance(cur_dir[user_input[1]], dict):
        return f"'{user_input[1]}' not a directory."

    # success
    dir_stack.append(cur_dir)
    cur_dir = cur_dir[user_input[1]]
    return None


def list_directory(dir, val):
    """
    Prints the contents of the current given directory JSON object

    Arguments:
    dir -- JSON directory object
    val -- 1 means summary, 2 means details

    Returns: None
    """
    # empty flag
    if len(dir) == 0:
        print('* EMPTY *')
        return

    # print contents
    for name, item in dir.items():
        
        if isinstance(item, dict):
            print(f' + [{name}]:[{len(item)}]')
        else:
            print(' - ' + name)

    # TODO: make this printing more pretty.
    # - maybe add sizes of each dir.
    # - make the printing a grid system (check if i'm able to know console size)
    # - make the character limit ~20 for each thing printed. if this is exceeded, append '...' to the first 17 chars of the item
    # - if there are more than ~100 items in the directory, print the distribution of letters and ask for a starting letter or something
    #       - with this ^, entering in nothing will just print everything
    #       - add a 'summary = False' argument if I need to just print a summary of the dir based on the directory being
    #         automatically printed due to a directory change
    # - also change the '{{Empty}}' to something better lol
    # - print contents in alphabetical order

def file_to_clipboard(user_input, location, password):
    """
    Copied a file entry to clipboard

    Arguments
    user_input -- List of user provided arguments

    Returns: Tuple of: (error message if applicable otherwise None, boolean whether filesystem has been modified
    """
    global cur_dir

    # check for valid 2nd arg
    if len(user_input) == 1:
        return ("'get' command requires second argument.", False)

    # check that 2nd arg exists in current directory
    if user_input[1] not in cur_dir:
        return (f"'{user_input[1]}' not found in current directory.", False)

    # check that 2nd arg is not a directory itself
    if isinstance(cur_dir[user_input[1]], dict):
        return (f"'{user_input[1]}' is a directory (should be a file).", False)

    # check the file actually exists. Remove file from filesystem if this is the case
    if not os.path.isfile(location + '/' + cur_dir[user_input[1]]):
        del cur_dir[user_input[1]]
        return (f"No file corresponding to '{user_input[1]}'. This entry has been removed.", True)

    # try and decrypt file
    print(f"Loading entry '{user_input[1]}'... ", end='')
    file_data = decrypt_file(location + '/' + cur_dir[user_input[1]][:-4], password)

    # error in decryption
    if file_data is None:
        print()
        return ('Decryption failed. File may be corrupted.', False)

    # use pandas.DataFrame to copy data to clipboard
    df = DataFrame([file_data])            
    df.to_clipboard(index=False,header=False)
    print('success. Data copied to clipboard.')
    return (None, False)


def create_new_file(user_input, location, password):
    """
    Create a new file entry in the filesystem along with a
    corresponding file entry.

    Arguments
    user_input -- User provided arguments
    location -- The directory where the filesystem is held
    password -- The password that successfully decrypted the filesystem

    Returns: Error message if applicable, otherwise None
    """
    global cur_dir

    # check for valid 2nd arg
    if len(user_input) == 1:
        return "'newfile' command required second argument."

    # check that this doesn't alrdy exist
    if user_input[1] in cur_dir:
        return f"'{user_input[1]}' already exists in current directory."

    # valid input so far; ask whether to use file input or raw input
    new_filename = user_input[1]
    user_input = input('[R]aw input or [F]ile input? (Default raw) > ')

    # raw input
    if len(user_input) == 0 or user_input[0].strip() != 'F':

        # get multiline user input
        print('Enter file data. End input with \'!EOF\' line')
        lines = []
        while True:
            line = input()
            if line != '!EOF':
                lines.append(line)
            else:
                break
        file_data = '\n'.join(lines)

        # TODO: make this verification a loop (until either y/n is entered)

        # check for empty entry
        if file_data == '':
            return 'File must contain at least one line.'

        # verify entry
        user_input = input(f'Verify entry [Y/n] > ')

        if len(user_input) > 0 and user_input[:1].lower() == 'n':
            return 'File canceled.'

    # file input
    else:

        # TODO: ask for filename (and give specific directory where it should appear)

        # look for expected file
        new_filepath = f'{location}/{new_filename}.qf2'
        print(f"Looking for file '{new_filepath}'...")
        
        if not os.path.isfile(new_filepath):
            return 'Input file not found.'
    
        print('File found. Encrypting file...')
        with open(new_filepath, 'r') as f:
            file_data = f.read()

        # check for empty file
        if file_data == '':
            return 'File must contain at least one line.'

        os.remove(new_filepath)
    
    # insert encoded filename into filesystem
    encoded_filename = get_file_hash(new_filename)

    # in rare case of collision, rerun hash
    while os.path.isfile(encoded_filename):
        sleep(0.0001)
        print('Woah!')
        encoded_filename = get_file_hash(new_filename)

    cur_dir[new_filename] = encoded_filename + '.qf2'

    # build and encrypt file
    encrypt_file(location + '/' + encoded_filename, file_data, password)
    print(f"New file successfully created with encoding '{encoded_filename}.qf2'")

    return None


def create_new_directory(user_input):
    """
    Create a new, empty directory in the current directory

    Arguments
    user_input -- User provided arguments

    Returns: Error if applicable, otherwise None
    """
    global cur_dir

    # check for valid 2nd arg
    if len(user_input) == 1:
        return "'newdir' command required second argument."

    # check that this doesn't alrdy exist
    if user_input[1] in cur_dir:
        return f"'{user_input[1]}' already exists in current directory."

    # success
    cur_dir[user_input[1]] = {}
    return None


def delete_file(user_input, location):
    """
    Deletes a file entry in the filesystem along with its corresponding storage file.

    Arguments:
    user_input -- User provided arguments
    location -- The directory where the filesystem is held

    Returns: Error if applicable, otherwise None
    """
    global cur_dir

    # check for valid 2nd arg
    if len(user_input) == 1:
        return "'delfile' command required second argument."

    # check that file exists in filesystem
    if user_input[1] not in cur_dir:
        return f"'{user_input[1]}' not found in current directory."

    # make sure the entry is not a directory
    if isinstance(cur_dir[user_input[1]], dict):
        return f"'{user_input[1]}' is a directory. Use 'deldir' command instead."

    # success; make sure the corresponding file exists
    if not os.path.isfile(location + '/' + cur_dir[user_input[1]]):
        print(f"'{cur_dir[user_input[1]]}' does not exist, but the entry has been removed from the filesystem.")

    else:
        os.remove(location + '/' + cur_dir[user_input[1]])
        print(f"'{cur_dir[user_input[1]]}' is deleted, and the filesystem has been updated.")

    del cur_dir[user_input[1]]
    return None


def delete_directory(user_input):
    """
    Deletes a directory in the filesystem

    Arguments:
    user_input -- User provided arguments

    Returns: Error if applicable, otherwise None
    """
    global cur_dir

    # check for valid 2nd arg
    if len(user_input) == 1:
        return "'deldir' command required second argument."

    # check that file exists in filesystem
    if user_input[1] not in cur_dir:
        return f"'{user_input[1]}' not found in current directory."

    # make sure the entry is not a directory
    if not isinstance(cur_dir[user_input[1]], dict):
        return f"'{user_input[1]}' is a file. Use 'delfile' command instead."

    # make sure directory is empty
    if len(cur_dir[user_input[1]]) != 0:
        return f"'{user_input[1]}' is not an empty directory. Please remove its contents first."

    # success
    print(f"Directory '{user_input[1]}' has been deleted.")
    del cur_dir[user_input[1]]
    
    return None


def print_help():
    """Prints each available command and what they do"""

    help_text = """Usable commands are:
    - up:        Go up one directory layer (i.e., 'cd ..')
    - down _:    Enter selected directory
    - list:      Show contents of current directory
    - get _:     Decrypt and copy selected file to clipboard (no qf2 tag needed)
    - newfile _: Create new file with selected name
    - newdir _:  Create new directory with selected name
    - delfile _: Delete a file entry along with the corresponding .qf2 file
    - deldir _:  Delete empty directory
    - exit:      Exit porgram
    - help:      Show these commands
    
    Underscores imply that a second user-provided argument is needed for the command.
    Commands are not case-sensitive."""
    
    print(help_text)