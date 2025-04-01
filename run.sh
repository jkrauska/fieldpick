#!/bin/bash +x

set -e
echo "############################################################################################"
echo "Running teams"
python3 fieldpick/create-teams.py 

echo "############################################################################################"
echo "Running calendar"
python3 fieldpick/create-calendar.py 


echo "Running picks"
echo "############################################################################################"
python3 fieldpick/pulpTeeBall.py

echo "############################################################################################"
python3 fieldpick/pulpFarmLower.py

echo "############################################################################################"
python3 fieldpick/pulpFarmUpper.py

echo "############################################################################################"
python3 fieldpick/pulpMajors.py

echo "############################################################################################"
python3 fieldpick/pulpMinorsAAA.py

echo "############################################################################################"
python3 fieldpick/pulpMinorsAA.py

echo "############################################################################################"
python3 fieldpick/pulpRookie.py

echo "############################################################################################"
python3 fieldpick/pulpChallenger.py

echo "############################################################################################"
python3 fieldpick/pulpJuniors.py

echo "############################################################################################"
python3 fieldpick/checks.py

echo "############################################################################################"
python3 fieldpick/publish.py

echo "############################################################################################"
python3 fieldpick/analysis.py 2>&1 | grep -v DEBUG


# python3 fieldpick/assign_fields.py 2>&1 | tee lastrun.log

# cp lastrun.log lastrun-$(date +%Y%m%d-%H%M%S).log

# python3 fieldpick/analysis.py 2>&1 