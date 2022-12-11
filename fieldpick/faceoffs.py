#!/usr/bin/env python3

from collections import deque
from itertools import islice

# Round robin scheduling
# https://stackoverflow.com/questions/32358841/grouping-list-combinations-for-round-robin-tournament
# itertools.combinations returns the right set of matchups, but in a unusable order
def fixtures(teams):
    # Fix odd numbered teams
    if len(teams) % 2:
        teams.append("Bye")

    ln = len(teams) // 2
    dq1, dq2 = deque(islice(teams, None, ln)), deque(islice(teams, ln, None))
    for _ in range(len(teams)-1):
        yield zip(dq1, dq2) # list(zip.. python3
        #  pop off first deque's left element to
        # "fix one of the competitors in the first column"
        start = dq1.popleft()
        # rotate the others clockwise one position
        # by swapping elements
        dq1.appendleft(dq2.popleft())
        dq2.append(dq1.pop())
        # reattach first competitor
        dq1.appendleft(start)

# Break up the groupings as we aren't doing a tournament
def faceoffs(teams):
    output = []
    for group in fixtures(teams):
        for faceoff in group:
            output.append(faceoff)
    return(output)

# Repeating cycle of faceoffs when # games > faceoffs
def faceoffs_repeated(teams, games=None):
    cycle=faceoffs(teams)
    if games:
        cycles = cycle * (games // len(cycle) + 1)
        return(cycles[:games])
    else:
        return(cycle)

if __name__ == "__main__":
    print('Demo of faceoffs function')
    teams = list(range(1,7))
    teams = ['Team 1', 'Team 2', 'Team 3', 'Team 4', 'Team 5', 'Team 6']
    print(f"Teams: {teams}")
    print(f"Faceoffs: {faceoffs(teams)}")
