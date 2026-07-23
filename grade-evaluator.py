#!/usr/bin/python3
import csv
import sys
import os

BG_RED = "\033[41m"
BG_YELLOW = "\033[43m"
RESET = "\033[0m"
BG_GREEN = "\033[42m"

def load_csv_data():
    # filename = "grades.csv"
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ") or "grades.csv"
    
    if not os.path.exists(filename):
        print(f"{BG_RED}[ERROR]{RESET} The file '{filename}' was not found.")
        sys.exit(1)
        
    try:
        if os.path.getsize(filename) == 0:
            print(f"{BG_RED}[ERROR]{RESET} The CSV file is empty. Please provide a CSV file with assignment data.")
            sys.exit(1)
    except OSError as e:
        print(f"{BG_RED}[ERROR]{RESET} Could not access file '{filename}': {e}")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print(f"{BG_RED}[ERROR]{RESET} The CSV file is missing a header row. Please provide a valid CSV file.")
                sys.exit(1)

            headers = [header.strip().lower() for header in reader.fieldnames if header]
            required = {"assignment", "group", "score", "weight"}

            if not required.issubset(set(headers)):
                print(f"{BG_RED}[ERROR]{RESET} CSV is missing required columns. Expected headers: assignment, group, score, weight")
                sys.exit(1)

            bad_rows = 0
            for row_num, row in enumerate(reader, start=2):
                single_row = {
                    (header.strip().lower() if header else header): (value or "").strip()
                    for header, value in row.items()
                }

                assignment_name = single_row.get("assignment", "")
                group = single_row.get("group", "")
                score_s = single_row.get("score", "")
                weight_s = single_row.get("weight", "")

                if not assignment_name or not group or score_s == "" or weight_s == "":
                    print(f"{BG_YELLOW}[WARNING]{RESET} Row {row_num} has missing fields — skipping.")
                    bad_rows += 1
                    continue

                try:
                    score = float(score_s)
                    weight = float(weight_s)
                except ValueError:
                    print(f"{BG_YELLOW}[WARNING]{RESET} Row {row_num} has non-numeric score/weight — skipping.")
                    bad_rows += 1
                    continue

                assignments.append({
                    'assignment': assignment_name,
                    'group': group,
                    'score': score,
                    'weight': weight
                })

            if bad_rows > 0:
                print(f"{BG_YELLOW}[WARNING]{RESET} Skipped {bad_rows} bad row(s).")

        return assignments
    except Exception as e:
        print(f"{BG_RED}[ERROR]{RESET} An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    print("\n--- Processing Grades ---")
    
    # TODOs: a) Check if all scores are percentage based (0-100)
    valid_data = []
    invalid_score_assignments = []
    for assignment in data:
        if 0 <= assignment["score"] <= 100:
            valid_data.append(assignment)
        else:
            invalid_score_assignments.append((assignment["assignment"], assignment["score"]))

    if invalid_score_assignments:
        for name, score in invalid_score_assignments:
            print(f"{BG_YELLOW}[WARNING]{RESET} Assignment '{name}' has score {score} (outside 0-100) and was excluded.")
        print("-" * 70)

    data = valid_data

    if not data:
        print(f"{BG_RED}[ERROR]{RESET} No assignments remain after filtering invalid scores.")
        sys.exit(1)

    # TODOs: b) Validate total weights (Total=100, Summative=40, Formative=60)
    weights = {"total": 0.0, "Formative": 0.0, "Summative": 0.0}
    for assignment in data:
        weights["total"] += assignment["weight"]

        if assignment["group"] == "Formative":
            weights["Formative"] += assignment["weight"]
        elif assignment["group"] == "Summative":
            weights["Summative"] += assignment["weight"]
            
    print(f"Total weight for Formatives: {int(weights["Formative"])}/60")
    print(f"Total weight for Summatives: {int(weights["Summative"])}/40")
    print(f"Total weight for all Assignments: {int(weights["total"])}/100")

    if weights["Formative"] != 60:
        print(f"{BG_RED}ERROR{RESET} This Formative weights are NOT well calibrated")
        sys.exit(1)
    elif weights["Summative"] != 40:
        print(f"{BG_RED}ERROR{RESET} This Summative weights are NOT well calibrated")
        sys.exit(1)
    elif weights["total"] != 100:
        print(f"{BG_RED}ERROR{RESET} This assignment's weights are NOT well calibrated")
        sys.exit(1)
    else:
        print(f"{BG_GREEN}ALL WEIGHTS ARE PERFECTLY CALLIBRATED{RESET}")
        print("-" * 70)

    # TODOs: c) Calculate the Final Grade and GPA
    total_grade = 0
    for assignment in data:
        total_grade += (assignment["score"] * assignment["weight"]) / 100
    GPA = (total_grade / 100) * 5.0

    print(f"Final GPA = {round(GPA, 4)}")
    print("-" * 70)

    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    scores = {"Formative": 0.0, "Summative": 0.0}
    for assignment in data:
        if assignment["group"] == "Formative":
            scores["Formative"] += (assignment["score"] * assignment["weight"]) / 100
        else:
            scores["Summative"] += (assignment["score"] * assignment["weight"]) / 100

    
    percentage_formative = (scores["Formative"] * 100) / 60
    percentage_summative = (scores["Summative"] * 100) / 40
    if  percentage_formative >= 50 and percentage_summative >= 50:
        status = "Pass"
    else:
        status = "Fail"
        
    print(f"Formative(60): {round(scores['Formative'], 2)}")
    print(f"Summative(40): {round(scores['Summative'], 2)}")
    print("-" * 70)
    
    # TODO: e) Check for failed formative assignments (< 50%) and determine which one(s) have the highest weight for resubmission.
    resubmission_assignments = []
    # if percentage_formative < 50:
    low_scored_assignments = []
    individual_weights = []

    for assignment in data:
        if assignment["group"] == "Formative" and assignment["score"] < 50:
            individual_weights.append(assignment["weight"])
            low_scored_assignments.append(assignment)

    if individual_weights:
        highest_weight = max(individual_weights)

        for assignment in low_scored_assignments:
            if assignment["weight"] == highest_weight:
                resubmission_assignments.append(assignment["assignment"])

    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options
    if status == "Pass":
        print(f"Status: {BG_GREEN}PASSED{RESET}")
    else:
        print(f"Status: {BG_RED}FAILED{RESET}")

    if len(resubmission_assignments) > 0:
        print(f"Available for resubmission: {', '.join(resubmission_assignments)}")
    else:
        print(f"Available for resubmission: None")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
