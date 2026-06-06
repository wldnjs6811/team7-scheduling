"""
Team 7 - Final Algorithm Comparison
Project: Single Machine Scheduling Algorithm Comparison
Context: Automotive Parts Manufacturing

Expected GitHub folder structure:

TEAM7-SCHEDULING/
├── algorithms/
│   ├── edd.py
│   ├── fifo.py
│   ├── spt.py
│   └── wspt.py
├── data/
│   ├── large_dataset.py
│   └── small_dataset.py
├── results/
│   └── Team7_Scheduling_Final.py

This code compares FIFO, SPT, EDD, and WSPT using small and large datasets.

It shows:
1. Small data results for all algorithms
2. Big data experiment results for all algorithms
3. Total Completion Time, ΣCj
4. Runtime
5. Big-O notation
6. Tardiness
7. Job sequence
8. Runtime and Total Completion Time graphs by data size

Coding style:
1. Function-based implementation
2. Dictionary / list data structure
3. Simple and visible steps
4. No complex classes
"""

import os
import sys
import csv
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Step 0. Set project root path
# ------------------------------------------------------------
# This file is placed inside the results folder.
# Therefore, the parent folder is the project root folder.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

# Add project root to Python module search path.
# This allows imports such as data.small_dataset and algorithms.fifo.
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from data.small_dataset import get_small_jobs, validate_small_jobs
from data.large_dataset import generate_large_jobs, validate_large_jobs

from algorithms.fifo import run_fifo
from algorithms.spt import run_spt
from algorithms.edd import run_edd
from algorithms.wspt import run_wspt


PROJECT_INFO = {
    "topic": "Single Machine Scheduling Algorithm Comparison for Minimizing Total Completion Time in Automotive Parts Manufacturing",
    "objective": "Minimize Total Completion Time, ΣCj",
    "algorithms": ["FIFO", "SPT", "EDD", "WSPT"],
    "main_metric": "Total Completion Time, ΣCj",
    "small_dataset": "10 automotive manufacturing jobs",
    "large_dataset": "Randomly generated 1000 jobs with dependency constraints",
    "presentation_required_items": [
        "Objectives",
        "Algorithms",
        "Small data results for all algorithms",
        "Big data experiment results for all algorithms",
        "Performance comparison using Big-O notation",
        "Conclusion and each member's role",
    ],
    "evaluation_criteria": {
        "Complexity": "30%",
        "Completeness": "20%",
        "Credibility": "20%",
        "Creativity": "20%",
        "Individual Score": "10%",
    },
}


# ------------------------------------------------------------
# Function title (KR): 프로젝트 정보 출력 함수
# ------------------------------------------------------------
def print_project_info():
    """
    Print project information and presentation checklist.
    """
    print("\n" + "=" * 80)
    print("PROJECT INFORMATION")
    print("=" * 80)
    print(f"Topic      : {PROJECT_INFO['topic']}")
    print(f"Objective  : {PROJECT_INFO['objective']}")
    print(f"Algorithms : {', '.join(PROJECT_INFO['algorithms'])}")
    print(f"Main Metric: {PROJECT_INFO['main_metric']}")

    print("\nPresentation Required Items:")
    for item in PROJECT_INFO["presentation_required_items"]:
        print(f"- {item}")

    print("\nEvaluation Criteria:")
    for key, value in PROJECT_INFO["evaluation_criteria"].items():
        print(f"- {key}: {value}")

    print("=" * 80 + "\n")


# ------------------------------------------------------------
# Function title (KR): 알고리즘 목록 생성 함수
# ------------------------------------------------------------
def get_algorithm_runners():
    """
    Return algorithm runner functions as a dictionary.
    """
    return {
        "FIFO": run_fifo,
        "SPT": run_spt,
        "EDD": run_edd,
        "WSPT": run_wspt,
    }


# ------------------------------------------------------------
# Function title (KR): 콘솔 표 출력 보조 함수
# ------------------------------------------------------------
def print_table(title, columns, rows):
    """
    Print rows in a clean console table format.

    Parameters:
        title (str): table title
        columns (list): column names
        rows (list): list of dictionaries
    """
    if not rows:
        print(f"\n{title}")
        print("(No data)")
        return

    widths = {}
    for column in columns:
        max_data_width = max(len(str(row.get(column, ""))) for row in rows)
        widths[column] = max(len(column), max_data_width)

    total_width = sum(widths[column] for column in columns) + 3 * (len(columns) - 1)

    print("\n" + "=" * total_width)
    print(title.center(total_width))
    print("=" * total_width)

    header = " | ".join(f"{column:<{widths[column]}}" for column in columns)
    print(header)
    print("-" * total_width)

    for row in rows:
        line = " | ".join(f"{str(row.get(column, '')):<{widths[column]}}" for column in columns)
        print(line)

    print("=" * total_width + "\n")


# ------------------------------------------------------------
# Function title (KR): 숫자 포맷 함수
# ------------------------------------------------------------
def format_number(value):
    """
    Format numeric values for better readability in console tables.
    """
    if isinstance(value, float):
        return f"{value:,.4f}"
    if isinstance(value, int):
        return f"{value:,}"
    return value


# ------------------------------------------------------------
# Function title (KR): 알고리즘별 결과 행 생성 함수
# ------------------------------------------------------------
def create_algorithm_display_row(algorithm_name, metrics, runtime):
    """
    Create a display row for one algorithm result.
    """
    return {
        "Algorithm": algorithm_name,
        "n": format_number(metrics["n_jobs"]),
        "ΣCj": format_number(metrics["total_Cj"]),
        "Avg Cj": format_number(metrics["avg_completion_time"]),
        "Avg Wait": format_number(metrics["avg_waiting_time"]),
        "Tardiness": format_number(metrics["total_tardiness"]),
        "Tardy Jobs": format_number(metrics["tardy_jobs"]),
        "Makespan": format_number(metrics["makespan"]),
        "Big-O": metrics["big_o"],
        "Runtime(ms)": format_number(runtime),
    }


# ------------------------------------------------------------
# Function title (KR): 작업 순서 표 출력 함수
# ------------------------------------------------------------
def print_sequence_table(dataset_name, sequence_rows):
    """
    Print job sequence results in a separate table.

    This keeps the main metric table readable.
    """
    print_table(
        title=f"JOB SEQUENCE TABLE - {dataset_name}",
        columns=["Algorithm", "Job Sequence"],
        rows=sequence_rows,
    )


# ------------------------------------------------------------
# Function title (KR): 작업 순서 추출 함수
# ------------------------------------------------------------
def get_job_sequence(results):
    """
    Extract the job sequence from scheduling results.
    """
    return " -> ".join(result["job_id"] for result in results)


# ------------------------------------------------------------
# Function title (KR): 작업 순서 축약 함수
# ------------------------------------------------------------
def shorten_sequence(results, max_jobs=20):
    """
    Shorten long job sequences for console output.
    """
    if len(results) <= max_jobs:
        return get_job_sequence(results)

    short_sequence = " -> ".join(result["job_id"] for result in results[:max_jobs])
    short_sequence += " -> ..."
    return short_sequence


# ------------------------------------------------------------
# Function title (KR): 비교용 요약 행 생성 함수
# ------------------------------------------------------------
def create_summary_row(dataset_name, algorithm_name, metrics, runtime, sequence):
    """
    Create one summary row for comparison tables.
    """
    row = {
        "dataset": dataset_name,
        "algorithm": algorithm_name,
        "n_jobs": metrics["n_jobs"],
        "total_completion_time_Sigma_Cj": metrics["total_Cj"],
        "avg_completion_time": metrics["avg_completion_time"],
        "avg_waiting_time": metrics["avg_waiting_time"],
        "total_flow_time": metrics["total_flow_time"],
        "avg_flow_time": metrics["avg_flow_time"],
        "total_tardiness": metrics["total_tardiness"],
        "tardy_jobs": metrics["tardy_jobs"],
        "makespan": metrics["makespan"],
        "big_o": metrics["big_o"],
        "runtime_ms": runtime,
        "job_sequence": sequence,
    }

    if "total_wCj" in metrics:
        row["total_weighted_completion_time_Sigma_wCj"] = metrics["total_wCj"]
    else:
        row["total_weighted_completion_time_Sigma_wCj"] = ""

    return row


# ------------------------------------------------------------
# Function title (KR): 단일 데이터셋 알고리즘 비교 함수
# ------------------------------------------------------------
def compare_algorithms_on_dataset(jobs, dataset_name, show_full_sequence=True):
    """
    Run all algorithms on one dataset and compare the results.

    The console output is separated into:
        1. Main metric table
        2. Job sequence table
    """
    algorithm_runners = get_algorithm_runners()
    summary_rows = []
    detailed_results_by_algorithm = {}
    display_rows = []
    sequence_rows = []

    for algorithm_name, runner in algorithm_runners.items():
        input_jobs = [job.copy() for job in jobs]
        results, metrics, runtime = runner(input_jobs)

        full_sequence = get_job_sequence(results)
        if show_full_sequence:
            printed_sequence = full_sequence
        else:
            printed_sequence = shorten_sequence(results, max_jobs=20)

        summary_row = create_summary_row(
            dataset_name=dataset_name,
            algorithm_name=algorithm_name,
            metrics=metrics,
            runtime=runtime,
            sequence=printed_sequence,
        )
        summary_rows.append(summary_row)

        detailed_results_by_algorithm[algorithm_name] = {
            "results": results,
            "metrics": metrics,
            "runtime": runtime,
            "sequence": full_sequence,
        }

        display_rows.append(
            create_algorithm_display_row(
                algorithm_name=algorithm_name,
                metrics=metrics,
                runtime=runtime,
            )
        )

        sequence_rows.append({
            "Algorithm": algorithm_name,
            "Job Sequence": printed_sequence,
        })

    print_table(
        title=f"ALGORITHM COMPARISON TABLE - {dataset_name}",
        columns=[
            "Algorithm", "n", "ΣCj", "Avg Cj", "Avg Wait",
            "Tardiness", "Tardy Jobs", "Makespan", "Big-O", "Runtime(ms)",
        ],
        rows=display_rows,
    )

    print_sequence_table(dataset_name, sequence_rows)

    return summary_rows, detailed_results_by_algorithm


# ------------------------------------------------------------
# Function title (KR): 요약 표 출력 함수
# ------------------------------------------------------------
def print_summary_table(summary_rows):
    """
    Print a compact final summary table.
    """
    display_rows = []

    for row in summary_rows:
        display_rows.append({
            "Dataset": row["dataset"],
            "Algorithm": row["algorithm"],
            "n": format_number(row["n_jobs"]),
            "ΣCj": format_number(row["total_completion_time_Sigma_Cj"]),
            "Avg Cj": format_number(row["avg_completion_time"]),
            "Avg Wait": format_number(row["avg_waiting_time"]),
            "Tardiness": format_number(row["total_tardiness"]),
            "Tardy Jobs": format_number(row["tardy_jobs"]),
            "Makespan": format_number(row["makespan"]),
            "Big-O": row["big_o"],
            "Runtime(ms)": format_number(row["runtime_ms"]),
        })

    print_table(
        title="FINAL SUMMARY COMPARISON TABLE",
        columns=[
            "Dataset", "Algorithm", "n", "ΣCj", "Avg Cj", "Avg Wait",
            "Tardiness", "Tardy Jobs", "Makespan", "Big-O", "Runtime(ms)",
        ],
        rows=display_rows,
    )


# ------------------------------------------------------------
# Function title (KR): CSV 저장 함수
# ------------------------------------------------------------
def save_summary_to_csv(summary_rows, filepath):
    """
    Save comparison summary rows to a CSV file.
    """
    if not summary_rows:
        return

    fieldnames = list(summary_rows[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"[Saved] {filepath}")


# ------------------------------------------------------------
# Function title (KR): 상세 결과 CSV 저장 함수
# ------------------------------------------------------------
def save_detailed_results_to_csv(detailed_results, dataset_name, output_dir):
    """
    Save detailed scheduling results for each algorithm.
    """
    for algorithm_name, data in detailed_results.items():
        results = data["results"]
        if not results:
            continue

        filename = f"{dataset_name.lower().replace(' ', '_')}_{algorithm_name.lower()}_detailed_results.csv"
        filepath = os.path.join(output_dir, filename)
        fieldnames = list(results[0].keys())

        with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"[Saved] {filepath}")


# ------------------------------------------------------------
# Function title (KR): 데이터 크기별 실험 함수
# ------------------------------------------------------------
def run_size_experiment(data_sizes, seed=7):
    """
    Run experiments for multiple dataset sizes.

    This is used to show how runtime and Total Completion Time change
    as the number of jobs increases.
    """
    algorithm_runners = get_algorithm_runners()
    experiment_rows = []
    display_rows = []

    for n in data_sizes:
        if n == 0:
            for algorithm_name in algorithm_runners:
                experiment_rows.append({
                    "n_jobs": 0,
                    "algorithm": algorithm_name,
                    "total_completion_time_Sigma_Cj": 0,
                    "runtime_ms": 0,
                    "big_o": "N/A",
                    "total_tardiness": 0,
                    "tardy_jobs": 0,
                })

                display_rows.append({
                    "n": "0",
                    "Algorithm": algorithm_name,
                    "ΣCj": "0",
                    "Runtime(ms)": "0",
                    "Big-O": "N/A",
                    "Tardiness": "0",
                    "Tardy Jobs": "0",
                })
            continue

        jobs = generate_large_jobs(n=n, seed=seed)
        validate_large_jobs(jobs)

        for algorithm_name, runner in algorithm_runners.items():
            input_jobs = [job.copy() for job in jobs]
            results, metrics, runtime = runner(input_jobs)

            experiment_rows.append({
                "n_jobs": n,
                "algorithm": algorithm_name,
                "total_completion_time_Sigma_Cj": metrics["total_Cj"],
                "runtime_ms": runtime,
                "big_o": metrics["big_o"],
                "total_tardiness": metrics["total_tardiness"],
                "tardy_jobs": metrics["tardy_jobs"],
            })

            display_rows.append({
                "n": format_number(n),
                "Algorithm": algorithm_name,
                "ΣCj": format_number(metrics["total_Cj"]),
                "Runtime(ms)": format_number(runtime),
                "Big-O": metrics["big_o"],
                "Tardiness": format_number(metrics["total_tardiness"]),
                "Tardy Jobs": format_number(metrics["tardy_jobs"]),
            })

    print_table(
        title="DATA SIZE EXPERIMENT TABLE",
        columns=["n", "Algorithm", "ΣCj", "Runtime(ms)", "Big-O", "Tardiness", "Tardy Jobs"],
        rows=display_rows,
    )

    return experiment_rows


# ------------------------------------------------------------
# Function title (KR): 실험 결과 CSV 저장 함수
# ------------------------------------------------------------
def save_experiment_to_csv(experiment_rows, filepath):
    """
    Save data size experiment results to CSV.
    """
    if not experiment_rows:
        return

    fieldnames = list(experiment_rows[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(experiment_rows)

    print(f"[Saved] {filepath}")


# ------------------------------------------------------------
# Function title (KR): 그래프용 데이터 추출 함수
# ------------------------------------------------------------
def get_series_by_algorithm(experiment_rows, value_key):
    """
    Convert experiment rows into series data for plotting.
    """
    series = {}

    for row in experiment_rows:
        algorithm = row["algorithm"]
        if algorithm not in series:
            series[algorithm] = []
        series[algorithm].append((row["n_jobs"], row[value_key]))

    for algorithm in series:
        series[algorithm] = sorted(series[algorithm], key=lambda item: item[0])

    return series


# ------------------------------------------------------------
# Function title (KR): 러닝타임 그래프 생성 함수
# ------------------------------------------------------------
def plot_runtime_graph(experiment_rows, output_path):
    """
    Plot runtime by dataset size for each algorithm.
    """
    series = get_series_by_algorithm(experiment_rows, "runtime_ms")

    plt.figure(figsize=(10, 6))

    for algorithm, values in series.items():
        x_values = [item[0] for item in values]
        y_values = [item[1] for item in values]
        plt.plot(x_values, y_values, marker="o", label=algorithm)

    plt.title("Algorithm Runtime by Dataset Size")
    plt.xlabel("# Data")
    plt.ylabel("Runtime (milliseconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"[Saved] {output_path}")


# ------------------------------------------------------------
# Function title (KR): 총 완료시간 그래프 생성 함수
# ------------------------------------------------------------
def plot_total_completion_time_graph(experiment_rows, output_path):
    """
    Plot Total Completion Time, ΣCj by dataset size for each algorithm.
    """
    series = get_series_by_algorithm(experiment_rows, "total_completion_time_Sigma_Cj")

    plt.figure(figsize=(10, 6))

    for algorithm, values in series.items():
        x_values = [item[0] for item in values]
        y_values = [item[1] for item in values]
        plt.plot(x_values, y_values, marker="o", label=algorithm)

    plt.title("Total Completion Time, ΣCj by Dataset Size")
    plt.xlabel("# Data")
    plt.ylabel("Total Completion Time, ΣCj")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"[Saved] {output_path}")

# ------------------------------------------------------------
# Function title (KR): 결론 생성 함수
# ------------------------------------------------------------
def print_conclusion(summary_rows):
    """
    Print a simple conclusion based on Total Completion Time, ΣCj.
    """
    conclusion_rows = []
    dataset_names = sorted(set(row["dataset"] for row in summary_rows))

    for dataset_name in dataset_names:
        rows = [row for row in summary_rows if row["dataset"] == dataset_name]
        best_row = min(rows, key=lambda row: row["total_completion_time_Sigma_Cj"])

        conclusion_rows.append({
            "Dataset": dataset_name,
            "Best Algorithm": best_row["algorithm"],
            "Minimum ΣCj": format_number(best_row["total_completion_time_Sigma_Cj"]),
            "Runtime(ms)": format_number(best_row["runtime_ms"]),
            "Big-O": best_row["big_o"],
        })

    print_table(
        title="CONCLUSION TABLE BASED ON TOTAL COMPLETION TIME, ΣCj",
        columns=["Dataset", "Best Algorithm", "Minimum ΣCj", "Runtime(ms)", "Big-O"],
        rows=conclusion_rows,
    )

    print("Interpretation:")
    print("- SPT is expected to perform strongly for minimizing Total Completion Time, ΣCj.")
    print("- FIFO is simple and fast in runtime, but it may not minimize ΣCj.")
    print("- EDD is useful as a due-date-aware comparison rule.")
    print("- WSPT reflects priority_weight and is meaningful when job importance is considered.")
    print()


# ------------------------------------------------------------
# Function title (KR): 메인 실행 함수
# ------------------------------------------------------------
def main():
    """
    Run the full final comparison workflow.

    Workflow:
        1. Print project information
        2. Load and validate small dataset
        3. Generate and validate large dataset
        4. Run all algorithms on small dataset
        5. Run all algorithms on large dataset
        6. Run data size experiment from 0 to 1000 jobs
        7. Save CSV files
        8. Save runtime and Total Completion Time graphs
        9. Print conclusion
    """
    output_dir = CURRENT_DIR
    os.makedirs(output_dir, exist_ok=True)

    print_project_info()

    small_jobs = get_small_jobs()
    validate_small_jobs(small_jobs)

    large_jobs = generate_large_jobs(n=1000, seed=7)
    validate_large_jobs(large_jobs)

    small_summary, small_details = compare_algorithms_on_dataset(
        jobs=small_jobs,
        dataset_name="Small Data",
        show_full_sequence=True,
    )

    large_summary, large_details = compare_algorithms_on_dataset(
        jobs=large_jobs,
        dataset_name="Large Data",
        show_full_sequence=False,
    )

    all_summary_rows = small_summary + large_summary
    print_summary_table(all_summary_rows)

    save_summary_to_csv(
        summary_rows=all_summary_rows,
        filepath=os.path.join(output_dir, "summary_comparison.csv"),
    )

    save_detailed_results_to_csv(
        detailed_results=small_details,
        dataset_name="Small Data",
        output_dir=output_dir,
    )

    save_detailed_results_to_csv(
        detailed_results=large_details,
        dataset_name="Large Data",
        output_dir=output_dir,
    )

    data_sizes = [0, 10, 50, 100, 250, 500, 750, 1000]
    experiment_rows = run_size_experiment(data_sizes=data_sizes, seed=7)

    save_experiment_to_csv(
        experiment_rows=experiment_rows,
        filepath=os.path.join(output_dir, "data_size_experiment.csv"),
    )

    plot_runtime_graph(
        experiment_rows=experiment_rows,
        output_path=os.path.join(output_dir, "runtime_by_data_size.png"),
    )

    plot_total_completion_time_graph(
        experiment_rows=experiment_rows,
        output_path=os.path.join(output_dir, "total_completion_time_by_data_size.png"),
    )

    print_conclusion(all_summary_rows)

    print("Final comparison completed successfully.")
    print(f"Output folder: {output_dir}")


# ------------------------------------------------------------
# Step 12. Execute main function
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
