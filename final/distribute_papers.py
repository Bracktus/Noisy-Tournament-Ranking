from itertools import product
from collections import defaultdict
import pulp as pl


"""
We want the paper distribution algo to:

- Be fast
- Avoid giving students their own paper DONE
- Prevent giving too many of one student to a specific student DONE
- Keep the number of papers each student marks fairly even DONE
- Maximise information gleamed

There are n C 2 = n*(n-1) / 2. matchups.
That means if we want a complete picture we'll
have to assign each student around (n - 1)/2 pairs

If we were to assign every student every matchup (exculding their own).

Then they would be assigned (n*(n-1) / 2) - (n - 1) matchups.

"make it work, make it right, make it fast"
"""
class PaperDistibutor():
    def __init__(self, n, pairs=None):
        self.prob = pl.LpProblem("Paper_Distribution", pl.LpMinimize)
        self.formulated = False
        self.solved = False
        self.students = range(n)
        if pairs != None:
            self.pairs = pairs
        else:
            # If there aren't a list of pairs, then we just select all of them
            self.pairs = list(pl.combination(self.students, 2))
        self.choices = {} # This will contain our decision variables

    def formulate_model(self):
        print("Formulating model...")

        valid_match = lambda m : m[0] != m[1] and m[0] != m[1]
        all_assignments = filter(valid_match, product(self.students, self.pairs))

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

            self.choices[asin] = var
            student_assignments[grader].append(var)

            student_contains[(grader, p1)].append(var)
            student_contains[(grader, p2)].append(var)

            pair_contains[(p1, p2)].append(var)

        for asins in pair_contains.values():    
            # Each pair is only assigned once
            self.prob += pl.lpSum(asins) == 1

        for i, grader_pair in enumerate(product(self.students, self.students)):
            # Every student is assigned a number of papers.
            # The difference in the number of papers assigned to each student
            # must not differ by more than 1

            # For example [a:5, b:5, c:3] is invalid since 5 - 3 =2
            # but [a:5, b:5, c:4] is valid
            g1, g2 = grader_pair
            if g1 == g2:
                continue
            
            sum1 = student_assignments[g1]
            sum2 = student_assignments[g2]

            abs_var = pl.LpVariable(f"abs_{i}", lowBound=0, cat="Integer")
            self.prob += abs_var >= pl.lpSum(sum1) - pl.lpSum(sum2)
            self.prob += abs_var >= pl.lpSum(sum2) - pl.lpSum(sum1)
            self.prob += abs_var <= 1

        c = pl.LpVariable("c", lowBound=0, cat="Integer")
        for asins in student_contains.values():
            self.prob += pl.lpSum(asins) <= c

        #C is our objective function that we're trying to minimise
        self.prob += c
        self.formulated = True
        print("Model formulated")

    def solve(self, show_msg=False):
        if not self.formulated:
            raise AttributeError("Model is not formulated")

        print("Solving model...")
        self.prob.solve(pl.GUROBI_CMD(msg=show_msg))
        self.solved = True
        print("Model solved")

    def print_solution(self):
        if not self.solved:
            raise AttributeError("Model is not solved")

        for c in self.choices:
            grader, (p1, p2) = c
            active = pl.value(self.choices[c]) == 1.0
            if active:
                print(f"{grader}: ({p1}, {p2})")

    def get_solution(self):
        if not self.solved:
            raise AttributeError("Model is not solved")

        solution_dict = defaultdict(list)
        for c in self.choices:
            grader, (p1, p2) = c
            active = pl.value(self.choices[c]) == 1.0
            if active:
                solution_dict[grader].append((p1, p2))

        return solution_dict


distributor = PaperDistibutor(30)
distributor.formulate_model()
distributor.solve(show_msg=True)
distributor.print_solution()
