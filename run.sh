#!/bin/bash +x

time python fieldpick/create-teams.py && \
time python fieldpick/create-calendar.py && \
time python fieldpick/assign_fields.py 2>&1 | tee lastrun.log

cp lastrun.log lastrun-$(date +%Y%m%d-%H%M%S).log

time python fieldpick/analysis.py 2>&1 