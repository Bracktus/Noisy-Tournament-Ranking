from random import gauss, random
from itertools import product
from collections import defaultdict


def get_score():
    """
    Generates a score test between 0 and 1 along a
    gaussian distribution.

    With mean 0.5 and stdev 0.3
    """
    score = gauss(0.5, 0.3)
    return max(0, min(score, 1))


def get_students(n):
    """
    Generates a dictionary of students with
    their corresponding test scores
    """
    return {i: get_score() for i in range(n)}


def get_prob_correct(score):
    """
    Converts a student's score
    into a probability of them grading a matchup correctly.

    If they were purely guessing,
    then the probability would be 0.5.

    Therefore, we can say the probability of them getting it correct
    would lie between [0.5 - 1].
    Assuming they aren't malicious
    """
    return score * 0.5 + 0.5


def valid_match(grader, stud1, stud2):
    """
    It's a valid match if
    - A grader doesn't mark their own paper.
    - student2 > student1, because (a,b) == (b,a) so we don't
      need duplicates
    """
    return grader != stud1 and grader != stud2 and stud2 > stud1


n = 300
# Students is a mapping from a student number to their grade
students = get_students(n)
pairings = product(students, students, students)

results = {student_num: [] for student_num in students}
wrong_count = defaultdict(int)

for pairing in pairings:
    grader, s1, s2 = pairing

    if not valid_match(grader, s1, s2):
        continue

    grader_score = students[grader]
    grader_prob = get_prob_correct(grader_score)

    winner, loser = (s1, s2) if students[s1] > students[s2] else (s2, s1)

    if grader_prob > random():
        results[grader].append((winner, loser))
    else:
        wrong_count[grader] += 1
        results[grader].append((loser, winner))


print(results)
print(students)
print(wrong_count)
print(len(results[0]))
