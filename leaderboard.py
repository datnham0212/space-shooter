import json

class Leaderboard:
    def __init__(self, file_path="leaderboard.json"):
        self.file_path = file_path
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_scores(self):
        with open(self.file_path, "w") as file:
            json.dump(self.scores, file)

    def add_score(self, name, score):
        self.scores.append({"name": name, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)[:5]  # Keep top 5 scores
        self.save_scores()

    def get_scores(self):
        return self.scores