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
    done = False
    modified = False
    list_dir = 1        # 0 = nothing printed, 1 = small print, 2 = entire print
    dir_stack = []
    cur_dir = filesystem

    print('Filesystem loaded. Enter \'help\' to see command list.')

    while not done:

        if list_dir:
            list_directory(cur_dir, list_dir)

        list_dir = 0
        error = ''
        
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

                # at root already
                if len(dir_stack) == 0:
                    error = 'Cannot go above root directory.'

                # success
                else:
                    list_dir = 1
                    cur_dir = dir_stack.pop()

            elif user_input[0] == 'down':

                # no second arg provided
                if len(user_input) == 1:
                    error = "'down' command requires second argument."

                # second arg not in current directory
                elif user_input[1] in cur_dir:
                    error = f"'{user_input[1]}' not found in current directory."

                # second arg is not directory
                elif not isinstance(cur_dir[user_input[1]], dict):
                    error = f"'{user_input[1]}' not a directory."

                # success
                else:
                    dir_stack.append(cur_dir)
                    cur_dir = cur_dir[user_input[1]]

            elif user_input[0] == 'list':
                # set print flag to detailed
                list_dir = 2

            elif user_input[0] == 'get':
                
                # check for valid 2nd arg
                if len(user_input) == 1:
                    error = "'get' command requires second argument."

                # check that 2nd arg exists in current directory
                elif user_input[1] not in cur_dir:
                    error = f"'{user_input[1]}' not found in current directory."

                # check that 2nd arg is not a directory itself
                elif isinstance(cur_dir[user_input[1]], dict):
                    error = f"'{user_input[1]}' is a directory (should be a file)."

                # check the file actually exists. Remove file from filesystem if this is the case
                elif not os.path.isfile(cur_dir[user_input[1]]):
                    error = f"No file corresponding to '{user_input[1]}'. This entry has been removed."
                    modified = True
                    del cur_dir[user_input[1]]

                # success
                else: 
                    print(f"Loading entry '{user_input[1]}'... ", end='')
                    file_data = decrypt_file(cur_dir[user_input[1]], password)

                    # use pandas.DataFrame to copy data to clipboard
                    df = DataFrame([file_data])            
                    df.to_clipboard(index=False,header=False)
                    print('success. Data copied to clipboard.')

            elif user_input[0] == 'newfile':
                
                # check for valid 2nd arg
                if len(user_input) == 1:
                    error = "'newfile' command required second argument."

                # check that this doesn't alrdy exist
                elif user_input[1] in cur_dir:
                    error = f"'{user_input[1]}' already exists in current directory."

                # success
                else:

                    # get user input
                    new_filename = user_input[1]
                    user_input = input('[R]aw input or [F]ile input? (Default raw) > ')

                    # raw input
                    if len(user_input) == 0 or user_input[0].strip() != 'F':

                        # get multiline user input
                        print('Enter file data. End input with \'!EOF\'')
                        lines = []
                        while True:
                            line = input()
                            if line != '!EOF':
                                lines.append(line)
                            else:
                                break
                        file_data = '\n'.join(lines)

                        # TODO: make this verification a loop (until either y/n is entered)

                        # verify entry
                        user_input = input(f'You entered:\n----\n{file_data}\n----\nAccept? [Y/n] >')
                
                        if len(user_input) > 0 and user_input[:1].lower() == 'n':
                            error = 'File canceled.'

                    # file input
                    else:

                        # TODO: ask for filename (and give specific directory where it should appear)

                        # look for expected file
                        new_filename = f'{location}/{new_filename}.qf2'
                        print(f"Looking for file '{new_filename}'...")
                        
                        if not os.path.isfile(new_filename):
                            error = 'Input file not found.'
                        else:
                            with open(new_filename, 'r') as f:
                                file_data = f.read()
                            os.remove(new_filename)
                    
                    # if everything is okay so far, continue
                    if error == '':

                        # insert encoded filename into filesystem
                        encoded_filename = get_file_hash(new_filename)

                        # in rare case of collision, rerun hash
                        while not os.path.isfile(encoded_filename):
                            sleep(0.0001)
                            print('Woah!')
                            encoded_filename = get_file_hash(new_filename)

                        cur_dir[new_filename] = encoded_filename

                        # build and encrypt file
                        encrypt_file(location + '/' + encoded_filename, file_data, password)
                        print(f"New file successfully created with encoding '{encoded_filename}'")

                        modified = True

            elif user_input[0] == 'newdir':

                # check for valid 2nd arg
                if len(user_input) == 1:
                    error = "'newdir' command required second argument."

                # check that this doesn't alrdy exist
                elif user_input[1] in cur_dir:
                    error = f"'{user_input[1]}' already exists in current directory."

                # success
                else:
                    cur_dir[user_input[1]] = {}
                    modified = True 

            elif user_input[0] == 'delfile':
                
                # check for valid 2nd arg
                if len(user_input) == 1:
                    error = "'delfile' command required second argument."

                # check that file exists in filesystem
                elif user_input[1] not in cur_dir:
                    error = f"'{user_input[1]}' not found in current directory."

                # make sure the entry is not a directory
                elif isinstance(cur_dir[user_input[1]], dict):
                    error = f"'{user_input[1]}' is a directory. Use 'deldir' command instead."

                # success
                else:

                    # make sure the corresponding file exists
                    if not os.path.isfile(location + '/' + cur_dir[user_input[1]]):
                        print(f"'{cur_dir[user_input[1]]}' does not exist, but the entry has been removed from the filesystem.")

                    else:
                        os.remove(location + '/' + cur_dir[user_input[1]])
                        print(f"'{cur_dir[user_input[1]]}' is deleted, and the filesystem has been updated.")

                    del cur_dir[user_input[1]]
                    modified = True

            elif user_input[0] == 'deldir':
                
                # check for valid 2nd arg
                if len(user_input) == 1:
                    error = "'deldir' command required second argument."

                # check that file exists in filesystem
                elif user_input[1] not in cur_dir:
                    error = f"'{user_input[1]}' not found in current directory."

                # make sure the entry is not a directory
                elif not isinstance(cur_dir[user_input[1]], dict):
                    error = f"'{user_input[1]}' is a file. Use 'delfile' command instead."

                # make sure directory is empty
                elif len(cur_dir[user_input[1]]) != 0:
                    error = f"'{user_input[1]}' is not an empty directory. Please remove its contents first."

                # success
                else:
                    del cur_dir[user_input[1]]
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
        if error != '':
            print(f'Error: {error}')


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