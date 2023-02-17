from random import random 
from collections import defaultdict

class TournamentGenerator():

    def __init__(self, n, classroom):
        self.num_students = n

        self.tournament_results = defaultdict(list)
        self.tournament_generated = False
        self.classroom = classroom

    def generate_tournament(self, assignments):
        """
        This returns a dictionary. 
        The keys are the graders, the values are the results of the matches that the student marked.
        """
        # Each student is now assigned a score

        for grader in assignments:
            matchups = assignments[grader]
            grades = self.classroom.grades
            grader_prob = self.classroom.grader_skill(grader)
            
            for p1, p2 in matchups:
                winner, loser = (p1, p2) if grades[p1] > grades[p2] else (p2, p1)
                if grader_prob > random():
                    result = (winner, loser)
                else:
                    result = (loser, winner)

                self.tournament_results[grader].append(result)

        self.tournament_generated = True
        self.print_tournament()

    def print_tournament(self):
        if not self.tournament_generated:
            raise AttributeError("Tournament not generated")
            
        grades = self.classroom.grades
        for student in self.tournament_results:
            matchups = self.tournament_results[student]
            print(f"{student}: {matchups}: {grades[student]}")

    def get_results(self):
        return self.tournament_results

    def get_true_ranking(self):
        grades = self.classroom.grades
        true_ranking = grades.items()
        true_ranking = sorted(true_ranking, key=lambda i: i[1], reverse=True)
        true_ranking = [student for (student, _) in true_ranking]
        return true_ranking
                            

