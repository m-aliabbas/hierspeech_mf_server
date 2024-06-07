import sys
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add this directory to sys.path if it's not already there
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
