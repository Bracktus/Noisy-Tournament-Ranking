from tourney_runner import run_iterative_tourney
from metrics import kendall_tau
from rankers import rbtl, btl, kemeny, copeland
from classroom import Classroom
import distribute_papers as dp
from graph_utils import fair_graph
from generate_tourney import TournamentGenerator


def main():
    n = 33
    papers = 13

    classroom = Classroom(n, malicious=False)
    real = classroom.get_true_ranking()
    print(f"running tourney with {n} students and {papers - 1} matchups to mark each")
    print(f"real: {real}")

    tourney_generator = TournamentGenerator(classroom)
    iter_ranking = run_iterative_tourney(n, papers - 1, rbtl, tourney_generator)
    kt0 = kendall_tau(real, iter_ranking)

    tourney_generator.reset_iter_tourney()
    iter_ranking2 = run_iterative_tourney(n, papers - 1, copeland, tourney_generator)
    kt_s = kendall_tau(real, iter_ranking2)

    pairs = fair_graph(n, papers * n)
    distributor = dp.PaperDistributor(n, pairs)
    assignments = distributor.get_solution()
    tourney = tourney_generator.generate_tournament(assignments)

    print(f"iter: {iter_ranking}")
    print(f"iter2: {iter_ranking2}")
    t1 = rbtl(tourney)
    print(f"rbtl: {t1}")
    t2 = btl(tourney)
    print(f" btl: {t2}")
    t3 = kemeny(tourney)
    print(f"keme: {t3}")
    t4 = copeland(tourney)
    print(f"cope: {t4}")

    print(f"The distance between the true ranking and the iter cope ranking is: {kt_s}")
    print(f"The distance between the true ranking and the iter rbtl ranking is: {kt0}")
    kt1 = kendall_tau(real, t1)
    print(f"The distance between the true ranking and the rbtl ranking is: {kt1}")
    kt2 = kendall_tau(real, t2)
    print(f"The distance between the true ranking and the btl ranking is: {kt2}")
    kt3 = kendall_tau(real, t3)
    print(f"The distance between the true ranking and the kemeny ranking is: {kt3}")
    kt4 = kendall_tau(real, t4)
    print(f"The distance between the true ranking and the copeland ranking is: {kt4}")

    print(f"The average grade of the class was {classroom.avg_grade()}")

    k = [(kt0, "iter"), (kt1, "rbtl"), (kt2, "btl"), (kt3, "kemeny"), (kt4, "copeland")]
    k.sort(key=lambda v: v[0])
    print(" > ".join([v[1] for v in k]))


if __name__ == "__main__":
    main()
