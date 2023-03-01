from random import gauss


class Classroom:
    def __init__(self, num_students, malicious=False):
        self.num_students = num_students
        self.grades = {s: self._gen_score() for s in range(self.num_students)}
        self.malicious = malicious

    def _gen_score(self):
        """
        Generates a score test between 0 and 1 along a gaussian distribution. With mean 0.5 and stdev 0.3
        """
        score = gauss(0.5, 0.3)
        return max(0, min(score, 1))

    def grader_skill(self, student):
        """
        Takes in a student number and return the probability of them marking a matchup correctly
        """
        score = self.get_student_score(student)
        if not self.malicious:
            prob = score * 0.5 + 0.5
        else:
            prob = score

        return prob

    def get_student_score(self, student):
        return self.grades[student]

    def __len__(self):
        return self.num_students

    def avg_grade(self):
        n = self.num_students
        total = sum(self.grades.values())
        return total / n

    def get_true_ranking(self):
        grades = self.grades
        true_ranking = grades.items()
        true_ranking = sorted(true_ranking, key=lambda i: i[1], reverse=True)
        true_ranking = [student for (student, _) in true_ranking]
        return true_ranking
