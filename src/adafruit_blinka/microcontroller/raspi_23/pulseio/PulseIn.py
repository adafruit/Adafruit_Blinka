import array
import time
import subprocess
import os, signal
import traceback
import signal
import sysv_ipc
import atexit
import random

DEBUG = False
queues = []
procs = []

# The message queues live outside of python space, and must be formally cleaned!
def final():
    if DEBUG:
        print("Cleaning up message queues", queues)
        print("Cleaning up processes", procs)
    for q in queues:
        q.remove()
    for proc in procs:
        proc.terminate()
atexit.register(final)

class PulseIn:
    def __init__(self, pin, maxlen=2, idle_state=False):
        self._pin = pin
        self._maxlen = maxlen
        self._idle_state = idle_state
        self._queue_key = random.randint(1, 9999)
        try:
            self._mq = sysv_ipc.MessageQueue(None, flags=sysv_ipc.IPC_CREX)
            if DEBUG:
                print("Message Queue Key: ", self._mq.key)
            queues.append(self._mq)
        except sysv_ipc.ExistentialError:
            raise RuntimeError("Message queue creation failed")

        cmd = ["/home/pi/libgpiod_pulsein/src/libgpiod_pulsein",
               "--pulses", str(maxlen),
               "--queue", str(self._mq.key)]
        if not idle_state:
            cmd.append("-i")
        cmd.append("gpiochip0")
        cmd.append(str(pin))
        if DEBUG:
            print(cmd)
        
        self._process = subprocess.Popen(cmd)
        procs.append(self._process)

        # wait for it to start up
        if DEBUG:
            print("Waiting for startup success message from subprocess")
        message = self._mq.receive(type=2)
        if message[0] != b'!':
            raise RuntimeError("Could not establish message queue with subprocess")


    def deinit(self):
        # Clean up after ourselves
        self._process.terminate()
        procs.remove(self._process)
        self._mq.remove()
        queues.remove(self._mq)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.deinit()

    def resume(self, trigger_duration=0):
        if trigger_duration != 0:
            self._mq.send("t%d" % trigger_duration, True, type=1)
        else:
            self._mq.send("r", True, type=1)

    def pause(self):
        self._mq.send("p", True, type=1)

    def clear(self):
        self._mq.send("c", True, type=1)

    def popleft(self):
        self._mq.send("^", True, type=1)
        message = self._mq.receive(type=2)
        reply = int(message[0].decode('utf-8'))
        if reply == -1:
            reply = None
        return reply

    def __len__(self):
        self._mq.send("l", True, type=1)
        message = self._mq.receive(type=2)
        return int(message[0].decode('utf-8'))
