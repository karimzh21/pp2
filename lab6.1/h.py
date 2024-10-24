import os

path = '/path/to/file_or_directory'

if os.path.exists(path):
    print("Path exists")
    print("Directory portion:", os.path.dirname(path))
    print("File name portion:", os.path.basename(path))
else:
    print("Path does not exist")
