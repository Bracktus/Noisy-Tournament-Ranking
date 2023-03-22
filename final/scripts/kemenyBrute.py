from itertools import permutations, combinations

all_perms = list(permutations("abcde"))
players = list("abcde")
results = {
    "a": [("c", "e"), ("b", "d")],
    "b": [("a", "e"), ("c", "d")],
    "c": [("a", "b"), ("d", "e")],
    "d": [("c", "a"), ("e", "b")],
    "e": [("a", "d"), ("c", "b")],
}
res_flat = set([item for sublist in list(results.values()) for item in sublist])

best_score = float("-inf")
best_ranking = None

for perm in all_perms:
    score = 0
    perm_pairs = list(combinations(perm, 2))

    for a, b in perm_pairs:
        if (a, b) in res_flat:
            score += 1
        elif (b, a) in res_flat:
            score -= 1

    if perm == ("c", "a", "b", "d", "e"):
        for a, b in perm_pairs:
            if (a, b) in res_flat:
                print(f"({a}, {b}) in +1")
            elif (b, a) in res_flat:
                print(f"({b}, {a}) in -1")

    if score > best_score:
        best_score = score
        best_ranking = perm

print(best_ranking)
print(best_score)
