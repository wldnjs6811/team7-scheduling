"""
Team 7 - Small Dataset
Project: Single Machine Scheduling Algorithm Comparison
Context: Automotive Parts Manufacturing

This code follows the professor's coding guidance:
1. Implement with functions
2. Use dictionary and list data structures
3. Keep the structure simple and intuitive
4. Make each step visible
5. Avoid unnecessary complex classes
"""

from copy import deepcopy
from pprint import pprint


# ------------------------------------------------------------
# Step 1. Define raw small dataset
# ------------------------------------------------------------
# Each job is represented as a dictionary.
# The whole input dataset is represented as a list of dictionaries.
#
# p_over_w_ratio = processing_time / priority_weight
# This column is used for WSPT / priority-based scheduling.

SMALL_JOB_DATA = [
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


# ------------------------------------------------------------
# Step 2. Check calculated column
# ------------------------------------------------------------
def check_p_over_w_ratio(job):
    """
    Check whether p_over_w_ratio is correctly calculated.

    Formula:
        p_over_w_ratio = processing_time / priority_weight
    """
    expected_ratio = round(job["processing_time"] / job["priority_weight"], 2)
    actual_ratio = round(job["p_over_w_ratio"], 2)

    return expected_ratio == actual_ratio


# ------------------------------------------------------------
# Step 3. Create small dataset
# ------------------------------------------------------------
def create_small_jobs():
    """
    Create the small dataset as a list of dictionaries.

    Returns:
        small_jobs (list): list of job dictionaries
    """
    small_jobs = []

    for job in SMALL_JOB_DATA:
        small_jobs.append(job.copy())

    return small_jobs


# ------------------------------------------------------------
# Step 4. Get small dataset safely
# ------------------------------------------------------------
def get_small_jobs():
    """
    Return a deep copy of the small dataset.

    A deep copy is used so that sorting or modifying jobs in one algorithm
    does not affect the original dataset or other algorithms.
    """
    small_jobs = create_small_jobs()

    return deepcopy(small_jobs)


# ------------------------------------------------------------
# Step 5. Validate small dataset
# ------------------------------------------------------------
def validate_small_jobs(jobs=None):
    """
    Validate whether the small dataset satisfies project constraints.

    Conditions:
        processing_time > 0
        due_date > arrival_time
        priority_weight > 0
        p_over_w_ratio = processing_time / priority_weight
    """
    if jobs is None:
        jobs = create_small_jobs()

    for job in jobs:
        job_id = job["job_id"]

        if job["processing_time"] <= 0:
            raise ValueError(f"{job_id}: processing_time must be greater than 0.")

        if job["due_date"] <= job["arrival_time"]:
            raise ValueError(f"{job_id}: due_date must be greater than arrival_time.")

        if job["priority_weight"] <= 0:
            raise ValueError(f"{job_id}: priority_weight must be greater than 0.")

        if not check_p_over_w_ratio(job):
            expected_ratio = round(job["processing_time"] / job["priority_weight"], 2)
            actual_ratio = round(job["p_over_w_ratio"], 2)
            raise ValueError(
                f"{job_id}: p_over_w_ratio should be {expected_ratio}, "
                f"but got {actual_ratio}."
            )

    return True


# ------------------------------------------------------------
# Step 6. Print small dataset
# ------------------------------------------------------------
def print_small_jobs(jobs=None):
    """
    Print the small dataset while keeping dictionary key order.
    """
    if jobs is None:
        jobs = create_small_jobs()

    pprint(jobs, sort_dicts=False)


# ------------------------------------------------------------
# Step 7. Create default small dataset
# ------------------------------------------------------------
small_jobs = create_small_jobs()


# ------------------------------------------------------------
# Step 8. Run validation and print dataset
# ------------------------------------------------------------
if __name__ == "__main__":
    validate_small_jobs(small_jobs)

    print("Small dataset validation passed.")
    print(f"Number of jobs: {len(small_jobs)}")
    print()

    print("Small dataset:")
    print_small_jobs(small_jobs)
