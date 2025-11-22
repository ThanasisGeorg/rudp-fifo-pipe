# RUDP FIFO Pipe

A **reliable UDP (RUDP) FIFO pipe** implementation in Python.  
This project provides a software-level reliable communication channel over UDP, using sequence numbers, acknowledgements (ACKs), retransmissions, and flow control, with a first-in-first-out (FIFO) buffer for sender and receiver.

## Features

- Reliable data transfer over UDP.
- Sender and receiver maintain internal buffers.
- Automatic retransmissions for lost packets.
- Flow control to prevent buffer overflow.
- Detection and dropping of duplicate packets.
- Blocking `write` and `read` operations respecting buffer capacity.
- Benchmarking scripts for performance evaluation.

## Project Structure

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
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ThanasisGeorg/rudp-fifo-pipe.git
cd rudp-fifo-pipe/
```

2. Ensure Python 3.8+ is installed.

## Usage

### Receiver

Initalize the receiver first:

```python
from pipe.receiver.receiver import pipe_rcv_open, pipe_read, pipe_rcv_close

receiver_id = pipe_rcv_open()
data = pipe_read(receiver_id, 512)
pipe_rcv_close(receiver_id)
```

### Sender

Then initialize the sender:

```python
from pipe.sender.sender import pipe_snd_open, pipe_write, pipe_snd_close

sender_id = pipe_snd_open()
pipe_write(sender_id, b"Hello World"*50)
pipe_snd_close(sender_id)
```

### Notes

1. Always start the receiver before the sender to avoid lost packets.
2. The sender and receiver buffers are configurable in protocol.py (default 25 KB).

## Test

1. Open a terminal.

2. Go to the root of the repo and run the following:

```bash
python3 src/main/receiver/receiver_main.py
```

3. Open a second terminal.

4. Go to the root of the repo and run the following:

```bash
cd rudp-fifo-pipe/
python3 src/main/sender/sender_main.py
```

## Benchmark

Run the following code to run the benchmark:

```bash
cd src/tests/
python3 benchmark.py
```

## License

MIT License. See <a href="https://github.com/ThanasisGeorg/rudp-fifo-pipe/blob/main/LICENSE">LICENSE</a> file for details.

## Author

<a href="https://github.com/ThanasisGeorg">ThanasisGeorg</a>
