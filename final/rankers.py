from collections import defaultdict
from simulated_annealing import calculate_kemeny
from mle import rbtl_mle, btl_mle


def ranking_to_weights(ranking):
    """converts a ranking to a mapping of player to weight"""
    n = len(ranking)
    k = (n * (n + 1)) / 2
    weights = {grader: (n - idx) / k for idx, grader in enumerate(ranking)}
    return weights


def win_count(tournament):
    """
    The win_count score of a student is:
    The node's outdegree
    """
    num_students = len(tournament)
    scores = {i: 0 for i in range(num_students)}
    for grader in tournament:
        for winner, _ in tournament[grader]:
            scores[winner] += 1

    ranking = scores.items()
    ranking = sorted(ranking, key=lambda i: i[1], reverse=True)
    ranking = [student for (student, _) in ranking]
    return ranking


def copeland(tournament, weights=None):
    """
    The copeland score of a student is:
    The node's outdegree - the node's indegree
    Optionally is weighted
    """
    copeland_scores = defaultdict(int)
    for grader in tournament:
        w = 1 if weights == None else weights[grader]
        for match in tournament[grader]:
            winner, loser = match
            copeland_scores[winner] += w
            copeland_scores[loser] -= w

    ranking = copeland_scores.items()
    ranking = sorted(ranking, key=lambda i: i[1], reverse=True)
    ranking = [student for (student, _) in ranking]
    return ranking

def weighted_borda(tournament):
    ranking = copeland(tournament)
    weights = ranking_to_weights(ranking)
    return copeland(tournament, weights)

def kemeny(tournament):
    """
    Finds an approximation of the kemeny ranking of a tournament
    through simulated annealing.
    """
    matchups = tournament.values()
    matchups = [matchup for sublist in matchups for matchup in sublist]
    inital_sol = [i for i in range(len(tournament))]
    ranking = calculate_kemeny(
        inital_solution=inital_sol,
        tourney=matchups,
        initial_temperature=0.9,
        temperature_length=100,
        cooling_ratio=0.99,
        num_non_improve=1000000,
    )
    return ranking


def rbtl(tournament):
    """
    Finds the refereed bradley-terry model ranking of a tournament
    through maximum likelihood estimation.
    """
    ranking = rbtl_mle(tournament)
    ranking = enumerate(ranking)
    ranking = sorted(ranking, key=lambda i: i[1], reverse=True)
    ranking = [student for (student, _) in ranking]
    return ranking


def btl(tournament):
    """
    Finds the refereed bradley-terry model ranking of a tournament
    through maximum likelihood estimation.
    """
    ranking = btl_mle(tournament)
    ranking = enumerate(ranking)
    ranking = sorted(ranking, key=lambda i: i[1], reverse=True)
    ranking = [student for (student, _) in ranking]
    return ranking
