import os

root_dir = ".\static\img"

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".jpg"):
            file_path = os.path.join(subdir, file)
            print(file_path)
            # do something with the file_path
