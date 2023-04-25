import sys

sys.path.append("..")

from tourney_runner import run_iterative_tourney
from metrics import kendall_tau
from classroom import Classroom
import distribute_papers as dp
import rankers as rk
from graph_utils import fair_graph
from generate_tourney import TournamentGenerator

import csv

fields = [
    "Number of students",
    "RBTL",
    "BTL",
    "KEMENY",
    "BORDA",
    "WEIGHTED BORDA",
    "WIN COUNT"
]

def get_num_edges(n):
    return (n*(n - 1))/2

n = 5
classroom = Classroom(n, malicious=False)
tourney_generator = TournamentGenerator(classroom)
rows = []

while n < 30:
    e = get_num_edges(n)
    graph = fair_graph(n, e)

    asins = {}

    for student in range(n):
        valid_match = lambda v: v[0] != student and v[1] != student
        asins[student] = [s for s in graph if valid_match(s)]
        
    tourney = tourney_generator.generate_tournament(asins)
    
    res_real = classroom.get_true_ranking()
    res_rbtl = rk.rbtl(tourney)
    res_btl = rk.btl(tourney)
    res_kem = rk.kemeny(tourney)
    res_borda = rk.copeland(tourney)
    res_w_borda = rk.weighted_borda(tourney)
    res_win_count = rk.win_count(tourney)
    
    row = [
        n,
        kendall_tau(res_real, res_rbtl),
        kendall_tau(res_real, res_btl),
        kendall_tau(res_real, res_kem),
        kendall_tau(res_real, res_borda),
        kendall_tau(res_real, res_w_borda),
        kendall_tau(res_real, res_win_count)
    ]

    print(row)

    rows.append(row)
    n += 1
    classroom.add_student()

with open(f"complete_information.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

