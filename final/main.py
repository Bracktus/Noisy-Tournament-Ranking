from tourney_runner import run_iterative_tourney, run_tourney
from metrics import kendall_tau
from rankers import rbtl, btl, kemeny, copeland
from classroom import Classroom


def main():
    n = 17
    papers = 10

    classroom = Classroom(n, malicious=False)
    real = classroom.get_true_ranking()
    # real, mine1 = run_iterative_tourney(
    #     k=1,
    #     rounds=papers,
    #     ranker=rbtl,
    #     classroom=classroom
    # )

    # print(f"running tourney with {n} students and {papers - 1} matchups to mark each")
    # print(f"real: {real}")
    # print(f"iterative: {mine1}")

    t1 = run_tourney(n=n, classroom=classroom, ranker=rbtl, k=papers)
    t2 = run_tourney(n=n, classroom=classroom, ranker=btl, k=papers)
    t3 = run_tourney(n=n, classroom=classroom, ranker=kemeny, k=papers)
    t4 = run_tourney(n=n, classroom=classroom, ranker=copeland, k=papers)
    kt1 = kendall_tau(real, t1)
    kt2 = kendall_tau(real, t2)
    kt3 = kendall_tau(real, t3)
    kt4 = kendall_tau(real, t4)
    print(
        f"The distance between the true ranking and the rbtl ranking is: {kt1}"
    )
    print(
        f"The distance between the true ranking and the btl ranking is: {kt2}"
    )
    print(
        f"The distance between the true ranking and the kemeny ranking is: {kt3}"
    )
    print(
        f"The distance between the true ranking and the copeland ranking is: {kt4}"
    )
 
    print(f"The average grade of the class was {classroom.avg_grade()}")

    k = [(kt1, "rbtl"), (kt2, "btl"), (kt3, "kemeny"), (kt4, "copeland")]
    k.sort(key=lambda v: v[0])
    print(" > ".join([v[1] for v in k]))

    


if __name__ == "__main__":
    main()
