import threading
import socket
import time
from main import protocol

next_sender_id = 1
senders = {}

class Sender:
    def __init__(self, local_host, local_port, buffer_size):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind( (local_host, local_port) )
        
        self.buffer = bytearray()
        self.buffer_size = buffer_size
        
        self.lock = threading.Lock()
        self.data_available = threading.Condition(self.lock)
        self.space_available = threading.Condition(self.lock)
        
        self.pending_packet = None
        self.pending_seq = 0
        
        self.running = True
        
        self.sender_thread = threading.Thread(target=self.send, daemon=True)
        self.sender_thread.start()
        
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listen_thread.start()
        
        # Statistics
        self.retransmissions = 0
        self.flow_control_waits = 0

        
    # Write payload to buffer
    def write_to_buffer(self, payload):
        with self.data_available:
            i = 0
            while i < len(payload):
                while len(self.buffer) >= self.buffer_size:
                    self.space_available.wait()
                    self.flow_control_waits += 1
                self.buffer.append(payload[i])
                i += 1
            self.data_available.notify()
        
    def send(self):
        while self.running:
            with self.data_available:
                while len(self.buffer) == 0 and self.pending_packet is None and self.running:
                    self.data_available.wait()
                if not self.running:
                    break
            
                if self.pending_packet is None and len(self.buffer) > 0:
                    data = self.buffer[:protocol.MAX_PAYLOAD]
                    del self.buffer[:protocol.MAX_PAYLOAD]
                    
                    self.space_available.notify()
                
                packet = protocol.pack_packet(self.pending_seq, 0, protocol.FLAG_DATA, bytes(data))
                
                self.pending_packet = packet
                
                self.socket.sendto(packet, (protocol.LOCAL_HOST, protocol.LOCAL_PORT))
                
            time.sleep(protocol.TIMEOUT)
            
    def listen(self):
        self.socket.settimeout(protocol.TIMEOUT)
        while self.running:
            try:
                data, addr = self.socket.recvfrom(protocol.MAX_PACKET)
            except socket.timeout:
                if self.pending_packet is not None:
                    try:
                        self.socket.sendto(self.pending_packet, (protocol.LOCAL_HOST, protocol.LOCAL_PORT))
                        self.retransmissions += 1
                    except OSError:
                        # socket closed while sending
                        return
                continue
            except OSError:
                # socket closed
                return
            
            seq , ack, flag, payload = protocol.unpack_packet(data)
            if flag == protocol.FLAG_ACK:
                with self.data_available:
                    if self.pending_packet is not None and ack == self.pending_seq + 1:
                        self.pending_packet = None
                        self.pending_seq += 1
                        self.data_available.notify()     
            elif flag == protocol.FLAG_FIN:
                self.running = False
                return
    
    def flush(self):
        with self.data_available:
            while len(self.buffer) > 0 or self.pending_packet is not None:
                self.data_available.wait()
    
    def close(self):
        self.flush()
        fin = protocol.pack_packet(self.pending_seq, 0, protocol.FLAG_FIN, b"")
        try:
            self.socket.sendto(fin, (protocol.LOCAL_HOST, protocol.LOCAL_PORT))
        except OSError:
            # socket closed while sending FIN
            pass
        
        self.running = False
        self.socket.close()        
        
        with self.data_available:
            self.data_available.notify_all()

def pipe_snd_open():
    global next_sender_id
    
    s = Sender(protocol.LOCAL_HOST, protocol.LOCAL_PORT + 1, protocol.BUFFER_SIZE)
    
    pipe_id = next_sender_id
    senders[pipe_id] = s
    next_sender_id += 1
    
    return pipe_id

def pipe_write(pipe_id, data):
    s = senders.get(pipe_id)
    if s is None:
        return
    s.write_to_buffer(data) 
    
def pipe_flush(pipe_id):
    s = senders.get(pipe_id)
    if s is None:
        return
    s.flush()
    return

def pipe_snd_close(pipe_id):
    s = senders.get(pipe_id)
    if s is None:
        return
    s.close()
    # del senders[pipe_id]
    return