#!/bin/bash

$1 &
PID=$!
sleep 1s
if ps -p $PID > /dev/null
then
   python3 ./main.py --input customers.csv --send_url http://localhost:9090
   kill $PID
   wait
   echo "Process finished"
   # Do something knowing the pid exists, i.e. the process with $PID is running
else
   echo "Process didn't start"
fig