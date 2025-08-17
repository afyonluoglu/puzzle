class Scoring:
    def __init__(self):
        self.score = 0
        self.high_scores = []

    def add_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score

    def save_high_score(self, name):
        self.high_scores.append((name, self.score))
        self.high_scores.sort(key=lambda x: x[1], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10 scores

    def get_high_scores(self):
        return self.high_scores

    def clear_high_scores(self):
        self.high_scores = []