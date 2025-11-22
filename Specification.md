# RUDP FIFO Pipe - Specification

## Project Overview

`RUDP FIFO pipe` is a Python project implementing a **reliable, FIFO-ordered data transfer protocol** on top of UDP. The project provides a **Sender** and **Receiver** abstraction, enabling users to transmit fixed-size data blocks reliably over an unreliable network.

The project simulates a simple **RUDP (Reliable UDP)** pipe with flow control, retransmissions, and duplicate packet handling.

## Goals / Objectives

- Implement a **reliable data transfer mechanism** over UDP.
- Ensure **FIFO ordering** of delivered data at the receiver.
- Implement **flow control** to avoid buffer overflows.
- Track and report **performance metrics**, including retransmissions and duplicate drops.
- Provide a **simple Python API** for sending and receiving data blocks.

## Functional Requirements

- **Sender**:
  - Open a pipe (`pipe_snd_open()`) and send data (`pipe_write()`).
  - Wait if buffer is full (flow control).
  - Track pending packets and retransmit if ACK not received within a timeout.
  - Close the pipe with `pipe_snd_close()` sending a FIN packet.

- **Receiver**:
  - Open a pipe (`pipe_rcv_open()`) and receive data (`pipe_read()`).
  - Store data in a buffer with FIFO order.
  - Drop duplicate packets and track drops.
  - Send ACKs for correctly received packets.
  - Handle FIN packets to terminate the connection gracefully.

- **Protocol**:
  - Packets include `seq`, `ack`, `flags`, and `payload`.
  - Flags:
    - `DATA` – data packet
    - `ACK` – acknowledgment
    - `FIN` – finalize transmission
  - Maximum payload per packet: 512 bytes.

## Non-functional Requirements

- **Buffer Sizes**: 25 × 1024B for sender and receiver.
- **Block Size**: 512B per data block.
- **Performance Metrics**:
  - Time to send/receive N blocks.
  - Number of retransmissions by sender.
  - Number of duplicate packets dropped by receiver.
  - Number of packets dropped due to buffer overflow.
  - Number of flow-control waits by sender.

- **Reliability**: Ensure no data is lost, delivered in order, and duplicates are discarded.

## Project structure

```
rudp-fifo-pipe/
├── src/
│   ├── main/
│   │   ├── __init__.py
│   │   ├── protocol.py
│   │   ├── receiver/
│   │   │   ├── receiver_main.py
│   │   │   └── receiver.py
│   │   └── sender/
│   │       ├── sender_main.py
│   │       └── sender.py
│   └── tests/
│       └── benchmark.py
├── statistics
│   └── benchmark_results.md
├── LICENSE
├── README.md
└── Specification.md
```

### Modules

- **protocol.py**: Defines packet structure, flags, constants, and test DATA_BLOCK.
- **sender.py**: Implements Sender class and API functions (`pipe_snd_open`, `pipe_write`, etc.).
- **receiver.py**: Implements Receiver class and API functions (`pipe_rcv_open`, `pipe_read`, etc.).
- **sender_main.py / receiver_main.py**: Example scripts to run sender or receiver standalone.
- **benchmark.py**: Script to measure performance and statistics for sending multiple data blocks.

## Data Protocol

- **Packet Structure**:
  - `seq` – sequence number of packet.
  - `ack` – acknowledgment number.
  - `flag` – packet type (`DATA`, `ACK`, `FIN`).
  - `payload` – raw data (≤512 bytes).
- **Transmission Logic**:
  - Sender sends DATA packets sequentially.
  - Receiver acknowledges each correctly received packet.
  - Retransmission occurs if ACK not received within `TIMEOUT`.
  - FIN signals end of transmission.

## API / Usage

### Sender API

```python
pipe_id = pipe_snd_open()
pipe_write(pipe_id, data)
pipe_flush(pipe_id)
pipe_snd_close(pipe_id)
```

### Receiver API

```python
pipe_id = pipe_rcv_open()
data = pipe_read(pipe_id, size)
pipe_rcv_close(pipe_id)
```

### Notes

- **pipe_write** blocks if the buffer is full (flow control)
- **pipe_read** blocks if no data is available
- All operations are thread-safe

## Limitations

- Communication is tested on localhost.
- UDP is used as the underlying transport; network loss can be simulated but is minimal on localhost.
- Block size fixed at 512B.
- Sender and receiver buffers fixed at 25 × 1024B.
- Single connection at a time (no multiplexing).
- No encryption or compression applied.
