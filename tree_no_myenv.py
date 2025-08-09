# tree_no_myenv.py
import os

def print_tree(root, indent=""):
    for name in sorted(os.listdir(root)):
        if name in {'myenv', '__pycache__'}:
            continue
        path = os.path.join(root, name)
        print(indent + "├── " + name)
        if os.path.isdir(path):
            print_tree(path, indent + "│   ")

print_tree(".")
