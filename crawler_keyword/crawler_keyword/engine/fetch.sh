#!/bin/bash

cd $(dirname $0)

logging="logging"

if [ ! -d "$logging" ]; then
    mkdir $logging
fi

now=$(date +"%d/%m/%Y")
logging_filename=$(date +"%d_%m-%Y_%T")
filename="$logging/$logging_filename.txt"
python3 job_v1.py $now $now > $filename