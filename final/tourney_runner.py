import distribute_papers as dp
from generate_tourney import TournamentGenerator
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


def run_tourney(n, classroom, ranker, k=None):
    if k == None:
        distributor = dp.PaperDistributor(n)
    else:
        pairs = connected_graph(n, k)
        distributor = dp.PaperDistributor(n, pairs)

    assignments = distributor.get_solution()
    tourney_generator = TournamentGenerator(classroom)
    tourney_generator.generate_tournament(assignments)
    tournament = tourney_generator.get_results()
    tourney_generator.print_tournament()

    t1 = tourney_generator.get_true_ranking()
    t2 = ranker(tournament)
    return t1, t2
