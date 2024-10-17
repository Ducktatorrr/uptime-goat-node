#!/bin/bash

# Run both scripts in the background, redirecting output
python goat_report.py & 
python endpoint_agent.py &

# Wait for all background processes to finish
wait
