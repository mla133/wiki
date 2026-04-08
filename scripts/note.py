import os
import datetime
import sys

# Set the directory path and file name
dir_path = os.path.expanduser('~/wiki')
file_name = 'inbox.md'

# Create the directory if it doesn't exist
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

def append_to_file(args):
    with open(os.path.join(dir_path, file_name), 'a') as f:
        print(f"# {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", file=f)
        for arg in args:
            if isinstance(arg, str):  # keep original argument input
                print(arg, file=f)

# Check if any command-line arguments were passed
if len(sys.argv) > 1:
    # Read from a file
    with open(sys.argv[1], 'r') as f:
        for line in f:
            append_to_file([line.strip()] + sys.argv[1:])
else:
    # Read from STDIN (default)
    args = []
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break
        args.append(line)
    append_to_file(args)

# Open the file in Notepad (equivalent to running `vim "+normal Go" +startinsert note.txt`)
os.startfile(os.path.join(dir_path, file_name))

