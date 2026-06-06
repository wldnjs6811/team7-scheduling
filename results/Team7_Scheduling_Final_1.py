
"""
Team 7 - Final Algorithm Comparison
Project: Single Machine Scheduling Algorithm Comparison
Context: Automotive Parts Manufacturing

This code is designed for the final presentation and final report.

It compares:
1. FIFO
2. SPT
3. EDD
4. WSPT

It shows:
1. Small data results for all algorithms
2. Big data experiment results for all algorithms
3. Total Completion Time, ΣCj
4. Runtime
5. Big-O notation
6. Tardiness
7. Job sequence
8. Graphs for runtime and Total Completion Time by data size

Coding style:
1. Function-based implementation
2. Dictionary / list data structure
3. Simple and visible steps
4. No complex classes
"""

import os
import csv
from pprint import pprint

import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Step 1. Import dataset and algorithm modules
# ------------------------------------------------------------
# Required files should be in the same folder:
# - small_dataset_functional_with_ratio.py
# - large_dataset_generator_functional_최종.py
# - fifo_final.py
# - spt_final.py
# - edd_final.py
# - wspt_final.py

from small_dataset_functional_with_ratio import get_small_jobs, validate_small_jobs
from large_dataset_generator_functional_최종 import generate_large_jobs, validate_large_jobs

from fifo_final import run_fifo
from spt_final import run_spt
from edd_final import run_edd
from wspt_final import run_wspt


# ------------------------------------------------------------
# Step 2. Define project information
# ------------------------------------------------------------
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

    This helps the team check whether the final comparison code covers
    the required presentation and final report items.
    """
    print("\n" + "=" * 80)
    print("PROJECT INFORMATION")
    print("=" * 80)
    print(f"Topic     : {PROJECT_INFO['topic']}")
    print(f"Objective : {PROJECT_INFO['objective']}")
    print(f"Algorithms: {', '.join(PROJECT_INFO['algorithms'])}")
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

    Each runner receives a list of job dictionaries and returns:
        results, metrics, runtime
    """
    algorithm_runners = {
        "FIFO": run_fifo,
        "SPT": run_spt,
        "EDD": run_edd,
        "WSPT": run_wspt,
    }

    return algorithm_runners


# ------------------------------------------------------------
# Function title (KR): 작업 순서 추출 함수
# ------------------------------------------------------------
def get_job_sequence(results):
    """
    Extract the job sequence from scheduling results.

    Parameters:
        results (list): scheduled result dictionaries

    Returns:
        sequence (str): job sequence such as J1 -> J2 -> J3
    """
    sequence = " -> ".join(result["job_id"] for result in results)

    return sequence


# ------------------------------------------------------------
# Function title (KR): 비교용 요약 행 생성 함수
# ------------------------------------------------------------
def create_summary_row(dataset_name, algorithm_name, metrics, runtime, sequence):
    """
    Create one summary row for comparison tables.

    This row includes the main objective value, runtime, Big-O,
    tardiness, and job sequence.
    """
    row = {
        "dataset": dataset_name,
        "algorithm": algorithm_name,
        "n_jobs": metrics["n_jobs"],
        "total_completion_time_Sigma_Cj": metrics["total_Cj"],
        "avg_completion_time": metrics["avg_completion_time"],
        "avg_waiting_time": metrics["avg_waiting_time"],
        "total_flow_time": metrics["total_flow_time"],
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

    Parameters:
        jobs (list): list of job dictionaries
        dataset_name (str): name of the dataset
        show_full_sequence (bool): if False, long sequences are shortened

    Returns:
        summary_rows (list): comparison rows
        detailed_results (dict): algorithm results and metrics
    """
    algorithm_runners = get_algorithm_runners()

    summary_rows = []
    detailed_results = {}

    print("\n" + "=" * 80)
    print(f"ALGORITHM COMPARISON - {dataset_name}")
    print("=" * 80)

    for algorithm_name, runner in algorithm_runners.items():
        # Use a copy of each job dictionary so that one algorithm cannot affect another.
        input_jobs = [job.copy() for job in jobs]

        results, metrics, runtime = runner(input_jobs)
        sequence = get_job_sequence(results)

        if not show_full_sequence and len(results) > 20:
            short_sequence = " -> ".join(result["job_id"] for result in results[:20])
            short_sequence += " -> ... "
        else:
            short_sequence = sequence

        summary_row = create_summary_row(
            dataset_name=dataset_name,
            algorithm_name=algorithm_name,
            metrics=metrics,
            runtime=runtime,
            sequence=short_sequence,
        )

        summary_rows.append(summary_row)

        detailed_results[algorithm_name] = {
            "results": results,
            "metrics": metrics,
            "runtime": runtime,
            "sequence": sequence,
        }

        print(f"\n[{algorithm_name}]")
        print(f"Job Sequence                  : {short_sequence}")
        print(f"Total Completion Time, ΣCj    : {metrics['total_Cj']}")
        print(f"Runtime                       : {runtime} ms")
        print(f"Big-O                         : {metrics['big_o']}")
        print(f"Total Tardiness               : {metrics['total_tardiness']}")
        print(f"Tardy Jobs                    : {metrics['tardy_jobs']}")

        if "total_wCj" in metrics:
            print(f"Weighted Completion Time, ΣwCj: {metrics['total_wCj']}")

    print("=" * 80 + "\n")

    return summary_rows, detailed_results


# ------------------------------------------------------------
# Function title (KR): 요약 표 출력 함수
# ------------------------------------------------------------
def print_summary_table(summary_rows):
    """
    Print a compact comparison table.

    The table focuses on key presentation metrics:
        Total Completion Time, runtime, Big-O, tardiness, and makespan.
    """
    print("\n" + "=" * 110)
    print("SUMMARY TABLE")
    print("=" * 110)

    header = (
        f"{'Dataset':<16}"
        f"{'Algorithm':<10}"
        f"{'n':>8}"
        f"{'ΣCj':>14}"
        f"{'Runtime(ms)':>14}"
        f"{'Big-O':>12}"
        f"{'Tardiness':>14}"
        f"{'Tardy Jobs':>12}"
        f"{'Makespan':>12}"
    )
    print(header)
    print("-" * 110)

    for row in summary_rows:
        print(
            f"{row['dataset']:<16}"
            f"{row['algorithm']:<10}"
            f"{row['n_jobs']:>8}"
            f"{row['total_completion_time_Sigma_Cj']:>14}"
            f"{row['runtime_ms']:>14.4f}"
            f"{row['big_o']:>12}"
            f"{row['total_tardiness']:>14}"
            f"{row['tardy_jobs']:>12}"
            f"{row['makespan']:>12}"
        )

    print("=" * 110 + "\n")


# ------------------------------------------------------------
# Function title (KR): CSV 저장 함수
# ------------------------------------------------------------
def save_summary_to_csv(summary_rows, filepath):
    """
    Save comparison summary rows to a CSV file.

    This file can be used for the final report or presentation table.
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

    Each CSV file contains:
        seq, job_id, start_time, completion_time, waiting_time,
        flow_time, tardiness, and other job information.
    """
    for algorithm_name, data in detailed_results.items():
        results = data["results"]

        if not results:
            continue

        filepath = os.path.join(
            output_dir,
            f"{dataset_name.lower().replace(' ', '_')}_{algorithm_name.lower()}_detailed_results.csv",
        )

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

    Parameters:
        data_sizes (list): example [0, 10, 50, 100, 250, 500, 750, 1000]
        seed (int): fixed random seed for reproducible large datasets

    Returns:
        experiment_rows (list): result rows for graph and CSV
    """
    algorithm_runners = get_algorithm_runners()
    experiment_rows = []

    print("\n" + "=" * 80)
    print("DATA SIZE EXPERIMENT")
    print("=" * 80)

    for n in data_sizes:
        print(f"\nRunning experiment for n = {n}")

        if n == 0:
            # n=0 is included only for graph baseline.
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

            print(
                f"  {algorithm_name:<5} | "
                f"ΣCj = {metrics['total_Cj']:<12} | "
                f"Runtime = {runtime:.4f} ms | "
                f"Big-O = {metrics['big_o']}"
            )

    print("=" * 80 + "\n")

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

    Parameters:
        experiment_rows (list): rows from run_size_experiment
        value_key (str): 'runtime_ms' or 'total_completion_time_Sigma_Cj'

    Returns:
        series (dict): algorithm -> list of (n_jobs, value)
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

    The graph is saved as a PNG file.
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

    The graph is saved as a PNG file.
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

    Since the main objective is minimizing ΣCj, the algorithm with
    the smallest total_Cj is selected as the best algorithm for each dataset.
    """
    print("\n" + "=" * 80)
    print("CONCLUSION BASED ON TOTAL COMPLETION TIME, ΣCj")
    print("=" * 80)

    dataset_names = sorted(set(row["dataset"] for row in summary_rows))

    for dataset_name in dataset_names:
        rows = [row for row in summary_rows if row["dataset"] == dataset_name]
        best_row = min(rows, key=lambda row: row["total_completion_time_Sigma_Cj"])

        print(
            f"For {dataset_name}, the best algorithm based on ΣCj is "
            f"{best_row['algorithm']} "
            f"with ΣCj = {best_row['total_completion_time_Sigma_Cj']}."
        )

    print("\nInterpretation:")
    print("- SPT is expected to perform strongly for minimizing Total Completion Time, ΣCj.")
    print("- FIFO is easy and fair by arrival order, but may perform worse when long jobs arrive early.")
    print("- EDD considers due dates, so it is useful as a due-date-aware comparison rule.")
    print("- WSPT reflects priority_weight and is useful as an extension when job importance is considered.")
    print("=" * 80 + "\n")


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
    output_dir = "team7_comparison_outputs"
    os.makedirs(output_dir, exist_ok=True)

    print_project_info()

    # Small dataset
    small_jobs = get_small_jobs()
    validate_small_jobs(small_jobs)

    # Large dataset
    large_jobs = generate_large_jobs(n=1000, seed=7)
    validate_large_jobs(large_jobs)

    # Compare algorithms on small and large datasets
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

    # Save comparison results
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

    # Run data size experiment for graph
    # 0 is used as a graph baseline.
    data_sizes = [0, 10, 50, 100, 250, 500, 750, 1000]
    experiment_rows = run_size_experiment(data_sizes=data_sizes, seed=7)

    save_experiment_to_csv(
        experiment_rows=experiment_rows,
        filepath=os.path.join(output_dir, "data_size_experiment.csv"),
    )

    # Save graphs
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
