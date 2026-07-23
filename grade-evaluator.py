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
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if os.path.getsize(filename) == 0:
                print(f"{BG_RED}[ERROR]{RESET} The CSV file is empty. Please provide a CSV file with assignment data.")
                sys.exit(1)

            if reader.fieldnames is None:
                print(f"{BG_RED}[ERROR]{RESET} The CSV file is missing a header row. Please provide a valid CSV file.")
                sys.exit(1)
                
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"{BG_RED}[ERROR]{RESET} An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    print("\n--- Processing Grades ---")
    
    # TODOs: a) Check if all scores are percentage based (0-100)
    invalid_score_assignments = [];
    for index, assignment in enumerate(data):
        if not(0 <= assignment["score"] <= 100):
            invalid_score_assignments.append(assignment["assignment"])
            data.pop(index)
            print(f"{BG_YELLOW}[WARNING]{RESET} Assignment {assignment['assignment']} has the score {assignment['score']} and it's not in the range of 0-100. Therefore it has been excluded")

    if len(invalid_score_assignments) > 0:
        print("-" * 70)

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
        print(f"Available for resubmission: {", ".join(resubmission_assignments)}")
    else:
        print(f"Available for resubmission: None")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
