import distribute_papers as dp
from graph_utils import random_cycle

# Idea
# instead of storing state in the class.
# let's maintain internal state in the method and just merge the dictionaries

def tourney_merge(t1, t2):
    acc = {}
    for grader in t1:
        l1 = t1[grader]
        l2 = t2[grader]
        acc[grader] = l1 + l2

    return acc
        
def run_iterative_tourney(n, rounds, ranker, tourney_generator):
    """
    n: number of players
    rounds: number of rounds
    ranker: the ranking function used in the process
    classroom: the students participating
    """

    # Big hack.
    # run this BEFORE doing the the regular tournies.
    # Otherwise it'll gain more information than it actually knows due to it ranking over the cache.

    ppr = 1
    pairs = random_cycle(n)
    assigner = dp.PaperDistributor(n, pairs)
    assignments = assigner.get_solution()
    
    full_tournament = tourney_generator.generate_tournament(assignments)
    ranking = ranker(full_tournament)

    seen_assignments = assignments
    for _ in range(rounds - 1):
        # rounds - 1 because we already did 1 round
        pairs = random_cycle(n)
        assigner = dp.IterativePaperDistributor(
            n=n, ranking=ranking, pairs=pairs, past_tourneys=seen_assignments
        )

        assignments = assigner.get_solution()
        for grader in assignments:
            for matchup in assignments[grader]:
                seen_assignments[grader].append(matchup)

        tournament = tourney_generator.generate_tournament(assignments)
        full_tournament = tourney_merge(full_tournament, tournament)
        ranking = ranker(full_tournament)

    return ranking
