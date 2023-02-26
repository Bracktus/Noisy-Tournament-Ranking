from tourney_runner import run_iterative_tourney, run_tourney
from metrics import kendall_tau
from rankers import rbtl
from classroom import Classroom


def main():
    n = 15
    papers = 8

    classroom = Classroom(n, malicious=False)
    real, mine1 = run_iterative_tourney(
        k=1,
        rounds=papers,
        ranker=rbtl,
        classroom=classroom
    )
    print(f"running tourney with {n} students and {papers - 1} matchups to mark each")
    print(f"real: {real}")
    print(f"iterative: {mine1}")

    real, mine2 = run_tourney(n=n, classroom=classroom, ranker=rbtl, k=papers)
    print(f"non-iterative: {mine2}")
    print(
        f"The distance between the true ranking and the iterative rbtl ranking is: {kendall_tau(real, mine1)}"
    )
    print(
        f"The distance between the true ranking and the non-iterative rbtl ranking is: {kendall_tau(real, mine2)}"
    )

    print(f"The average grade of the class was {classroom.avg_grade()}")


if __name__ == "__main__":
    main()
