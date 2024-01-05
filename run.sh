#!/bin/bash +x

set -e
echo "############################################################################################"
echo "Running teams"
python fieldpick/create-teams.py 

echo "############################################################################################"
echo "Running calendar"
python fieldpick/create-calendar.py 


echo "Running picks"
echo "############################################################################################"
python fieldpick/pulpTeeBall.py

echo "############################################################################################"
python fieldpick/pulpFarmLower.py

echo "############################################################################################"
python fieldpick/pulpFarmUpper.py

echo "############################################################################################"
python fieldpick/pulpRookie.py


echo "############################################################################################"
python fieldpick/pulpMinorsAA.py

echo "############################################################################################"
python fieldpick/pulpMinorsAAA.py

echo "############################################################################################"
python fieldpick/pulpMajors.py

echo "############################################################################################"
python fieldpick/publish.py

echo "############################################################################################"
python fieldpick/analysis.py 2>&1 | grep -v DEBUG

exit

python fieldpick/assign_fields.py 2>&1 | tee lastrun.log

cp lastrun.log lastrun-$(date +%Y%m%d-%H%M%S).log

python fieldpick/analysis.py 2>&1 