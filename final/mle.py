from scipy.optimize import minimize, Bounds
import numpy as np

def _btl_obj_func(skill_levels, tournament):
    likelihood_f = np.array([])
    for grader in tournament:
        matchups = tournament[grader]
        for p1, p2 in matchups:
            j,k = skill_levels[p1], skill_levels[p2]
            p_jk = np.log(1 + np.exp(-(j - k)))
            likelihood_f = np.append(likelihood_f, p_jk)

    return np.sum(likelihood_f)

def _rbtl_obj_func(skill_levels, tournament):
    """
    The refereed bradley-terry model is as follows:
    p(i: j > k) = 1/(1 + e^{gi*(wj + wk)})
    where wj and wk are the skill levels of j and k
    and gi is the grading level of i. Which is a function of wi.

    Our likelihood function will be product(p(i: j > k)) for all (i:j,k) in assignemnts
    If we take the log of this we get.
    sum(-ln(1 + e^{gi*(wj + wk)})) for all (i:j,k) in assingments
    Maximise this function to get our values for gi, wj, wk for all i,j,k.

    (we actually minimise but just remove the minus sign)
    """
    a, b, *skill_levels = skill_levels
    likelihood_f = np.array([])

    for grader in tournament:
        matchups = tournament[grader]
        for p1, p2 in matchups:
            i = skill_levels[grader]
            j = skill_levels[p1]
            k = skill_levels[p2]

            p_ijk = np.log(1 + np.exp(-(a * i + b) * (j - k)))
            likelihood_f = np.append(likelihood_f, p_ijk)

    return np.sum(likelihood_f)


def btl_mle(tournament, inital_guess=None):
    tourney_len = len(tournament)
    if inital_guess == None:
        inital_guess = [0.5 for _ in range(tourney_len)]

    inital_guess = inital_guess
    f = lambda guess: _btl_obj_func(guess, tournament)
    bounds = Bounds(-50, 50)

    ranking = minimize(f, inital_guess, bounds=bounds).x
    return ranking

def rbtl_mle(tournament, inital_guess=None):
    tourney_len = len(tournament)
    if inital_guess == None:
        inital_guess = [0.5 for _ in range(tourney_len)]

    ab = [1, 1]
    inital_guess = ab + inital_guess
    f = lambda guess: _rbtl_obj_func(guess, tournament)
    bounds = Bounds(-50, 50)

    ranking = minimize(f, inital_guess, bounds=bounds).x
    ranking = ranking[2:]  # The first 2 values are a and b, we want the rest
    return ranking
