from generate_tourney import TournamentGenerator
from distribute_papers import PaperDistributor
from rankers import copeland, ranking_to_weights, kemeny, rbtl
from random import shuffle
from metrics import kendall_tau
from graph_utils import connected_graph


def main():
    n = 31
    pairs = connected_graph(n, 10)

    # distributor = PaperDistributor(n)
    distributor = PaperDistributor(n, pairs)
    assignments = distributor.get_solution()

    tourney_generator = TournamentGenerator(assignments)
    tourney_generator.generate_tournament(malicious=True)
    tourney_generator.print_tournament()
    tournament = tourney_generator.get_results()

    t1 = tourney_generator.get_true_ranking()
    print(f"true: \n{t1}")

    t2 = copeland(tournament)
    print(f"copeland: \n{t2}")

    weights = ranking_to_weights(t1)
    t2w = copeland(tournament, weights=weights)
    print(f"weighted copeland: \n{t2w}")

    t3 = kemeny(tournament)
    print(f"kemeny: \n{t3}")

    t4 = rbtl(tournament)
    print(f"rbtl: \n{t4}")

    t5 = t1.copy()
    shuffle(t5)
    print(f"random: \n{t5}")

    print(f"The distance between the true ranking and the copeland ranking is: {kendall_tau(t1, t2)}")
    print(f"The distance between the true ranking and the weighted copeland ranking is: {kendall_tau(t1, t2w)}")
    print(f"The distance between the true ranking and the kemeny ranking is: {kendall_tau(t1, t3)}")
    print(f"The distance between the true ranking and the rbtl ranking is: {kendall_tau(t1, t4)}")
    print(f"The distance between the true ranking and a random ranking is: {kendall_tau(t1,t5)}")

if __name__ == "__main__":
    main()
