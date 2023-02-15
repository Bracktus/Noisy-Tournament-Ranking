import distribute_papers as dp
from generate_tourney import TournamentGenerator
from graph_utils import connected_graph

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
   
