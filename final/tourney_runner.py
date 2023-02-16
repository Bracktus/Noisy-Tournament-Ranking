import distribute_papers as dp
from generate_tourney import TournamentGenerator
from graph_utils import connected_graph
from metrics import kendall_tau

def run_iterative_tourney(n, k, rounds, ranker):
    """
    n: number of students
    k: number of papers given per round
    rounds: number of rounds 
    ranker: the ranking function used in the process
    """

    pairs = connected_graph(n, k)
    assigner = dp.PaperDistributor(n, pairs) 
    assignments = assigner.get_solution()

    tourney_generator = TournamentGenerator(assignments)
    tourney_generator.generate_tournament()
    tournament = tourney_generator.get_results()
    ranking = ranker(tournament)

    seen_assignments = assignments
    for _ in range(rounds):
        pairs = connected_graph(n,k)
        assigner = dp.IterativePaperDistributor(
            n=n, 
            ranking=ranking, 
            pairs=pairs,
            past_tourneys=seen_assignments
        )

        assignments = assigner.get_solution()
        for grader in assignments:
            for matchup in assignments[grader]:
                seen_assignments[grader].append(matchup)

        tourney_generator = TournamentGenerator(assignments)
        tourney_generator.generate_tournament()
        tournament = tourney_generator.get_results()
        ranking = ranker(tournament)

    return ranking

def run_tourney(n, k=None):
    if k != None:
        distributor = PaperDistributor(n)    
    else:
        pairs = connected_graph(n, k)
        distributor = PaperDistributor(n, pairs)

    assignments = distributor.get_solution()
    tourney_generator = TournamentGenerator(assignments)
    tourney_generator.generate_tournament(malicious=True)
    tourney_generator.print_tournament()
    tournament = tourney_generator.get_results()

    t1 = tourney_generator.get_true_ranking()
    print(f"true: \n{t1}")

    t2 = copeland(tournament)
    print(f"copeland: \n{t2}")

    weights = ranking_to_weights(t1)
    t2w = copeland(tournament, weights=weights)
    print(f"weighted copeland: \n{t2w}")

    t3 = kemeny(tournament)
    print(f"kemeny: \n{t3}")

    t4 = rbtl(tournament)
    print(f"rbtl: \n{t4}")

    t5 = t1.copy()
    shuffle(t5)
    print(f"random: \n{t5}")

    print(f"The distance between the true ranking and the copeland ranking is: {kendall_tau(t1, t2)}")
    print(f"The distance between the true ranking and the weighted copeland ranking is: {kendall_tau(t1, t2w)}")
    print(f"The distance between the true ranking and the kemeny ranking is: {kendall_tau(t1, t3)}")
    print(f"The distance between the true ranking and the rbtl ranking is: {kendall_tau(t1, t4)}")
    print(f"The distance between the true ranking and a random ranking is: {kendall_tau(t1,t5)}")

   
