import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from main.receiver.receiver import pipe_rcv_close, pipe_rcv_open, pipe_read
import time

def main():
    print("Receiver starting...")
    rcv_id = pipe_rcv_open()

    print(f"Receiver ready with id={rcv_id}")
    print("Waiting for incoming data...\n")

    while True:
        data = pipe_read(rcv_id, 1024)
        if not data:
            time.sleep(0.1)
            continue
        print(f"Received {len(data)} bytes: {data[:50]} ...")
        break
    
    pipe_rcv_close(rcv_id)
    print("\nReceiver closed.")

if __name__ == "__main__":
    main()