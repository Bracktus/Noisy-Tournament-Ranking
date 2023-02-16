from generate_tourney import TournamentGenerator
from distribute_papers import PaperDistributor
from rankers import copeland, ranking_to_weights, kemeny, rbtl
from random import shuffle
from metrics import kendall_tau
from graph_utils import connected_graph
from tourney_runner import run_iterative_tourney, run_tourney


def main():
    n = 33
    k = 2
    run_tourney(n) 
    run_iterative_tourney(n, k, 7, rbtl)

if __name__ == "__main__":
    main()
