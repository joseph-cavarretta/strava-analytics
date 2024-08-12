#!/bin/bash
python3 /app/etl/process_activities.py refresh
python3 /app/etl/load_activities.py