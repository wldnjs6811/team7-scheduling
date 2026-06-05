# Team 7 — Single Machine Scheduling Algorithm Comparison

> **Course**: Data Structure and Algorithm  
> **Objective**: Minimize Total Completion Time (ΣCj) on a single machine  
> **Dataset**: Automotive Parts Manufacturing (synthetic data)

---

## Project Structure

```
team7-scheduling/
├── main.py                          # Run all algorithms + comparison table
├── data/
│   ├── small_dataset.csv            # 15 jobs — manually designed
│   └── large_dataset.csv            # 1,000 jobs — randomly generated
├── algorithms/
│   ├── fifo.py                      # First-In First-Out
│   ├── spt.py                       # Shortest Processing Time
│   ├── edd.py                       # Earliest Due Date
│   └── wspt.py                      # Weighted Shortest Processing Time
└── results/
    └── Team7_Scheduling_Final.xlsx  # Full result tables & comparison
```

---

## Algorithms

| Algorithm | Dispatching Rule | Data Structure | Time Complexity |
|-----------|-----------------|----------------|-----------------|
| **FIFO** | Earliest `arrival_time` first | Queue | O(n log n) |
| **SPT** | Shortest `processing_time` among available | Priority Queue | O(n²) |
| **EDD** | Earliest `due_date` among available | Priority Queue | O(n²) |
| **WSPT** | Smallest `p/w` ratio among available | Priority Queue | O(n²) |

> All algorithms handle **release times** (`arrival_time > 0`).  
> SPT / EDD / WSPT use a dispatch loop: at each step, only jobs that have arrived are eligible.

---

## Dataset Design

### Small Dataset (n = 15)
- Manually designed so each algorithm produces a **different job sequence**
- Non-monotonic: `processing_time`, `arrival_time`, `due_date`, `priority_weight` are intentionally mixed

### Large Dataset (n = 1,000)
- Randomly generated with the following constraints:
  - `processing_time` ∈ [5, 120]
  - `arrival_time` ∈ [0, 500]
  - `due_date = arrival_time + slack`,  slack ∈ [p, 3p + 100]  → always `due_date > arrival_time`
  - `priority_weight` ∈ [1, 5]

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/team7-scheduling.git
cd team7-scheduling
```

### 2. Run a single algorithm
```bash
# Run on small dataset (default)
python algorithms/fifo.py
python algorithms/spt.py
python algorithms/edd.py
python algorithms/wspt.py

# Run on large dataset
python algorithms/spt.py data/large_dataset.csv
```

### 3. Run all algorithms and compare
```bash
# Small dataset only
python main.py

# Small + Large dataset with runtime scalability
python main.py --large
```

### Example Output
```
==========================================================================================
  Small Dataset  —  Algorithm Comparison
==========================================================================================
  Algorithm        ΣCj     Avg Wait  Total Tardiness   Tardy Jobs    Makespan  Runtime (ms)
  --------------------------------------------------------------------------------------
  FIFO          2847          82.13              486            7         897     0.0421  
  SPT           2601 ★        71.40              412 ★          6         897     0.0312 ★
  EDD           2790          80.27              398 ★          5         897     0.0389  
  WSPT          2715          76.53              445            6         897     0.0401  

  ★ = best in column
```

---

## Key Findings

| Criterion | Best Algorithm | Reason |
|-----------|---------------|--------|
| Minimize ΣCj | **SPT** | Processes short jobs first → completions cluster early |
| Minimize Tardiness | **EDD** | Focuses on due-date proximity |
| Fastest Runtime | **FIFO** | Single sort O(n log n); no dispatch loop |
| Priority-aware | **WSPT** | Weights urgency via p/w ratio |

---

## References

- Pinedo, M. (2016). *Scheduling: Theory, Algorithms, and Systems* (5th ed.). Springer.  
- Baker, K. R., & Trietsch, D. (2009). *Principles of Sequencing and Scheduling*. Wiley.  
- Shakhlevich, N. (2007). *Handout 02 — Single Machine Scheduling*. University of Leeds.
