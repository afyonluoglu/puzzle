class GameState:
    def __init__(self):
        self.piece_positions = {}
        self.score = 0
        self.high_score = 0
        self.is_completed = False

    def save_state(self):
        # Logic to save the current game state to a file or database
        pass

    def load_state(self):
        # Logic to load the game state from a file or database
        pass

    def update_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self):
        self.piece_positions.clear()
        self.score = 0
        self.is_completed = False

    def check_completion(self):
        # Logic to check if the puzzle is completed
        pass