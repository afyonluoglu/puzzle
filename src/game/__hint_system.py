from datetime import datetime

class HintSystem:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.hints_used = 0
        self.max_hints = 3  # Maximum number of hints allowed
        self.hint_log = []  # To keep track of hints used

    def provide_hint(self):
        if self.hints_used < self.max_hints:
            hint = self.generate_hint()
            self.hints_used += 1
            self.hint_log.append((datetime.now(), hint))
            return hint
        else:
            return "No more hints available."

    def generate_hint(self):
        # Logic to generate a hint, e.g., suggest a piece position
        for piece in self.puzzle.pieces:
            if not piece.is_placed:
                return f"Try placing piece {piece.id} at position {piece.suggested_position}."
        return "All pieces are placed!"

    def reset_hints(self):
        self.hints_used = 0
        self.hint_log.clear()

    def get_hint_log(self):
        return self.hint_log