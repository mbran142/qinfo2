import sys
import os

last_password = ''

def main():

    # TODO: make it so if no arguments are provided, the program asks for a directory
    # The selected directory (either my program input or command line) should have a 
    # 'root.qi2' file

    # check that valid directory is given
    if len(sys.argv) != 2:
        print('Error: One argument required (name of data directory).')
        exit(1)

    elif not os.path.isdir(f'data/{sys.argv[1]}'):
        print(f'Error: `data/{sys.argv[1]}` not valid directory')
        exit(1)

    # auth

    # control flow:
    # -> if no args provided, ask for one
    # -> make sure the directory provided exists and contains a `root.qi2` file
    #       -> if not, exit
    # -> ask for password (use link below). 3 second delay per failed attempt.
    # -> decrypt filesystem
    # -> call main ui loop
    # other:
    # use: https://stackoverflow.com/questions/9202224/getting-command-line-password-input-in-python


if __name__ == '__main__':
    main()