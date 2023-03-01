from random import random
from collections import defaultdict


class TournamentGenerator:
    def __init__(self, classroom):
        self.num_students = len(classroom)

        self.cache = defaultdict(list)
        self.iter_tourney = defaultdict(list)
        self.tournament_generated = False
        self.classroom = classroom

    def get_grader_prob(self, grader, p1, p2):
        return self.classroom.grader_skill(grader)

    def reset_iter_tourney(self):
        self.iter_tourney = defaultdict(list)
    
    def populate_iter_tournament(self, assignments):
        for grader in assignments:
            matchups = assignments[grader]
            grader_prob = self.classroom.grader_skill(grader)

            for p1, p2 in matchups:
                first_in = (p1, p2) in self.cache[grader]
                second_in = (p2, p1) in self.cache[grader]
                           
                if first_in:
                    result = self.cache[grader]
                    self.iter_tourney[grader].append(result)
                elif second_in:
                    result = self.cache[grader]
                    self.iter_tourney[grader].append(result)
                else:
                    grades = self.classroom.grades
                    winner, loser = (p1, p2) if grades[p1] > grades[p2] else (p2, p1)

                    if grader_prob > random():
                        result = (winner, loser)
                    else:
                        result = (loser, winner)

                    self.cache[grader].append(result)
                    self.iter_tourney[grader].append(result)

        

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
                first_in = (p1, p2) if (p1, p2) in self.cache[grader] else False
                second_in = (p2, p1) if (p2, p1) in self.cache[grader] else False
                           
                if first_in:
                    tournament_results[grader].append(first_in)
                elif second_in:
                    tournament_results[grader].append(second_in)
                else:
                    grades = self.classroom.grades
                    winner, loser = (p1, p2) if grades[p1] > grades[p2] else (p2, p1)
                    grader_prob = self.get_grader_prob(grader, p1, p2)

                    if grader_prob > random():
                        result = (winner, loser)
                    else:
                        result = (loser, winner)

                    self.cache[grader].append(result)
                    tournament_results[grader].append(result)

        return tournament_results

    def print_tournament(self, tournament):
        grades = self.classroom.grades
        for student in tournament:
            matchups = tournament[student]
            print(f"{student}: {matchups}: {grades[student]}")
