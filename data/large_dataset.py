"""
Team 7 - Large Dataset Generator
Project: Single Machine Scheduling Algorithm Comparison
Context: Automotive Parts Manufacturing

This code follows the professor's coding guidance:
1. Implement with functions
2. Use dictionary and list data structures
3. Keep the structure simple and intuitive
4. Make each step visible
5. Avoid unnecessary complex classes
"""

import random
from pprint import pprint


# ------------------------------------------------------------
# Step 1. Define product and operation settings
# ------------------------------------------------------------
# Each product has possible operation types.
# Each operation type has its own processing_time range.
# This reflects dependency between product, operation_type, and processing_time.

PRODUCT_OPERATION_SETTINGS = {
    "Sensor Housing": {
        "Milling": (5, 25),
        "Drilling": (5, 20),
    },
    "Brake Component": {
        "Drilling": (15, 45),
        "Grinding": (20, 55),
    },
    "Engine Bracket": {
        "Milling": (25, 70),
        "Grinding": (30, 80),
    },
    "Gear Box Cover": {
        "Milling": (35, 90),
        "Drilling": (25, 75),
    },
    "Battery Module Cover": {
        "Assembly": (40, 100),
        "Milling": (35, 85),
    },
    "Drive Shaft": {
        "Lathe": (50, 120),
        "Grinding": (45, 110),
    },
    "EV Battery Case": {
        "Assembly": (60, 120),
        "Milling": (55, 115),
    },
}


# Product importance is used to determine priority_weight.
# Higher value means higher importance.
PRODUCT_IMPORTANCE = {
    "Sensor Housing": 1,
    "Brake Component": 4,
    "Engine Bracket": 3,
    "Gear Box Cover": 3,
    "Battery Module Cover": 4,
    "Drive Shaft": 4,
    "EV Battery Case": 5,
}


# ------------------------------------------------------------
# Step 2. Select product and operation type
# ------------------------------------------------------------
def select_product_and_operation():
    """
    Randomly select product and operation_type.

    Returns:
        product (str)
        operation_type (str)
        processing_range (tuple): (min_processing_time, max_processing_time)
    """
    product = random.choice(list(PRODUCT_OPERATION_SETTINGS.keys()))
    operation_type = random.choice(list(PRODUCT_OPERATION_SETTINGS[product].keys()))
    processing_range = PRODUCT_OPERATION_SETTINGS[product][operation_type]

    return product, operation_type, processing_range


# ------------------------------------------------------------
# Step 3. Generate processing_time
# ------------------------------------------------------------
def generate_processing_time(processing_range):
    """
    Generate processing_time according to product and operation_type range.

    Condition:
        processing_time > 0
        processing_time is within [5, 120]
    """
    min_time, max_time = processing_range
    processing_time = random.randint(min_time, max_time)

    return processing_time


# ------------------------------------------------------------
# Step 4. Generate arrival_time
# ------------------------------------------------------------
def generate_arrival_time():
    """
    Generate arrival_time.

    Condition:
        arrival_time is within [0, 500]
    """
    arrival_time = random.randint(0, 500)

    return arrival_time


# ------------------------------------------------------------
# Step 5. Determine urgent order and priority_weight
# ------------------------------------------------------------
def generate_priority_weight(product):
    """
    Generate priority_weight based on product importance and urgent order.

    Condition:
        priority_weight is within [1, 5]

    Logic:
        - Important products have higher base priority.
        - Urgent orders receive additional priority.
        - Final priority_weight is limited to 5.
    """
    base_priority = PRODUCT_IMPORTANCE[product]

    # 20% probability of urgent order
    urgent_order = random.random() < 0.20

    if urgent_order:
        priority_weight = min(5, base_priority + 1)
    else:
        priority_weight = base_priority

    # Safety check: keep priority_weight within [1, 5]
    priority_weight = max(1, min(priority_weight, 5))

    return priority_weight, urgent_order


# ------------------------------------------------------------
# Step 6. Generate due_date
# ------------------------------------------------------------
def generate_due_date(arrival_time, processing_time, urgent_order):
    """
    Generate due_date using:
        due_date = arrival_time + processing_time + slack_time

    Conditions:
        due_date > arrival_time
        due_date > arrival_time + processing_time

    Logic:
        - Urgent orders have shorter slack_time.
        - Normal orders have longer slack_time.
    """
    if urgent_order:
        slack_time = random.randint(10, 60)
    else:
        slack_time = random.randint(40, 150)

    due_date = arrival_time + processing_time + slack_time

    return due_date, slack_time


# ------------------------------------------------------------
# Step 7. Create one job dictionary
# ------------------------------------------------------------
def create_job(job_number):
    """
    Create one job as a dictionary.

    Output dictionary structure:
        job_id
        product
        operation_type
        processing_time
        arrival_time
        due_date
        priority_weight
        slack_time
        urgent_order
        p_over_w_ratio
    """
    product, operation_type, processing_range = select_product_and_operation()

    processing_time = generate_processing_time(processing_range)
    arrival_time = generate_arrival_time()
    priority_weight, urgent_order = generate_priority_weight(product)
    due_date, slack_time = generate_due_date(arrival_time, processing_time, urgent_order)

    job = {
        "job_id": f"J{job_number:04d}",
        "product": product,
        "operation_type": operation_type,
        "processing_time": processing_time,
        "arrival_time": arrival_time,
        "due_date": due_date,
        "priority_weight": priority_weight,
        "slack_time": slack_time,
        "urgent_order": urgent_order,
        "p_over_w_ratio": round(processing_time / priority_weight, 2),
    }

    return job


# ------------------------------------------------------------
# Step 8. Generate large dataset
# ------------------------------------------------------------
def generate_large_jobs(n=1000, seed=7):
    """
    Generate large dataset.

    Default:
        n = 1000

    Optional:
        n = 10000 for extended experiment

    Fixed seed:
        The same code always generates the same dataset.
    """
    random.seed(seed)

    jobs = []

    for job_number in range(1, n + 1):
        job = create_job(job_number)
        jobs.append(job)

    return jobs


# ------------------------------------------------------------
# Step 9. Validate generated dataset
# ------------------------------------------------------------
def validate_large_jobs(jobs):
    """
    Validate whether generated jobs satisfy the required conditions.

    Conditions:
        processing_time > 0
        5 <= processing_time <= 120
        0 <= arrival_time <= 500
        due_date > arrival_time
        due_date > arrival_time + processing_time
        1 <= priority_weight <= 5
        p_over_w_ratio = processing_time / priority_weight
    """
    for job in jobs:
        assert job["processing_time"] > 0, f"Invalid processing_time: {job}"
        assert 5 <= job["processing_time"] <= 120, f"processing_time out of range: {job}"
        assert 0 <= job["arrival_time"] <= 500, f"arrival_time out of range: {job}"
        assert job["due_date"] > job["arrival_time"], f"Invalid due_date: {job}"
        assert job["due_date"] > job["arrival_time"] + job["processing_time"], f"Invalid slack condition: {job}"
        assert 1 <= job["priority_weight"] <= 5, f"priority_weight out of range: {job}"

        expected_ratio = round(job["processing_time"] / job["priority_weight"], 2)
        assert job["p_over_w_ratio"] == expected_ratio, f"Invalid p_over_w_ratio: {job}"

    return True


# ------------------------------------------------------------
# Step 10. Create default large dataset
# ------------------------------------------------------------
large_jobs = generate_large_jobs(n=1000, seed=7)


# ------------------------------------------------------------
# Step 11. Print dataset when this file is executed directly
# ------------------------------------------------------------
if __name__ == "__main__":
    validate_large_jobs(large_jobs)

    print("Large dataset generated successfully.")
    print(f"Number of jobs: {len(large_jobs)}")
    print()

    print("First 10 jobs:")
    pprint(large_jobs[:10], sort_dicts=False)
    print()

    print("Last 5 jobs:")
    pprint(large_jobs[-5:], sort_dicts=False)
    print()

    # If you want to generate 10000 jobs, use the code below.
    # large_jobs_10000 = generate_large_jobs(n=10000, seed=7)
    # validate_large_jobs(large_jobs_10000)
    # print(f"Number of jobs: {len(large_jobs_10000)}")
