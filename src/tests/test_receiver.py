import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pipe.receiver as receiver

# Open receiver
receiver_id = receiver.pipe_rcv_open()
print(f"Receiver opened with ID {receiver_id}")

# Read data in a loop
try:
    while True:
        data = receiver.pipe_read(receiver_id, 1024)
        if not data:
            break
        print(f"Received: {data.decode()}")
finally:
    receiver.pipe_rcv_close(receiver_id)
    print("Receiver closed")
