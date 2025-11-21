import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pipe.sender as sender
import time

# Open sender
sender_id = sender.pipe_snd_open()
print(f"Sender opened with ID {sender_id}")

messages = ["Hello", "this is", "a test", "message over UDP"]

for msg in messages:
    sender.pipe_write(sender_id, msg.encode())
    print(f"Sent: {msg}")
    time.sleep(0.5)

# Wait for all messages to be sent
sender.pipe_flush(sender_id)

# Close sender
sender.pipe_snd_close(sender_id)
print("Sender closed")
