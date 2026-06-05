"""
main.py  —  Run all scheduling algorithms and compare results
=============================================================
Usage
-----
    python main.py                        # small dataset only
    python main.py --large                # small + large dataset
    python main.py --dataset data/small_dataset.csv

Outputs a side-by-side comparison table:
    Algorithm | ΣCj | Avg Wait | Total Tardiness | Tardy Jobs | Makespan | Runtime
"""

import sys
import os

# Make sure sibling 'algorithms/' directory is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "algorithms"))

import fifo as FIFO
import spt  as SPT
import edd  as EDD
import wspt as WSPT


ALGORITHMS = [
    ("FIFO",  FIFO),
    ("SPT",   SPT),
    ("EDD",   EDD),
    ("WSPT",  WSPT),
]


def run_all(filepath: str) -> list[dict]:
    rows = []
    for name, module in ALGORITHMS:
        results, m, runtime = module.run(filepath)
        rows.append({
            "algorithm"      : name,
            "total_Cj"       : m["total_Cj"],
            "avg_waiting"    : m["avg_waiting_time"],
            "total_tardiness": m["total_tardiness"],
            "tardy_jobs"     : m["tardy_jobs"],
            "makespan"       : m["makespan"],
            "runtime_ms"     : runtime,
        })
    return rows


def print_table(rows: list[dict], title: str):
    W = 90
    print(f"\n{'='*W}")
    print(f"  {title}")
    print(f"{'='*W}")
    fmt = f"  {{:<8}} {{:>10}} {{:>12}} {{:>18}} {{:>12}} {{:>10}} {{:>12}}"
    print(fmt.format(
        "Algorithm", "ΣCj", "Avg Wait", "Total Tardiness",
        "Tardy Jobs", "Makespan", "Runtime (ms)"
    ))
    print(f"  {'-'*86}")

    best_cj   = min(r["total_Cj"]        for r in rows)
    best_tard = min(r["total_tardiness"]  for r in rows)
    best_rt   = min(r["runtime_ms"]       for r in rows)

    for r in rows:
        star_cj   = " ★" if r["total_Cj"]       == best_cj   else "  "
        star_tard = " ★" if r["total_tardiness"] == best_tard else "  "
        star_rt   = " ★" if r["runtime_ms"]      == best_rt   else "  "
        print(fmt.format(
            r["algorithm"],
            f"{r['total_Cj']}{star_cj}",
            f"{r['avg_waiting']:.2f}",
            f"{r['total_tardiness']}{star_tard}",
            r["tardy_jobs"],
            r["makespan"],
            f"{r['runtime_ms']:.4f}{star_rt}",
        ))

    print(f"\n  ★ = best in column")
    print(f"{'='*W}\n")


def main():
    run_large = "--large" in sys.argv

    # Determine dataset path
    custom = next((a for a in sys.argv[1:] if a.startswith("--dataset")), None)
    if custom:
        small_path = custom.split("=")[-1]
        large_path = None
    else:
        base = os.path.dirname(__file__)
        small_path = os.path.join(base, "data", "small_dataset.csv")
        large_path = os.path.join(base, "data", "large_dataset.csv")

    if not os.path.exists(small_path):
        print(f"[ERROR] Small dataset not found: {small_path}")
        sys.exit(1)

    # ── Small dataset ──
    print(f"\nLoading small dataset: {small_path}")
    small_rows = run_all(small_path)
    print_table(small_rows, "Small Dataset  —  Algorithm Comparison")

    # ── Large dataset ──
    if run_large and large_path:
        if not os.path.exists(large_path):
            print(f"[ERROR] Large dataset not found: {large_path}")
        else:
            print(f"Loading large dataset: {large_path}")
            large_rows = run_all(large_path)
            print_table(large_rows, "Large Dataset  —  Algorithm Comparison")

            # Runtime scalability
            W = 70
            print(f"{'='*W}")
            print(f"  Runtime Scalability  (Small → Large)")
            print(f"{'='*W}")
            fmt2 = f"  {{:<8}} {{:>16}} {{:>16}} {{:>14}}"
            print(fmt2.format("Algorithm","Small (ms)","Large (ms)","Ratio"))
            print(f"  {'-'*58}")
            for s, l in zip(small_rows, large_rows):
                ratio = f"{l['runtime_ms']/s['runtime_ms']:.1f}x" if s["runtime_ms"] > 0 else "—"
                print(fmt2.format(s["algorithm"], s["runtime_ms"], l["runtime_ms"], ratio))
            print(f"{'='*W}\n")


if __name__ == "__main__":
    main()
