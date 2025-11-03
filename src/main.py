import threading
import time
import udp.server as server
import udp.client as client

t1 = threading.Thread(target=server.init, daemon=True)
t1.start()

time.sleep(1)
client.init()