#!/bin/bash

time python fieldpick/create-teams.py && \
time python fieldpick/create-calendar.py && \
time python fieldpick/assign_fields.py