from itertools import combinations


def kendall_tau(r1, r2):
    """
    Returns the kendall tau distance between 2 rankings
    https://stats.stackexchange.com/questions/168602/whats-the-kendall-taus-distance-between-these-2-rankings
    """
    # Direction translation of:
    # https://en.wikipedia.org/wiki/Kendall_tau_distance#Computing_the_Kendall_tau_distance
    if len(r1) != len(r2):
        raise ValueError("Length of rankings aren't equal")

    n = len(r1)
    inversions = 0
    pairs = combinations(range(n), 2)
    for x, y in pairs:
        a = r1.index(x) - r1.index(y)
        b = r2.index(x) - r2.index(y)

        if a * b < 0:
            inversions += 1

    normalised = (2 * inversions) / (n * (n - 1))
    return normalised
