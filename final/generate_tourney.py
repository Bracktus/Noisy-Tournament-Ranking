from random import gauss, random 
from collections import defaultdict

class TournamentGenerator():

    def __init__(self, assignments):
        self.assignments = assignments
        self.num_students = len(assignments)

        self.grades = {}
        self.tournament_results = defaultdict(list)

        self.tournament_generated = False

    def get_score(self):
        """
        Generates a score test between 0 and 1 along a gaussian distribution. With mean 0.5 and stdev 0.3
        """
        score = gauss(0.5, 0.3)
        return max(0, min(score, 1))

 
    def get_prob_correct(self, score):
        """
        Converts a student's score into a probability of them grading a matchup correctly.
        If they were purely guessing, then the probability would be 0.5.
        Therefore, we can say the probability of them getting it correct would lie between [0.5 - 1].
        Assuming they aren't malicious
        """
        return score * 0.5 + 0.5

    def generate_tournament(self):
        """
        This returns a dictionary. 
        The keys are the graders, the values are the results of the matches that the student marked.
        """
        # Each student is now assigned a score
        self.grades = {s: self.get_score() for s in range(self.num_students)}
        for grader in self.assignments:
            matchups = self.assignments[grader]
            grader_score = self.grades[grader]
            grader_prob = grader_score

            # Uncommenting this line assumes unmalicious students
            # grader_prob = self.get_prob_correct(grader_score)
            
            for p1, p2 in matchups:
                winner, loser = (p1, p2) if self.grades[p1] > self.grades[p2] else (p2, p1)
                if grader_prob > random():
                    result = (winner, loser)
                else:
                    result = (loser, winner)

                self.tournament_results[grader].append(result)

        self.tournament_generated = True

    def print_tournament(self):
        if not self.tournament_generated:
            raise AttributeError("Tournament not generated")
            
        for student in self.tournament_results:
            matchups = self.tournament_results[student]
            print(f"{student}: {matchups}: {self.grades[student]}")

    def get_results(self):
        return self.tournament_results

    def get_true_ranking(self):
        true_ranking = self.grades.items()
        true_ranking = sorted(true_ranking, key=lambda i: i[1], reverse=True)
        true_ranking = [student for (student, _) in true_ranking]
        return true_ranking
                            

