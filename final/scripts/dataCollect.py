import sys

sys.path.append("..")

import csv
from tourney_runner import run_iterative_tourney
from metrics import kendall_tau
from rankers import rbtl, btl, kemeny, copeland
from classroom import Classroom
import distribute_papers as dp
from graph_utils import connected_graph
from generate_tourney import TournamentGenerator

n = 22
classroom = Classroom(n, malicious=False)
real = classroom.get_true_ranking()
tourney_generator = TournamentGenerator(classroom)
print(f"real: {real}")


fields = [
    "Num papers",
    "RBTL",
    "BTL",
    "KEMENY",
    "BORDA",
    "ITER RBLT",
    "ITER BTL",
    "ITER KEMENY",
    "ITER BORDA",
]
rows = []

for papers in range(1, n):
    print(f"running tourney with {n} students and ~{papers} matchups to mark each")
    pairs = connected_graph(n, papers)
    distributor = dp.PaperDistributor(n, pairs)
    assignments = distributor.get_solution()

    # --- Iterative tournies --------
    it1 = run_iterative_tourney(n, papers - 1, rbtl, tourney_generator)
    tourney_generator.reset_iter_tourney()

    it2 = run_iterative_tourney(n, papers - 1, btl, tourney_generator)
    tourney_generator.reset_iter_tourney()

    it3 = run_iterative_tourney(n, papers - 1, copeland, tourney_generator)
    tourney_generator.reset_iter_tourney()

    it4 = run_iterative_tourney(n, papers - 1, kemeny, tourney_generator)
    tourney_generator.reset_iter_tourney()

    # --- Non-iterative tournies -----
    tourney = tourney_generator.generate_tournament(assignments)
    t1 = rbtl(tourney)
    print(f"rbtl: \t{t1}")

    t2 = btl(tourney)
    print(f" btl: \t{t2}")

    t3 = kemeny(tourney)
    print(f"keme: \t{t3}")

    t4 = copeland(tourney)
    print(f"cope: \t{t4}")

    print(f"iter rbtl: \t{it1}")
    print(f"iter  btl: \t{it2}")
    print(f"iter keme: \t{it3}")
    print(f"iter cope: \t{it4}")

    kt1 = kendall_tau(real, t1)
    print(f"The distance between the true ranking and the rbtl ranking is: {kt1}")

    kt2 = kendall_tau(real, t2)
    print(f"The distance between the true ranking and the btl ranking is: {kt2}")

    kt3 = kendall_tau(real, t3)
    print(f"The distance between the true ranking and the kemeny ranking is: {kt3}")

    kt4 = kendall_tau(real, t4)
    print(f"The distance between the true ranking and the copeland ranking is: {kt4}")

    ikt1 = kendall_tau(real, it1)
    print(f"The distance between the true ranking and the iter rblt ranking is: {ikt1}")
    ikt2 = kendall_tau(real, it2)
    print(f"The distance between the true ranking and the iter btl ranking is: {ikt2}")
    ikt3 = kendall_tau(real, it3)
    print(
        f"The distance between the true ranking and the iter kemeny ranking is: {ikt3}"
    )
    ikt4 = kendall_tau(real, it4)
    print(
        f"The distance between the true ranking and the iter copeland ranking is: {ikt4}"
    )

    print(f"The average grade of the class was {classroom.avg_grade()}")

    k = [
        (kt1, "rbtl"),
        (kt2, "btl"),
        (kt3, "kemeny"),
        (kt4, "copeland"),
        (ikt1, "iter rblt"),
        (ikt2, "iter btl"),
        (ikt3, "iter kemeny"),
        (ikt4, "iter borda"),
    ]
    k.sort(key=lambda v: v[0])
    print(" > ".join([v[1] for v in k]))
    rows.append([str(k) for k in [papers, kt1, kt2, kt3, kt4, ikt1, ikt2, ikt3, ikt4]])

print(f"real: {real}")
with open(f"n={n}_regular.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
