from scipy.optimize import minimize, Bounds
import numpy as np

results = {
    0: [(2, 4), (1, 3)],
    1: [(0, 4), (2, 3)],
    2: [(0, 1), (3, 4)],
    3: [(2, 0), (4, 1)],
    4: [(0, 3), (2, 1)]
}

res_flat = []
for v in results:
    for t1, t2 in results[v]:
        res_flat.append((v, t1, t2))

def _btl_obj_func(skill_levels, tournament):
    likelihood_f = np.array([])
    for _, p1, p2 in tournament:
        j, k = skill_levels[p1], skill_levels[p2]
        p_jk = np.log(1 + np.exp(-(j - k)))
        likelihood_f = np.append(likelihood_f, p_jk)

    return np.sum(likelihood_f)

def btl_mle(tournament, inital_guess=None):
    tourney_len = len(tournament)
    if inital_guess == None:
        inital_guess = [0.5 for _ in range(5)]

    inital_guess = inital_guess
    f = lambda guess: _btl_obj_func(guess, tournament)
    bounds = Bounds(0, 1)

    ranking = minimize(f, inital_guess, bounds=bounds).x
    return ranking

ranking = btl_mle(res_flat)
print(ranking)

