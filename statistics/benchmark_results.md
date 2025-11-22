# PIPE PERFORMANCE BENCHMARK

Below are the results of the pipe implementation, sending/receiving a 512B block for different values of N. Each test was repeated 3 times.

---

## N = 10 (3 repetitions)

| Run | Status |
|-----|--------|
| 1   | OK     |
| 2   | OK     |
| 3   | OK     |

**Statistics:**

| Metric                 | Min       | Avg       | Max       |
|------------------------|-----------|-----------|-----------|
| Time (sec)             | 0.092053  | 0.092233  | 0.092437  |
| Retransmissions        | 0         | 0         | 0         |
| Duplicates             | 10        | 10        | 10        |
| Dropped (buffer full)  | 0         | 0         | 0         |
| Flow-control waits     | 0         | 0         | 0         |

---

## N = 100 (3 repetitions)

| Run | Status |
|-----|--------|
| 1   | OK     |
| 2   | OK     |
| 3   | OK     |

**Statistics:**

| Metric                 | Min       | Avg       | Max       |
|------------------------|-----------|-----------|-----------|
| Time (sec)             | 1.015526  | 1.021414  | 1.029916  |
| Retransmissions        | 15        | 25.333    | 38        |
| Duplicates             | 115       | 125.333   | 138       |
| Dropped (buffer full)  | 0         | 0         | 0         |
| Flow-control waits     | 0         | 0         | 0         |

---

## N = 1000 (3 repetitions)

| Run | Status |
|-----|--------|
| 1   | OK     |
| 2   | OK     |
| 3   | OK     |

**Statistics:**

| Metric                 | Min        | Avg        | Max        |
|------------------------|------------|------------|------------|
| Time (sec)             | 10.229888  | 10.285102  | 10.339065  |
| Retransmissions        | 139        | 232.333    | 322        |
| Duplicates             | 1139       | 1232.333   | 1322       |
| Dropped (buffer full)  | 0          | 0          | 0          |
| Flow-control waits     | 0          | 0          | 0          |

---

## N = 10000 (3 repetitions)

| Run | Status |
|-----|--------|
| 1   | OK     |
| 2   | OK     |
| 3   | OK     |

**Statistics:**

| Metric                 | Min        | Avg        | Max        |
|------------------------|------------|------------|------------|
| Time (sec)             | 101.851594 | 102.494714 | 103.355460 |
| Retransmissions        | 586        | 1590.667   | 2913       |
| Duplicates             | 10586      | 11590.667  | 12913      |
| Dropped (buffer full)  | 0          | 0          | 0          |
| Flow-control waits     | 0          | 0          | 0          |

---

**Conclusions:**

- Time increases almost linearly with N, as expected.  
- Retransmissions and duplicates occur, especially for large N, due to sender retransmissions and duplicate packets.  
- No packets were dropped due to full buffers.  
- Flow-control was not triggered, indicating that the buffers were large enough for the current tests.