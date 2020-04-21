import requests
import os
from playsound import playsound
import multiprocessing
from multiprocessing import Process
import time

stream_url = 'http://stream.rockradio.si:9034/;stream/1'


def capture_stream():
    r = requests.get(stream_url, stream=True)
    with open('stream.mp3', 'wb') as f:
        for block in r.iter_content(1024):
            f.write(block)

def main():
    Process(target = capture_stream).start()
    time.sleep(3)
    Process(playsound("stream.mp3", True)).start()
    # os.remove("stream.mp3")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()