import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from main.sender.sender import pipe_snd_open, pipe_write, pipe_snd_close
import time

def main():
    print("Sender starting...")
    snd_id = pipe_snd_open()

    print(f"Sender ready with id={snd_id}")

    msg = b"Hello receiver!" * 10
    print(f"Sending {len(msg)} bytes...")
    pipe_write(snd_id, msg)

    time.sleep(1)
    pipe_snd_close(snd_id)
    print("\nSender closed.")

if __name__ == "__main__":
    main()