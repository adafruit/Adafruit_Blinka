# dependencies
# pip3 install watchdog
import time
import subprocess
from watchdog.observers import Observer

command = 'rsync --prune-empty-dirs --include="*/" --include="*.py" --exclude="*" --recursive --whole-file --verbose --progress ./ /media/cefn/CIRCUITPY'

syncing = False;
def sync():
    syncing = True
    subprocess.run(command, shell=True)
    syncing = False

class ChangeEventHandler:
    def dispatch(self, event):
        if not syncing:
            sync()

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ChangeEventHandler(), ".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
