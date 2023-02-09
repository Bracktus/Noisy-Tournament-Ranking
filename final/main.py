from generate_tourney import TournamentGenerator
from distribute_papers import PaperDistibutor
from rankers import copeland, ranking_to_weights, kemeny, rbtl
from random import shuffle
from metrics import kendall_tau


def main():
    distributor = PaperDistibutor(30)
    distributor.formulate_model()
    distributor.solve()

    assignments = distributor.get_solution()
    tourney_generator = TournamentGenerator(assignments)
    tourney_generator.generate_tournament()
    tourney_generator.print_tournament()
    tournament = tourney_generator.get_results()

    t1 = tourney_generator.get_true_ranking()

    t2 = copeland(tournament)
    weights = ranking_to_weights(t1)
    t2w = copeland(tournament, weights=weights)

    t3 = t1.copy()
    shuffle(t3)

    t4 = kemeny(tournament)
    t5 = rbtl(tournament)

    print(f"true: \n{t1}")
    print(f"copeland: \n{t2}")
    print(f"weighted copeland: \n{t2w}")
    print(f"kemeny: \n{t4}")
    print(f"rbtl: \n{t5}")
    print(f"random: \n{t3}")

    print(f"The distance between the true ranking and the copeland ranking is: {kendall_tau(t1, t2)}")
    print(f"The distance between the true ranking and the weighted copeland ranking is: {kendall_tau(t1, t2w)}")
    print(f"The distance between the true ranking and the kemeny ranking is: {kendall_tau(t1, t4)}")
    print(f"The distance between the true ranking and the rbtl ranking is: {kendall_tau(t1, t5)}")
    print(f"The distance between the true ranking and a random ranking is: {kendall_tau(t1,t3)}")

if __name__ == "__main__":
    main()
