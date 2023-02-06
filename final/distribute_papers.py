from itertools import product
from collections import defaultdict
import pulp as pl


"""
We want the paper distribution algo to:

- Be fast
- Avoid giving students their own paper DONE
- Prevent giving too many of one student to a specific student DONE
- Maximise information gleamed

There are n C 2 = n*(n-1) / 2. matchups.
That means if we want a complete picture we'll
have to assign each student around (n - 1)/2 pairs

If we were to assign every student every matchup (exculding their own).

Then they would be assigned (n*(n-1) / 2) - (n - 1) matchups.

"make it work, make it right, make it fast"
"""


def valid_match(match):
    grader, (p1, p2) = match
    return grader != p1 and grader != p2 

print("Starting model formulation...")

n = 101
students = range(n)

# We could load in pairs from a data file. 
# Since there will be less edges than the complete graph (what we are doing here)
# This will greatly reduce the model formulation/solving time!
pairs = list(pl.combination(students, 2))

all_assignments = filter(valid_match, product(students, pairs))

prob = pl.LpProblem("Paper_Distribution", pl.LpMinimize)

# Creating some dictionaries of decision variables for easy lookup
choices = {} # Lookup using (grader, p1, p2)

# These are defined to avoid redunant looping
# Contains all the valid assignments for a student 
student_assignments = defaultdict(list) 

# Contains all the possible pairs for a grader that contain another student
# For example student_contains[(0, 3)] = [0_(1,3), 0_(2,3), 0_(3,4), 0_(3,5)] 
student_contains = defaultdict(list) 

# Contains all the students a pair could be assigned to
pair_contains = defaultdict(list)

for asin in all_assignments:
    grader, (p1, p2) = asin
    var_name = f"{grader}-({p1},{p2})"
    var = pl.LpVariable(var_name, 0, 1, cat="Binary")

    choices[asin] = var
    student_assignments[grader].append(var)

    student_contains[(grader, p1)].append(var)
    student_contains[(grader, p2)].append(var)

    pair_contains[(p1, p2)].append(var)

for asins in pair_contains.values():    
    prob += pl.lpSum(asins) == 1

for i, grader_pair in enumerate(product(students, students)):
    g1, g2 = grader_pair
    if g1 == g2:
        continue
    
    sum1 = student_assignments[g1]
    sum2 = student_assignments[g2]

    abs_var = pl.LpVariable(f"abs_{i}", lowBound=0, cat="Integer")
    prob += abs_var >= pl.lpSum(sum1) - pl.lpSum(sum2)
    prob += abs_var >= pl.lpSum(sum2) - pl.lpSum(sum1)
    prob += abs_var <= 1

c = pl.LpVariable("c", lowBound=0, cat="Integer")
for asins in student_contains.values():
    prob += pl.lpSum(asins) <= c


#C is our objective function that we're trying to minimise
prob += c

print("Model formulation complete")
print("Starting model solving...")

# prob.solve(pl.PULP_CBC_CMD(msg=True, timeLimit=120))
# prob.solve(pl.GUROBI_CMD(msg=True, timeLimit=360))
prob.solve(pl.GUROBI_CMD(msg=True))

counter = defaultdict(int)
for k in choices:
    grader, (p1, p2) = k
    active = pl.value(choices[k]) == 1.0
    if active:
        print(k)
        counter[grader] += 1

print(counter.values())
print(f"The value of C is {pl.value(c)}")

