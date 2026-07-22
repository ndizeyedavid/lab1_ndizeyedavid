#!/usr/bin/python3
import csv
import sys
import os

BG_RED = "\033[41m"
BG_YELLOW = "\033[43m"
RESET = "\033[0m"
BG_GREEN = "\033[42m"

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    # filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    filename = "grades.csv"
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
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
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    print("\n--- Processing Grades ---")
    
    # TODOs: a) Check if all scores are percentage based (0-100)
    invalid_score_assignments = [];
    for index, assignment in enumerate(data):
        if 0 < assignment["score"] > 100:
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
            
    print(f"Total weight for Formatives: {weights["Formative"]}")
    print(f"Total weight for Summatives: {weights["Summative"]}")
    print(f"Total weight for all Assignments: {weights["total"]}")

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

    # TODO: c) Calculate the Final Grade and GPA
    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    # TODO: e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for resubmission.
    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options
    
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
