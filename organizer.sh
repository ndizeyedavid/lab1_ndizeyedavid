#!/bin/bash
log_timestamp=$(date +"%F - %H:%M:%S")

echo "$log_timestamp Starting the Archiving process" >> organizer.log

if [ ! -f "grades.csv" ]; then
    echo "[ERROR] The grades file is MISSING"
    exit 1
fi

if [ ! -d "archive" ]; then
    echo "$log_timestamp Creating the archive directory" >> organizer.log
    
    echo "Archive Directory Is not present. Creating it now.....";
    mkdir "archive"
    sleep 1
    echo "[OK] Archive dir created successfully"
else
    echo "[OK] The archive directory arleady exists. Archiving instead";
fi

echo "$log_timestamp Recording the current Timestamp" >> organizer.log

timestamp=$(date +"%Y%m%d-%H%M%S")
echo "[OK] Timestamp Recorded"

echo "$log_timestamp Archived grades.csv to grades-$timestamp.csv" >> organizer.log
mv "./grades.csv" "./archive/grades_$timestamp.csv"
echo "[OK] grades.csv file successfully archived(grades-$timestamp.csv)"

echo "$log_timestamp New grades.csv file initiated" >> organizer.log
touch "./grades.csv"
echo "[OK] New grades.csv file created..."

echo "$log_timestamp Archiving completed" >> organizer.log
echo "" >> organizer.log
