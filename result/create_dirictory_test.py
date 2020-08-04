import os

# Directory name
directory = "1"

# Parent Directory path
parent_dir = "/result"

# join path ???
path = os.path.join(parent_dir, directory)

os.mkdir(path)
