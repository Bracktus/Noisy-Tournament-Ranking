import distribute_papers as dp
from graph_utils import connected_graph


def run_iterative_tourney(n, rounds, ranker, tourney_generator):
    """
    n: number of players
    rounds: number of rounds
    ranker: the ranking function used in the process
    classroom: the students participating
    """

    #Big hack.
    #run this BEFORE doing the the regular tournies.
    #Otherwise it'll gain more information than it actually knows due to it ranking over the cache.

    ppr = 1
    pairs = connected_graph(n, ppr)
    assigner = dp.PaperDistributor(n, pairs)
    assignments = assigner.get_solution()

    tournament = tourney_generator.generate_tournament(assignments)
    ranking = ranker(tournament)

    seen_assignments = assignments
    for _ in range(rounds - 1):
        # rounds - 1 because we already did 1 round
        pairs = connected_graph(n, ppr)
        assigner = dp.IterativePaperDistributor(
            n=n, ranking=ranking, pairs=pairs, past_tourneys=seen_assignments
        )

        assignments = assigner.get_solution()
        for grader in assignments:
            for matchup in assignments[grader]:
                seen_assignments[grader].append(matchup)

        tourney_generator.generate_tournament(assignments)
        tournament = tourney_generator.cache
        ranking = ranker(tournament)


    return ranking

