#!/bin/bash

if [ ! -d "archive" ]; then
    echo "Archive Directory Is not present. Creating it now.....";
    mkdir "archive"
else
    echo "The archive directory arleady exists. Archiving instead";
fi
