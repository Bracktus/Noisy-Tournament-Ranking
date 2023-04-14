import sys

sys.path.append("..")

import csv
from tourney_runner import run_iterative_tourney
from metrics import kendall_tau
from classroom import Classroom
import distribute_papers as dp
import rankers as rk
from graph_utils import fair_graph
from generate_tourney import TournamentGenerator

n = 30
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
    "WEIGHTED BORDA",
    "WIN COUNT",
    "ITER RBLT",
    "ITER BTL",
    "ITER KEMENY",
    "ITER BORDA",
    "ITER WEIGHTED BORDA",
    "ITER WIN COUNT",
]

rows = []

for papers_each in range(1, n):
    print(f"running tourney with {n} students and ~{papers_each} matchups to mark each")
    pairs = fair_graph(n, papers_each*n)
    distributor = dp.PaperDistributor(n, pairs)
    assignments = distributor.get_solution()
    print(f"real: {real}")

    # --- Iterative tournies --------

    it_count = run_iterative_tourney(n, papers_each, rk.win_count, tourney_generator)
    print(f"iter  count: \t{it_count}")

    it_borda = run_iterative_tourney(n, papers_each, rk.copeland, tourney_generator)
    print(f"iter borda: \t{it_borda}")

    it_weight_borda = run_iterative_tourney(n, papers_each, rk.weighted_borda, tourney_generator)
    print(f"iter w_borda: \t{it_weight_borda}")

    it_kemeny = run_iterative_tourney(n, papers_each, rk.kemeny, tourney_generator)
    print(f"iter kem: \t{it_kemeny}")

    it_btl = run_iterative_tourney(n, papers_each, rk.btl, tourney_generator)
    print(f"iter  btl: \t{it_btl}")

    it_rbtl = run_iterative_tourney(n, papers_each, rk.rbtl, tourney_generator)
    print(f"iter rbtl: \t{it_rbtl}")

    # --- Non-iterative tournies -----
    tourney = tourney_generator.generate_tournament(assignments)

    nit_count = rk.win_count(tourney)
    print(f"count \t{nit_count}")
    
    nit_borda = rk.copeland(tourney)
    print(f"borda: \t{nit_borda}")

    nit_weight_borda = rk.weighted_borda(tourney)
    print(f"w_borda: \t{nit_weight_borda}")

    nit_kemeny = rk.kemeny(tourney)
    print(f"kem: \t{nit_kemeny}")

    nit_btl = rk.btl(tourney)
    print(f"btl: \t{nit_btl}")

    nit_rbtl = rk.rbtl(tourney)
    print(f"rbtl: \t{nit_rbtl}")

    kt_it_count = kendall_tau(real, it_count)
    print(f"The distance between the true ranking and the iterative win count ranking is: {kt_it_count}")

    kt_it_borda = kendall_tau(real, it_borda)
    print(f"The distance between the true ranking and the iterative borda is: {kt_it_borda}")

    kt_it_w_borda = kendall_tau(real, it_weight_borda)
    print(f"The distance between the true ranking and the iterative w borda is: {kt_it_w_borda}")

    kt_it_kem = kendall_tau(real, it_kemeny)
    print(f"The distance between the true ranking and the iterative kemeny is: {kt_it_kem}")

    kt_it_btl = kendall_tau(real, it_btl)
    print(f"The distance between the true ranking and the iterative btl is: {kt_it_btl}")

    kt_it_rbtl = kendall_tau(real, it_rbtl)
    print(f"The distance between the true ranking and the iterative rbtl is: {kt_it_rbtl}")

    kt_nit_count = kendall_tau(real, nit_count)
    print(f"The distance between the true ranking and the non iter win count is: {kt_nit_count}")

    kt_nit_borda = kendall_tau(real, nit_borda)
    print(f"The distance between the true ranking and the non iter borda is: {kt_nit_borda}")

    kt_nit_w_borda = kendall_tau(real, nit_weight_borda)
    print(f"The distance between the true ranking and the non iter w borda is: {kt_nit_w_borda}")

    kt_nit_kem = kendall_tau(real, nit_kemeny)
    print(f"The distance between the true ranking and the non iter kemen is: {kt_nit_kem}")

    kt_nit_btl = kendall_tau(real, nit_btl)
    print(f"The distance between the true ranking and the non iter btl is: {kt_nit_btl}")

    kt_nit_rbtl = kendall_tau(real, nit_rbtl)
    print(f"The distance between the true ranking and the non iter rbtl is: {kt_nit_rbtl}")

    print(f"The average grade of the class was {classroom.avg_grade()}")

    k = [
        (kt_nit_rbtl, "rbtl"),
        (kt_nit_btl, "btl"),
        (kt_nit_kem, "kemeny"),
        (kt_nit_borda, "borda"),
        (kt_nit_w_borda, "weighted_borda"),
        (kt_nit_count, "win_count"),
        (kt_it_rbtl, "iter rbtl"),
        (kt_it_btl, "iter btl"),
        (kt_it_kem, "iter kemeny"),
        (kt_it_borda, "iter borda"),
        (kt_it_w_borda, "iter weighted_borda"),
        (kt_it_count, "iter win_count")
    ]
    rows.append([papers_each]+ [i[0] for i in k])
    k.sort(key=lambda v: v[0])
    print(" > ".join([v[1] for v in k]))

with open(f"n={n}_regular.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
