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
have to assign each student (n - 1)/2 pairs

If we were to assign every student every matchup (exculding their own).

Then they would be assigned (n*(n-1) / 2) - (n - 1) matchups.

"make it work, make it right, make it fast"
"""


def valid_match(match):
    grader, (p1, p2) = match
    return grader != p1 and grader != p2 


n = 30
students = range(n)
pairs = list(pl.combination(students, 2))
all_assignments = filter(valid_match, product(students, pairs))

prob = pl.LpProblem("Paper_Distribution", pl.LpMinimize)

# Creating some dictionaries of decision variables for easy lookup
choices = {} # Lookup using (grader, p1, p2)

# These are defined to avoid redunant looping
# Contains all the valid assingments for a student 
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


c = pl.LpVariable("c", lowBound=0, cat="Integer")
for asins in student_contains.values():
    prob += pl.lpSum(asins) <= c

for asins in pair_contains.values():    
    prob += pl.lpSum(asins) == 1

sums = [student_assignments[grader] for grader in students]
abs_vars = []
for i, sum_pair in enumerate(product(sums, sums)):
    sum1, sum2 = sum_pair

    abs_var = pl.LpVariable(f"abs_{i}", lowBound=0, cat="Integer")
    prob += abs_var >= pl.lpSum(sum1) - pl.lpSum(sum2)
    prob += abs_var >= pl.lpSum(sum2) - pl.lpSum(sum1)
    prob += abs_var <= 1
    abs_vars.append(abs_var)

#C is our objective function that we're trying to minimise
prob += c

# prob.solve(pl.PULP_CBC_CMD(msg=True, timeLimit=120))
prob.solve(pl.GUROBI_CMD(msg=True, timeLimit=120))

counter = defaultdict(int)
for k in choices:
    grader, (p1, p2) = k
    active = pl.value(choices[k]) == 1.0
    if active:
        print(k)
        counter[grader] += 1

print(counter.values())
print(f"The value of C is {pl.value(c)}")

