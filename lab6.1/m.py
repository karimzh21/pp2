import os

path = '/path/to/file_to_delete'

if os.path.exists(path):
    if os.access(path, os.W_OK):
        os.remove(path)
        print(f"File {path} has been deleted.")
    else:
        print(f"No write permission for {path}.")
else:
    print(f"File {path} does not exist.")
