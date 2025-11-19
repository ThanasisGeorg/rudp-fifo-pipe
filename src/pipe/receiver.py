
import socket
import threading
from xmlrpc import server
import protocol

next_receiver_id = 1
receivers = {}

class Receiver:
    def __init__(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((protocol.LOCAL_HOST, protocol.LOCAL_PORT))
        self.buffer = bytearray()
        self.lock = threading.Lock()
        self.expect_seq = 0
        self.running = True
        self.data_available = threading.Condition(self.lock)

    def listen(self):
        while self.running:
            data, addr = self.socket.recvfrom(protocol.MAX_PACKET)
            
            seq , ack, flag, payload = protocol.unpack_packet(data)
            
            if flag == protocol.FLAG_DATA:
                # Check for expected sequence number
                if seq == self.expect_seq:
                    self.store_to_buffer(payload)
                    self.expect_seq += 1
                    
                # Send ACK
                ack_packet = protocol.pack_packet(0, self.expect_seq, protocol.FLAG_ACK, b"")
                self.socket.sendto(ack_packet, addr)
            elif flag == protocol.FLAG_FIN:
                self.running = False
                final_ack_packet = protocol.pack_packet(0, self.expect_seq, protocol.FLAG_ACK, b"")
                self.socket.sendto(final_ack_packet, addr)
                
                with self.data_available:
                    self.data_available.notify_all()
            elif flag == protocol.FLAG_ACK:
                pass            
            
    # Store payload to buffer
    def store_to_buffer(self, payload):
        with self.data_available:
            free_space = protocol.BUFFER_SIZE - len(self.buffer)
            if len(payload) > free_space:
                payload = payload[:free_space]
            self.buffer.extend(payload)
            self.data_available.notify()
            
def pipe_rcv_open():
    global next_receiver_id
    
    r = Receiver(protocol.LOCAL_HOST, protocol.LOCAL_PORT, protocol.BUFFER_SIZE)
    
    t = threading.Thread(target=r.listen, daemon=True)
    t.start()
    
    receivers[next_receiver_id] = r
    next_receiver_id += 1
    
    return

def pipe_read(pipe_id, size):
    r = receivers.get(pipe_id)
    if r is None:
        return b""
    
    with r.data_available:
        if len(r.buffer) == 0:
            if r.closed or not r.running:
                return b""
            r.data_available.wait()
            
        if len(r.buffer) == 0:
            return b""

        read_size = min(size, len(r.buffer))
        data = r.buffer[:read_size]
        
        del r.buffer[:read_size]
    return bytes(data)

def pipe_rcv_close(pipe_id):
    r = receivers.get(pipe_id)
    if r is None:
        return
    
    # Stop the thread
    r.running = False
    
    # Close the socket
    r.socket.close()
    
    # Remove from receivers
    del receivers[pipe_id]
    
    return