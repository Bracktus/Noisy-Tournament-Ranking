import distribute_papers as dp
from generate_tourney import TournamentGenerator
from rankers import copeland, ranking_to_weights, kemeny, rbtl
from random import shuffle
from metrics import kendall_tau
from graph_utils import connected_graph


def run_iterative_tourney(k, rounds, ranker, classroom):
    """
    k: number of papers given per round
    rounds: number of rounds
    ranker: the ranking function used in the process
    classroom: the students participating
    """

    n = len(classroom)
    pairs = connected_graph(n, k)
    assigner = dp.PaperDistributor(n, pairs)
    assignments = assigner.get_solution()

    tourney_generator = TournamentGenerator(classroom)
    tourney_generator.generate_tournament(assignments)
    tournament = tourney_generator.get_results()
    ranking = ranker(tournament)

    seen_assignments = assignments
    for _ in range(rounds - 1):
        # rounds - 1 because we already did 1 round
        pairs = connected_graph(n, k)
        assigner = dp.IterativePaperDistributor(
            n=n, ranking=ranking, pairs=pairs, past_tourneys=seen_assignments
        )

        assignments = assigner.get_solution()
        for grader in assignments:
            for matchup in assignments[grader]:
                seen_assignments[grader].append(matchup)

        tourney_generator.generate_tournament(assignments)
        tournament = tourney_generator.get_results()
        ranking = ranker(tournament)

    real_ranking = tourney_generator.get_true_ranking()
    return real_ranking, ranking


def run_tourney(n, classroom, k=None):
    if k == None:
        distributor = dp.PaperDistributor(n)
    else:
        pairs = connected_graph(n, k)
        distributor = dp.PaperDistributor(n, pairs)

    assignments = distributor.get_solution()
    tourney_generator = TournamentGenerator(classroom)
    tourney_generator.generate_tournament(assignments)
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

    print(
        f"The distance between the true ranking and the copeland ranking is: {kendall_tau(t1, t2)}"
    )
    print(
        f"The distance between the true ranking and the weighted copeland ranking is: {kendall_tau(t1, t2w)}"
    )
    print(
        f"The distance between the true ranking and the kemeny ranking is: {kendall_tau(t1, t3)}"
    )
    print(
        f"The distance between the true ranking and the rbtl ranking is: {kendall_tau(t1, t4)}"
    )
    print(
        f"The distance between the true ranking and a random ranking is: {kendall_tau(t1,t5)}"
    )
