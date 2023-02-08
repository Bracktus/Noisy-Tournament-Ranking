import random
import math

def kemeny_score(ranking, tourney):
    score = 0
    for i in range(len(ranking)):
        for j in range(i + 1, len(ranking)):
            pair = (ranking[j], ranking[i])
            if pair in tourney:
                score += 1
    return score


def get_neighbour(ranking, tourney, orig_score):
    idx_1 = random.randrange(0, len(ranking) - 1)
    idx_2 = idx_1 + 1

    new_rnk = ranking.copy()

    new_rnk[idx_1], new_rnk[idx_2] = new_rnk[idx_2], new_rnk[idx_1]
    score = orig_score

    l_plr = new_rnk[idx_1]
    h_plr = new_rnk[idx_2]

    pair_1 = (l_plr, h_plr)
    pair_2 = (h_plr, l_plr)

    if pair_1 in tourney:
        score -= 1
    if pair_2 in tourney:
        score += 1

    return score, new_rnk


def calculate_kemeny(inital_solution,
                     tourney,
                     initial_temperature,
                     temperature_length,
                     cooling_ratio,
                     num_non_improve):
    """
    Calculates an approximation of the best kemeny ranking using simulated annealing
    """

    # Set the inital and the best solutions
    curr_sol = inital_solution
    best_sol = inital_solution
    curr_score = kemeny_score(inital_solution, tourney)
    best_score = curr_score

    non_improve_count = 0
    temperature = initial_temperature

    # While the stopping criterion is not in effect
    while non_improve_count < num_non_improve:
        # Run inner loop for temperature_length iterations
        for _ in range(temperature_length):
            # Get a neighbour
            new_score, new_sol = get_neighbour(curr_sol,
                                               tourney,
                                               curr_score)
            # Get delta_C
            score_diff = new_score - curr_score

            # If the neighbours score is better than the current solution
            if score_diff <= 0:
                # Then set the current neighbourhood to it
                curr_score = new_score
                curr_sol = new_sol

                # If it's the best solution found so far
                if new_score < best_score:
                    # Then set it to the best solution
                    non_improve_count = 0
                    best_score = new_score
                    best_sol = new_sol.copy()
                else:
                    non_improve_count += 1

            else:
                non_improve_count += 1
                # Generate a number between 0 and 1
                q = random.random()
                # If it's greater than e^{-deltaC/T}
                if q < math.exp(-score_diff/temperature):
                    curr_sol = new_sol
                    curr_score = new_score

        # set T to f(T), where f(T) = a * T
        temperature *= cooling_ratio

    return best_sol 
