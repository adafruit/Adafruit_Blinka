#!/usr/bin/python3
# Verified on Ubuntu with dependencies...
# pip3 install watchdog
# sudo apt install rsync
import time
import subprocess
from watchdog.observers import Observer

# the rsync command intended to selectively upload from the local repo to a feather m0 express
command = (
    'rsync '
    '--recursive --verbose --progress '
    '--prune-empty-dirs --inplace --times --archive --whole-file '
    # should already be built-in to circuitpython
    '--exclude="/board" '
    '--exclude="/digitalio" '
    '--exclude="/microcontroller" '
    # prefer unittest.mpy bytecode
    '--exclude="/unittest.py" '
    # should never be used by tests targeting feather m0
    '--exclude="mcp" '
    # don't upload upload https://www.youtube.com/watch?v=iEwW6D0sht0
    '--exclude="upload_*_watch.py" '
    # recurse in search
    '--include="*/" '
    # filter for python source files and micropython bytecode files
    '--include="*.py" '
    '--include="*.mpy" '
    # exclude everything else
    '--exclude="*" '
    # rsync from folder
    './ '
    # rsync to folder
    '/media/cefn/CIRCUITPY '
)

syncing = False

def sync():
    """Synchronizes from git repo to Feather filesystem"""
    global syncing
    syncing = True
    subprocess.run(command, shell=True)
    syncing = False

class ChangeEventHandler:
    """handler for future filesystem events"""
    def dispatch(self, event):
        if not syncing:
            sync()

if __name__ == "__main__":
    sync()
    handler=ChangeEventHandler() 
    
    # set up filesystem monitoring
    observer = Observer()
    observer.schedule(handler, ".", recursive=True)
    observer.start()
    
    # await CTRL+C
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    # join daemon thread to shutdown interpreter
    observer.join()
