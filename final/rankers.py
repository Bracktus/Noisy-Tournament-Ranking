from collections import defaultdict
from simulated_annealing import calculate_kemeny

def kendall_tau(r1, r2):
    """
    Returns the kendall tau distance between 2 rankings
    """
    # Direction translation of:
    # https://en.wikipedia.org/wiki/Kendall_tau_distance#Computing_the_Kendall_tau_distance

    if len(r1) != len(r2):
        raise ValueError("Length of rankings aren't equal")
    
    rank_len = len(r1)
    inversions = 0

    for i in range(rank_len):
        for j in range(i + 1, rank_len):
            a = r1[i] < r1[j] and r2[i] > r2[j]
            b = r1[i] > r1[j] and r2[i] < r2[j]

            if a or b:
                inversions += 1
    n = len(r1)
    normalised = (2 * inversions ) / (n * (n - 1))
    return normalised

def ranking_to_weights(ranking):
    """converts a ranking to a mapping of player to weight"""
    n = len(ranking)
    k = (n*(n+1))/2
    weights = {grader: (n-idx)/k for idx, grader in enumerate(ranking)}
    return weights

def copeland(tournament, weights=None):
    """
    The copeland score of a student is:
    The node's indegree - the node's outdegree
    Optionally is weighted
    """
    matchups = tournament.values()
    matchups = [matchup for sublist in matchups for matchup in sublist]
    copeland_scores = defaultdict(int)
    for grader in tournament:
        w = 1 if weights == None else weights[grader]
        for match in matchups:
            winner, loser = match
            if grader == winner:
                copeland_scores[grader] += w
            elif grader == loser:
                copeland_scores[grader] -= w

    result = copeland_scores.items()
    result = sorted(result, key=lambda i : i[1], reverse=True)
    result = [student for (student, _) in result]
    return result

def kemeny(tournament):
    matchups = tournament.values()
    matchups = set([matchup for sublist in matchups for matchup in sublist])
    n = len(tournament)
    inital_sol = [i for i in range(n)]
    solution = calculate_kemeny(
        inital_solution=inital_sol, 
        tourney=matchups,
        initial_temperature=0.9,
        temperature_length=100,
        cooling_ratio=0.99,
        num_non_improve=1000000
    )
    return solution
    

