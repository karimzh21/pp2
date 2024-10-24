import os

path = '/path/to/directory'

# List only directories
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
print("Directories:", directories)

# List only files
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
print("Files:", files)

# List all directories and files
all_items = os.listdir(path)
print("All items:", all_items)
