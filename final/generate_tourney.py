from random import random
from collections import defaultdict


class TournamentGenerator:
    def __init__(self, classroom):
        self.num_students = len(classroom)

        self.cache = defaultdict(list)
        self.iter_tourney = defaultdict(list)
        self.tournament_generated = False
        self.classroom = classroom

        """
        We need a cache to ensure our data is consistent across tests.
        (i, j, k) should remain the same whenever we rerun a tourney with different assignments.
        This allows us to compare the ranking methods with at least some accuracy.
        """

    def get_grader_prob(self, grader, p1, p2):
        return self.classroom.grader_skill(grader)

    def generate_tournament(self, assignments):
        """
        This returns a dictionary.
        The keys are the graders, the values are the results of the matches that the student marked.
        """
        # Each student is now assigned a score

        tournament_results = defaultdict(list)
        for grader in assignments:
            matchups = assignments[grader]

            for p1, p2 in matchups:
                grades = self.classroom.grades
                winner, loser = (p1, p2) if grades[p1] > grades[p2] else (p2, p1)
                correct = (winner, loser)
                wrong = (loser, winner)

                if correct in self.cache[grader]:
                    tournament_results[grader].append(correct)
                elif wrong in self.cache[grader]:
                    tournament_results[grader].append(wrong)
                else:
                    grader_prob = self.get_grader_prob(grader, p1, p2)
                    if grader_prob > random():
                        result = correct
                    else:
                        result = wrong

                    self.cache[grader].append(result)
                    tournament_results[grader].append(result)

        return tournament_results

    def print_tournament(self, tournament):
        grades = self.classroom.grades
        for student in tournament:
            matchups = tournament[student]
            print(f"{student}: {matchups}: {grades[student]}")
