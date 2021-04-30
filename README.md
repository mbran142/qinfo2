# Qinfo2

Basic command-line data-snippet manager. Stored files are encrypted using AES file encryption with sha256-generated keys from a password.

## Getting started

To start a new filesystem, run `src/main.py` with the command line arguments `-n` and `<dir_name>` (i.e., choose a directory name for a new, empty filesystem). You will be prompted for to provide a password for the new filesystem.

## Authentication

To enter the filesystem, run `src/main.py` with the command line argument `<dir_name>` (or simply provide the directory name at runtime). Next, enter your password.

## Using the filesystem

Once you have created a filesystem, you can use the following commands to insert, view, and delete entries:

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

Note the '_' in some commands implies a second argument is required.