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

n = 20
classroom = Classroom(n, malicious=False)
real = classroom.get_true_ranking()
tourney_generator = TournamentGenerator(classroom)
print(f"real: {real}")


fields = [
    "Num matches",
    "Constrained RBTL",
    "Constrained BTL",
    "Constrained KEMENY",
    "Constrained BORDA",
    "Constrained WEIGHTED BORDA",
    "Constrained WIN COUNT",
    "Unconstrained RBLT",
    "Unconstrained BTL",
    "Unconstrained KEMENY",
    "Unconstrained BORDA",
    "Unconstrained WEIGHTED BORDA",
    "Unconstrained WIN COUNT",
]

rows = []
total = int(n * (n - 1) * (0.5))

for papers in range(n, total, 5):
    print(f"running tourney with {n} students and ~{papers} matchups total to mark")
    pairs = fair_graph(n, papers)

    distributor_good = dp.PaperDistributor(n, pairs, toggle=False)
    distributor_bad = dp.PaperDistributor(n, pairs, toggle=True)

    assignments_good = distributor_good.get_solution()
    assignments_bad = distributor_bad.get_solution()
    print(f"real: {real}")

    # --- Iterative tournies --------

    # it_count = run_iterative_tourney(n, papers_each, rk.win_count, tourney_generator)
    # print(f"iter  count: \t{it_count}")

    # it_borda = run_iterative_tourney(n, papers_each, rk.copeland, tourney_generator)
    # print(f"iter borda: \t{it_borda}")

    # it_weight_borda = run_iterative_tourney(n, papers_each, rk.weighted_borda, tourney_generator)
    # print(f"iter w_borda: \t{it_weight_borda}")

    # it_kemeny = run_iterative_tourney(n, papers_each, rk.kemeny, tourney_generator)
    # print(f"iter kem: \t{it_kemeny}")

    # it_btl = run_iterative_tourney(n, papers_each, rk.btl, tourney_generator)
    # print(f"iter  btl: \t{it_btl}")

    # it_rbtl = run_iterative_tourney(n, papers_each, rk.rbtl, tourney_generator)
    # print(f"iter rbtl: \t{it_rbtl}")

    # --- Non-iterative tournies -----
    tourney_good = tourney_generator.generate_tournament(assignments_good)
    tourney_bad = tourney_generator.generate_tournament(assignments_bad)

    good_count = rk.win_count(tourney_good)
    print(f"g count \t{good_count}")

    good_borda = rk.copeland(tourney_good)
    print(f"g borda: \t{good_borda}")

    good_weight_borda = rk.weighted_borda(tourney_good)
    print(f"g w_borda: \t{good_weight_borda}")

    good_kemeny = rk.kemeny(tourney_good)
    print(f"g kem: \t{good_kemeny}")

    good_btl = rk.btl(tourney_good)
    print(f"g btl: \t{good_btl}")

    good_rbtl = rk.rbtl(tourney_good)
    print(f"g rbtl: \t{good_rbtl}")

    bad_count = rk.win_count(tourney_bad)
    print(f"b count \t{bad_count}")

    bad_borda = rk.copeland(tourney_bad)
    print(f"b borda: \t{bad_borda}")

    bad_weight_borda = rk.weighted_borda(tourney_bad)
    print(f"b w_borda: \t{bad_weight_borda}")

    bad_kemeny = rk.kemeny(tourney_bad)
    print(f"b kem: \t{bad_kemeny}")

    bad_btl = rk.btl(tourney_bad)
    print(f"b btl: \t{bad_btl}")

    bad_rbtl = rk.rbtl(tourney_bad)
    print(f"b rbtl: \t{bad_rbtl}")

    # kt_it_count = kendall_tau(real, it_count)
    # print(f"The distance between the true ranking and the iterative win count ranking is: {kt_it_count}")

    # kt_it_borda = kendall_tau(real, it_borda)
    # print(f"The distance between the true ranking and the iterative borda is: {kt_it_borda}")

    # kt_it_w_borda = kendall_tau(real, it_weight_borda)
    # print(f"The distance between the true ranking and the iterative w borda is: {kt_it_w_borda}")

    # kt_it_kem = kendall_tau(real, it_kemeny)
    # print(f"The distance between the true ranking and the iterative kemeny is: {kt_it_kem}")

    # kt_it_btl = kendall_tau(real, it_btl)
    # print(f"The distance between the true ranking and the iterative btl is: {kt_it_btl}")

    # kt_it_rbtl = kendall_tau(real, it_rbtl)
    # print(f"The distance between the true ranking and the iterative rbtl is: {kt_it_rbtl}")

    kt_good_count = kendall_tau(real, good_count)
    print(
        f"The distance between the true ranking and the good win count is: {kt_good_count}"
    )

    kt_good_borda = kendall_tau(real, good_borda)
    print(
        f"The distance between the true ranking and the good borda is: {kt_good_borda}"
    )

    kt_good_w_borda = kendall_tau(real, good_weight_borda)
    print(
        f"The distance between the true ranking and the good w borda is: {kt_good_w_borda}"
    )

    kt_good_kem = kendall_tau(real, good_kemeny)
    print(f"The distance between the true ranking and the good kemen is: {kt_good_kem}")

    kt_good_btl = kendall_tau(real, good_btl)
    print(f"The distance between the true ranking and the good btl is: {kt_good_btl}")

    kt_good_rbtl = kendall_tau(real, good_rbtl)
    print(f"The distance between the true ranking and the good rbtl is: {kt_good_rbtl}")

    kt_bad_count = kendall_tau(real, bad_count)
    print(
        f"The distance between the true ranking and the bad win count is: {kt_bad_count}"
    )

    kt_bad_borda = kendall_tau(real, bad_borda)
    print(f"The distance between the true ranking and the bad borda is: {kt_bad_borda}")

    kt_bad_w_borda = kendall_tau(real, bad_weight_borda)
    print(
        f"The distance between the true ranking and the bad w borda is: {kt_bad_w_borda}"
    )

    kt_bad_kem = kendall_tau(real, bad_kemeny)
    print(f"The distance between the true ranking and the bad kemen is: {kt_bad_kem}")

    kt_bad_btl = kendall_tau(real, bad_btl)
    print(f"The distance between the true ranking and the bad btl is: {kt_bad_btl}")

    kt_bad_rbtl = kendall_tau(real, bad_rbtl)
    print(f"The distance between the true ranking and the bad rbtl is: {kt_bad_rbtl}")

    print(f"The average grade of the class was {classroom.avg_grade()}")

    k = [
        (kt_good_rbtl, "constrained rbtl"),
        (kt_good_btl, "constrained btl"),
        (kt_good_kem, "constrained kemeny"),
        (kt_good_borda, "constrained borda"),
        (kt_good_w_borda, "constrained weighted_borda"),
        (kt_good_count, "constrained win_count"),
        (kt_bad_rbtl, "unconstrained rbtl"),
        (kt_bad_btl, "unconstrained btl"),
        (kt_bad_kem, "unconstrained kemeny"),
        (kt_bad_borda, "unconstrained borda"),
        (kt_bad_w_borda, "unconstrained weighted_borda"),
        (kt_bad_count, "unconstrained win_count"),
        # (kt_it_rbtl, "iter rbtl"),
        # (kt_it_btl, "iter btl"),
        # (kt_it_kem, "iter kemeny"),
        # (kt_it_borda, "iter borda"),
        # (kt_it_w_borda, "iter weighted_borda"),
        # (kt_it_count, "iter win_count")
    ]
    rows.append([papers] + [i[0] for i in k])
    k.sort(key=lambda v: v[0])
    print(" > ".join([v[1] for v in k]))

with open(f"n={n}_regular.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
