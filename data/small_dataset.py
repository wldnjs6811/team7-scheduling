"""
Small dataset for Team 7 single-machine scheduling project.

Source:
- Team7_revised_single_machine_scheduling.xlsx
- Sheet: 02_Revised_Small_Dataset

Project:
Single Machine Scheduling Algorithm Comparison for Minimizing
Total Completion Time in Automotive Parts Manufacturing

Objective:
Minimize Total Completion Time, ΣCj

Columns:
job_id, product, operation_type, processing_time, arrival_time,
due_date, priority_weight, p_over_w_ratio

Notes:
- processing_time > 0
- due_date > arrival_time
- p_over_w_ratio = processing_time / priority_weight
- This small dataset is designed so that FIFO, SPT, EDD, and WSPT
  do not all produce the same job sequence.
"""

from copy import deepcopy


small_jobs = [
    {
        "job_id": "J1",
        "product": "Sensor Housing",
        "operation_type": "Milling",
        "processing_time": 18,
        "arrival_time": 0,
        "due_date": 110,
        "priority_weight": 2,
        "p_over_w_ratio": 9.0,
    },
    {
        "job_id": "J2",
        "product": "Brake Component",
        "operation_type": "Drilling",
        "processing_time": 42,
        "arrival_time": 0,
        "due_date": 90,
        "priority_weight": 5,
        "p_over_w_ratio": 8.4,
    },
    {
        "job_id": "J3",
        "product": "Engine Bracket",
        "operation_type": "Grinding",
        "processing_time": 25,
        "arrival_time": 5,
        "due_date": 160,
        "priority_weight": 3,
        "p_over_w_ratio": 8.33,
    },
    {
        "job_id": "J4",
        "product": "Battery Module Cover",
        "operation_type": "Assembly",
        "processing_time": 60,
        "arrival_time": 10,
        "due_date": 150,
        "priority_weight": 4,
        "p_over_w_ratio": 15.0,
    },
    {
        "job_id": "J5",
        "product": "Drive Shaft",
        "operation_type": "Lathe",
        "processing_time": 35,
        "arrival_time": 0,
        "due_date": 120,
        "priority_weight": 2,
        "p_over_w_ratio": 17.5,
    },
    {
        "job_id": "J6",
        "product": "EV Battery Case",
        "operation_type": "Additive Manufacturing",
        "processing_time": 85,
        "arrival_time": 15,
        "due_date": 260,
        "priority_weight": 5,
        "p_over_w_ratio": 17.0,
    },
    {
        "job_id": "J7",
        "product": "Gear Plate",
        "operation_type": "Milling",
        "processing_time": 22,
        "arrival_time": 8,
        "due_date": 100,
        "priority_weight": 1,
        "p_over_w_ratio": 22.0,
    },
    {
        "job_id": "J8",
        "product": "Control Box",
        "operation_type": "Assembly",
        "processing_time": 55,
        "arrival_time": 20,
        "due_date": 180,
        "priority_weight": 4,
        "p_over_w_ratio": 13.75,
    },
    {
        "job_id": "J9",
        "product": "Cooling Fan Hub",
        "operation_type": "Drilling",
        "processing_time": 12,
        "arrival_time": 3,
        "due_date": 70,
        "priority_weight": 3,
        "p_over_w_ratio": 4.0,
    },
    {
        "job_id": "J10",
        "product": "Precision Shaft",
        "operation_type": "Lathe",
        "processing_time": 48,
        "arrival_time": 12,
        "due_date": 140,
        "priority_weight": 5,
        "p_over_w_ratio": 9.6,
    },
]


def get_small_jobs():
    """
    Return a deep copy of the small job dataset.

    A deep copy is used so that sorting or modifying jobs in one algorithm
    does not affect the original dataset or other algorithms.
    """
    return deepcopy(small_jobs)


def validate_small_jobs(jobs=None):
    """
    Validate the small dataset based on the project constraints.

    Returns:
        True if all jobs satisfy the constraints.

    Raises:
        ValueError if any job violates a constraint.
    """
    if jobs is None:
        jobs = small_jobs

    for job in jobs:
        job_id = job["job_id"]

        if job["processing_time"] <= 0:
            raise ValueError(f"{job_id}: processing_time must be greater than 0.")

        if job["due_date"] <= job["arrival_time"]:
            raise ValueError(f"{job_id}: due_date must be greater than arrival_time.")

        if job["priority_weight"] <= 0:
            raise ValueError(f"{job_id}: priority_weight must be greater than 0.")

        expected_ratio = round(job["processing_time"] / job["priority_weight"], 2)
        actual_ratio = round(job["p_over_w_ratio"], 2)

        if actual_ratio != expected_ratio:
            raise ValueError(
                f"{job_id}: p_over_w_ratio should be {expected_ratio}, "
                f"but got {actual_ratio}."
            )

    return True


if __name__ == "__main__":
    validate_small_jobs()
    print(f"Small dataset validation passed. Number of jobs: {len(small_jobs)}")
    print("First job:", small_jobs[0])
