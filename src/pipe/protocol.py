import struct

MAX_PAYLOAD = 1024
BUFFER_SIZE = 25 * MAX_PAYLOAD

FLAG_DATA = 1
FLAG_ACK  = 2
FLAG_FIN  = 4

LOCAL_HOST = "192.168.1.4"
LOCAL_PORT = 20001

# Header format:
# SEQ  (4 bytes, unsigned int)
# ACK  (4 bytes, unsigned int)
# FLAG (1 byte)
# LEN  (2 bytes, unsigned short)
#
# Total header size = 11 bytes
HEADER_FORMAT = "!IIBH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

MAX_PACKET = MAX_PAYLOAD + HEADER_SIZE

# Packeting functions
def pack_packet(seq, ack, flag, payload: bytes):
    if len(payload) > MAX_PAYLOAD:
        raise ValueError("Payload too large")

    header = struct.pack(
        HEADER_FORMAT,
        seq,
        ack,
        flag,
        len(payload)
    )

    return header + payload

def unpack_packet(packet: bytes):
    if len(packet) < HEADER_SIZE:
        raise ValueError("Packet too small")

    header = packet[:HEADER_SIZE]
    payload = packet[HEADER_SIZE:]

    seq, ack, flag, length = struct.unpack(HEADER_FORMAT, header)

    if len(payload) != length:
        raise ValueError("Payload length mismatch")

    return seq, ack, flag, payload
