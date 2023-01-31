#!/bin/bash +x

python fieldpick/create-teams.py && \
python fieldpick/create-calendar.py && \
python fieldpick/assign_fields.py 2>&1 | tee lastrun.log

cp lastrun.log lastrun-$(date +%Y%m%d-%H%M%S).log

python fieldpick/analysis.py 2>&1 