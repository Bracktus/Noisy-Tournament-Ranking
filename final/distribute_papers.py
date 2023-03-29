from itertools import product
from collections import defaultdict
import pulp as pl

class PaperDistributor:
    def __init__(self, n, pairs=None):
        self.prob = pl.LpProblem("Paper_Distribution", pl.LpMinimize)
        self.formulated = False
        self.solved = False
        self.students = range(n)
        if pairs != None:
            self.pairs = pairs
        else:
            # If there aren't a list of pairs, then we just select all of them
            self.pairs = pl.combination(self.students, 2)
        self.choices = {}  # This will contain our decision variables

    def _formulate_model(self):
        valid_match = lambda m: m[0] != m[1][0] and m[0] != m[1][1]
        all_assignments = filter(valid_match, product(self.students, self.pairs))

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
            # self.prob += pl.lpSum(asins) >= 1
            self.prob += pl.lpSum(asins) == 1

        grader_pairs = pl.combination(self.students, 2)
        for i, (grader_1, grader_2) in enumerate(grader_pairs):
            # Every student is assigned a number of papers.
            # The difference in the number of papers assigned to each student
            # must not differ by more than 1
            # For example [a:5, b:5, c:3] is invalid since 5 - 3 = 2
            # but [a:5, b:5, c:4] is valid

            sum1 = student_assignments[grader_1]
            sum2 = student_assignments[grader_2]

            abs_var = pl.LpVariable(f"abs_{i}", lowBound=0, cat="Integer")
            self.prob += abs_var >= pl.lpSum(sum1) - pl.lpSum(sum2)
            self.prob += abs_var >= pl.lpSum(sum2) - pl.lpSum(sum1)
            self.prob += abs_var <= 1

        c = pl.LpVariable("c", lowBound=0, cat="Integer")
        for asins in student_contains.values():
            # Every student marks an amount of another student's paper.
            # For example for the assignment:
            # a:[(b,c), (c, d)]
            # (a,b) = 1, (a,c) = 2 and (a,d) = 1 since a marks c's paper twice
            # So here were looping over all such combinations and setting c to be the maximum of these values
            self.prob += pl.lpSum(asins) <= c

        # C is our objective function that we're trying to minimise
        self.prob += c
        self.formulated = True

    def _solve(self, show_msg=False):
        if not self.formulated:
            self._formulate_model()

        self.prob.solve(pl.GUROBI_CMD(msg=show_msg))
        self.solved = True

    def print_solution(self):
        if not self.solved:
            self._solve()

        for c in self.choices:
            grader, (p1, p2) = c
            active = pl.value(self.choices[c]) == 1.0
            if active:
                print(f"{grader}: ({p1}, {p2})")

    def get_solution(self):
        if not self.solved:
            self._solve()

        solution_dict = defaultdict(list)
        for c in self.choices:
            grader, (p1, p2) = c
            active = pl.value(self.choices[c]) == 1.0
            if active:
                solution_dict[grader].append((p1, p2))

        return solution_dict


class IterativePaperDistributor:
    def __init__(self, n, ranking, pairs, past_tourneys):
        self.students = range(n)
        self.ranking = ranking
        self.pairs = pairs
        self.past_tourneys = past_tourneys

        self.choices = {}
        self.prob = pl.LpProblem("Paper_Distribution", pl.LpMinimize)

        self.player_indexes = self._update_player_indexes()

        self.solved = False
        self.formulated = False

    def _update_player_indexes(self):
        cache = {}
        for idx, p in enumerate(self.ranking):
            cache[p] = idx
        return cache

    def _formulate_model(self):
        def valid_match(m):
            grader, (p1, p2) = m
            diff = grader != p1 and grader != p2
            unseen1 = (p1, p2) not in self.past_tourneys[grader]
            unseen2 = (p2, p1) not in self.past_tourneys[grader]

            return diff and unseen1 and unseen2

        all_assignments = filter(valid_match, product(self.students, self.pairs))

        # Contains all the students a pair could be assigned to
        pair_contains = defaultdict(list)

        # Contains all the valid assignments for a student
        student_assignments = defaultdict(list)

        for asin in all_assignments:
            grader, (p1, p2) = asin
            var_name = f"{grader}-({p1},{p2})"
            var = pl.LpVariable(var_name, 0, 1, cat="Binary")

            pair_contains[(p1, p2)].append(var)
            student_assignments[grader].append(var)
            self.choices[asin] = var

        for asins in pair_contains.values():
            # Each pair is only assigned once
            self.prob += pl.lpSum(asins) == 1
            # self.prob += pl.lpSum(asins) >= 1

        grader_pairs = pl.combination(self.students, 2)
        for i, (grader_1, grader_2) in enumerate(grader_pairs):
            # Every student is assigned a number of papers.
            # The difference in the number of papers assigned to each student
            # must not differ by more than 1
            # For example [a:5, b:5, c:3] is invalid since 5 - 3 = 2
            # but [a:5, b:5, c:4] is valid

            sum1 = student_assignments[grader_1]
            sum2 = student_assignments[grader_2]

            abs_var = pl.LpVariable(f"abs_{i}", lowBound=0, cat="Integer")
            self.prob += abs_var >= pl.lpSum(sum1) - pl.lpSum(sum2)
            self.prob += abs_var >= pl.lpSum(sum2) - pl.lpSum(sum1)
            self.prob += abs_var <= 1

        obj_arr = []
        for asin in all_assignments:
            # Every student is given a score from their ranking
            # Every pair is given an uncertainty rating

            # Give the strongest players the most uncertain matchups
            grader, (p1, p2) = asin
            uncertainty = self.calc_uncert(p1, p2)
            skill = self.calc_skill(grader)

            var_name = f"abs_{grader},{p1},{p2}"
            abs_var = pl.LpVariable(var_name, lowBound=0, cat="Integer")
            obj_arr.append(self.choices[asin] * abs(uncertainty - skill))

        self.prob += pl.lpSum(obj_arr)

    def _solve(self, show_msg=False):
        if not self.formulated:
            self._formulate_model()

        self.prob.solve(pl.GUROBI_CMD(msg=show_msg))
        self.solved = True

    def get_solution(self):
        """Obtains a tournament from the MIP model"""
        if not self.solved:
            self._solve()

        solution_dict = defaultdict(list)
        for c in self.choices:
            grader, (p1, p2) = c
            active = pl.value(self.choices[c]) == 1.0
            if active:
                solution_dict[grader].append((p1, p2))

        return solution_dict

    def print_solution(self):
        if not self.solved:
            self._solve()

        for c in self.choices:
            grader, (p1, p2) = c
            active = pl.value(self.choices[c]) == 1.0
            if active:
                print(f"{grader}: ({p1}, {p2})")

    def calc_uncert(self, p1, p2):
        i1 = self.player_indexes[p1]
        i2 = self.player_indexes[p2]

        n = len(self.students)
        return abs(i1 - i2) / n

    def calc_skill(self, student):
        idx = self.player_indexes[student]
        n = len(self.students)
        return (n - idx) / n
