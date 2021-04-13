import subprocess
import os
import pync
import time
import glob


container_name = "specify7_webpack_1"


def send_notification(message, title, sound="Pop"):
    pync.notify(message, title=title, group="specify7_notifications")
    run_process("afplay /System/Library/Sounds/%s.aiff" % sound)


def run_process(command):
    print(command)
    os.system(command)
