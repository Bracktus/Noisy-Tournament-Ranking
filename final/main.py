from tourney_runner import run_iterative_tourney, run_tourney
from metrics import kendall_tau
from rankers import rbtl
from classroom import Classroom


def main():
    n = 22
    classroom = Classroom(n, malicious=False)
    real, mine = run_iterative_tourney(1, 5, rbtl, classroom)
    print(
        f"The distance between the true ranking and the rbtl ranking is: {kendall_tau(real, mine)}"
    )

    # run_tourney(n, 4)


if __name__ == "__main__":
    main()
