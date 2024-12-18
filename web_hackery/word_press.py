import contextlib
import os 
import queue
import requests 
import sys 
import threading 
import time 

FILTERED = ['.jpg', '.gif', '.png', '.css']
TARGET = ""
THREADS = 10 

answers = queue.Queue()
web_paths = queue.Queue()

def gather_paths():
    for root, _, files in os.walk("."):
        for fname in files:
            if os.path.splittext(fname) [1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith("."):
                path = path[1:]
            print(path)
            web_paths.put(path)
@contextlib.contextmanager
def chdir(path):
    """
    On enter, change directory to specified path.
    On exit, change directory back to original. 
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)
if __name__ == '__main__':
    with chdir("/home/lucid/Downloads/"):
        gather_paths()
    input("Press return to continue")
    
