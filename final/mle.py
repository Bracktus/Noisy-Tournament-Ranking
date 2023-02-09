from scipy.optimize import minimize
import numpy as np


def obj_func(skill_levels, tournament):
    likelihood_f = np.array([])

    for grader in tournament:
        matchups = tournament[grader]
        for p1, p2 in matchups:
            i = skill_levels[grader]
            j = skill_levels[p1]
            k = skill_levels[p2]

            p_ijk = np.log(1 + np.exp(-(0.5*i + 0.5)*(j - k)))
            likelihood_f = np.append(likelihood_f, p_ijk)

    return np.prod(likelihood_f)


def mle(tournament, inital_guess=None):
    tourney_len = len(tournament) 
    if inital_guess == None:
        inital_guess = [0.5 for _ in range(tourney_len)]

    f = lambda guess : obj_func(guess, tournament)
    return minimize(f, inital_guess)
