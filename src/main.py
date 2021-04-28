import sys
import os
from time import sleep
import json
from getpass import getpass
from security import decrypt_filesystem, encrypt_filesystem
from browse import main_user_loop


def create_new_filesystem(dirname, password):
    '''Creates a new filesystem. Returns False if an error occurs.'''

    # check if directory already exists.
    if (os.path.isdir(f'data/{dirname}')):
        return False

    # create directory and save empty filesystem into it
    os.mkdir(f'data/{dirname}')
    encrypt_filesystem(f'data/{dirname}', json.dumps({}), password)
    return True


def main():
    '''Entry point of program. Handles authentication and directs control flow elsewhere.'''

    # check if '-n' argument is provided, if yes create new filesystem directory
    if len(sys.argv) == 3 and sys.argv[1] == '-n':

        print('Building new filesystem in directory `data/' + sys.argv[2] + '`')

        # get password
        new_pass = getpass('Enter new filesystem password: ')
        confirm_pass = getpass('Confirm password: ')

        if new_pass != confirm_pass:
            print('Error: Passowrds do not match. The program will now exit.')
            exit(1)

        # attempt to create directory
        print('Attempting to build `data/' + sys.argv[2] + '`... ', end='')

        if create_new_filesystem(sys.argv[2], new_pass):
            print('success. Relaunch program to populate filesystem.')
            exit(0)
        else:
            print(f'failure. Directory `data/{sys.argv[2]}` already exists.')
            exit(1)

    # if not arg provided, get input from user
    if len(sys.argv) < 2:
        sel_dir = input("Select directory: ")
    else:
        sel_dir = sys.argv[1].strip('/')

    # check given directory is exists and has 'root.qf2' file
    if not os.path.isdir(f'data/{sel_dir}'):
        print(f'Error: `data/{sel_dir}` not valid directory')
        exit(1)
    elif not os.path.isfile(f'data/{sel_dir}/root.qf2'):
        print(f'Error: `data/{sel_dir}` does not contain `root.qf2` file')
        exit(1)

    # auth loop
    attempts = 0
    while (attempts < 5):

        password = getpass('Enter password: ')
        filesystem = decrypt_filesystem('data/' + sel_dir, password)

        if filesystem is None:
            sleep(3)
            attempts += 1
            print('Incorrect.')
        else:
            break

    # enter main ui loop if pass is correct
    if attempts != 5:
        main_user_loop('data/' + sel_dir, filesystem, password)
    else:
        print('Too many incorrect entries. The program will now exit.')
        exit(1)


if __name__ == '__main__':
    main()