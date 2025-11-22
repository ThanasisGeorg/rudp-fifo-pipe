import sys
import os
import time
import statistics

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main.protocol import DATA_BLOCK
from main.sender.sender import pipe_snd_open, pipe_write, pipe_snd_close, senders
from main.receiver.receiver import pipe_rcv_open, pipe_read, pipe_rcv_close, receivers

ITERATIONS = [10, 100, 1000, 10000]
REPEATS = 3

def run_once(N):
    snd = pipe_snd_open()
    rcv = pipe_rcv_open()

    start = time.time()

    for _ in range(N):
        pipe_write(snd, DATA_BLOCK)
        pipe_read(rcv, len(DATA_BLOCK))

    pipe_snd_close(snd)
    pipe_rcv_close(rcv)

    end = time.time()
    elapsed = end - start

    s = senders.get(snd)
    r = receivers.get(rcv)

    result = {
        "time": elapsed,
        "retransmissions": getattr(s, "retransmissions", 0),
        "duplicates": getattr(r, "duplicate_drops", 0),
        "dropped_full": getattr(r, "full_buffer_drops", 0),
        "flow_waits": getattr(s, "flow_control_waits", 0)
    }

    # Cleanup
    senders.clear()
    receivers.clear()

    return result

def print_stats(label, values):
    nums = [v for v in values]
    print(f"{label}: min={min(nums):.6f}, avg={statistics.mean(nums):.6f}, max={max(nums):.6f}")

def main():
    print("=== PIPE PERFORMANCE BENCHMARK ===\n")

    for N in ITERATIONS:
        print(f"\n=======================")
        print(f"Running N = {N}, {REPEATS} times")
        print("=======================\n")

        times = []
        retrans = []
        duplicates = []
        dropped = []
        flow_waits = []
        
        for i in range(REPEATS):
            print(f"  Run {i+1}/{REPEATS} ... ", end="")
            result = run_once(N)
            print("OK")

            times.append(result["time"])
            retrans.append(result["retransmissions"])
            duplicates.append(result["duplicates"])
            dropped.append(result["dropped_full"])
            flow_waits.append(result["flow_waits"])

        print("\n--- Results for N =", N, "---")
        print_stats("Time (sec)", times)
        print_stats("Retransmissions", retrans)
        print_stats("Duplicates", duplicates)
        print_stats("Dropped (buffer full)", dropped)
        print_stats("Flow-control waits", flow_waits)
        print("--------------------------\n")

        # Cleanup
        senders.clear()
        receivers.clear()

if __name__ == "__main__":
    main()
