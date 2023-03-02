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

n = 33
classroom = Classroom(n, malicious=False)
real = classroom.get_true_ranking()
tourney_generator = TournamentGenerator(classroom)
print(f"real: {real}")


fields = ["Num papers", "RBTL", "BTL", "KEMENY", "BORDA"]
rows = []

for papers in range(1, n):
    print(f"running tourney with {n} students and ~{papers} matchups to mark each")
    pairs = connected_graph(n, papers)
    distributor = dp.PaperDistributor(n, pairs)
    assignments = distributor.get_solution()
    tourney_generator.generate_tournament(assignments)
    tourney = tourney_generator.get_results()

    t1 = rbtl(tourney)
    print(f"rbtl: {t1}")
    t2 = btl(tourney)
    print(f" btl: {t2}")
    t3 = kemeny(tourney)
    print(f"keme: {t3}")
    t4 = copeland(tourney)
    print(f"cope: {t4}")

    kt1 = kendall_tau(real, t1)
    print(f"The distance between the true ranking and the rbtl ranking is: {kt1}")
    kt2 = kendall_tau(real, t2)
    print(f"The distance between the true ranking and the btl ranking is: {kt2}")
    kt3 = kendall_tau(real, t3)
    print(f"The distance between the true ranking and the kemeny ranking is: {kt3}")
    kt4 = kendall_tau(real, t4)
    print(f"The distance between the true ranking and the copeland ranking is: {kt4}")

    print(f"The average grade of the class was {classroom.avg_grade()}")

    k = [(kt1, "rbtl"), (kt2, "btl"), (kt3, "kemeny"), (kt4, "copeland")]
    k.sort(key=lambda v: v[0])
    print(" > ".join([v[1] for v in k]))
    rows.append([str(k) for k in [papers, kt1, kt2, kt3, kt4]])

with open("data4.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
