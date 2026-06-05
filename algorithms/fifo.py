"""
FIFO (First-In First-Out) Scheduling
=====================================
Dispatching Rule : Process jobs in order of earliest arrival_time.
                   Ties broken by job_id.
Objective        : Minimize Total Completion Time  ΣCj
Data Structure   : Queue  (sorted list, processed front-to-back)
Time Complexity  : O(n log n)  — one-time sort by arrival_time
Space Complexity : O(n)
"""

import csv
import time


# ──────────────────────────────────────────────
# Core Algorithm
# ──────────────────────────────────────────────

def fifo(jobs: list[dict]) -> list[dict]:
    """
    Run FIFO scheduling on a list of jobs.

    Parameters
    ----------
    jobs : list of dict
        Each dict must have keys:
            job_id, processing_time (p), arrival_time (r), due_date (d),
            priority_weight (w), pw_ratio

    Returns
    -------
    list of dict
        Scheduled results with added fields:
            seq, start_time, completion_time,
            waiting_time, flow_time, tardiness
    """
    # Sort by arrival_time (FIFO queue order); tie-break by job_id
    queue = sorted(jobs, key=lambda j: (j["arrival_time"], j["job_id"]))

    current_time = 0
    results = []

    for seq, job in enumerate(queue, start=1):
        start = max(current_time, job["arrival_time"])
        end   = start + job["processing_time"]
        current_time = end

        results.append({
            "seq"             : seq,
            "job_id"          : job["job_id"],
            "product"         : job["product"],
            "operation_type"  : job["operation_type"],
            "processing_time" : job["processing_time"],
            "arrival_time"    : job["arrival_time"],
            "due_date"        : job["due_date"],
            "priority_weight" : job["priority_weight"],
            "pw_ratio"        : job["pw_ratio"],
            "start_time"      : start,
            "completion_time" : end,
            "waiting_time"    : start - job["arrival_time"],
            "flow_time"       : end   - job["arrival_time"],
            "tardiness"       : max(0, end - job["due_date"]),
        })

    return results


# ──────────────────────────────────────────────
# Metrics Helper
# ──────────────────────────────────────────────

def compute_metrics(results: list[dict]) -> dict:
    n = len(results)
    return {
        "algorithm"       : "FIFO",
        "n_jobs"          : n,
        "total_Cj"        : sum(r["completion_time"] for r in results),
        "avg_waiting_time": round(sum(r["waiting_time"] for r in results) / n, 2),
        "total_tardiness" : sum(r["tardiness"] for r in results),
        "tardy_jobs"      : sum(1 for r in results if r["tardiness"] > 0),
        "makespan"        : max(r["completion_time"] for r in results),
    }


# ──────────────────────────────────────────────
# Runner (loads CSV → runs → prints summary)
# ──────────────────────────────────────────────

def run(filepath: str) -> tuple[list[dict], dict, float]:
    """
    Load a CSV dataset, execute FIFO, and return results.

    Returns
    -------
    results  : scheduled job list
    metrics  : summary metrics dict
    runtime  : elapsed time in milliseconds
    """
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        jobs = []
        for row in reader:
            jobs.append({
                "job_id"          : row["job_id"],
                "product"         : row["product"],
                "operation_type"  : row["operation_type"],
                "processing_time" : int(row["processing_time"]),
                "arrival_time"    : int(row["arrival_time"]),
                "due_date"        : int(row["due_date"]),
                "priority_weight" : int(row["priority_weight"]),
                "pw_ratio"        : float(row["pw_ratio"]),
            })

    t0 = time.perf_counter()
    results = fifo(jobs)
    runtime = (time.perf_counter() - t0) * 1000  # ms

    m = compute_metrics(results)
    return results, m, round(runtime, 4)


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import sys, os

    dataset = sys.argv[1] if len(sys.argv) > 1 else "../data/small_dataset.csv"

    if not os.path.exists(dataset):
        print(f"[ERROR] File not found: {dataset}")
        sys.exit(1)

    results, m, runtime = run(dataset)

    print(f"\n{'='*50}")
    print(f"  FIFO Scheduling Results")
    print(f"  Dataset : {dataset}")
    print(f"{'='*50}")
    print(f"  {'#':<4} {'Job ID':<8} {'Start':>7} {'Cj':>7} "
          f"{'Wait':>6} {'Tard':>6}")
    print(f"  {'-'*44}")
    for r in results:
        print(f"  {r['seq']:<4} {r['job_id']:<8} "
              f"{r['start_time']:>7} {r['completion_time']:>7} "
              f"{r['waiting_time']:>6} {r['tardiness']:>6}")
    print(f"\n  Total Completion Time  ΣCj : {m['total_Cj']}")
    print(f"  Avg Waiting Time           : {m['avg_waiting_time']}")
    print(f"  Total Tardiness            : {m['total_tardiness']}")
    print(f"  Tardy Jobs                 : {m['tardy_jobs']}")
    print(f"  Makespan                   : {m['makespan']}")
    print(f"  Runtime                    : {runtime} ms")
    print(f"{'='*50}\n")
