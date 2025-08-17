class PuzzleBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pieces = []
        self.placed_pieces = {}
        self.is_complete = False

    def add_piece(self, piece):
        self.pieces.append(piece)

    def place_piece(self, piece, position):
        if piece in self.pieces:
            self.placed_pieces[position] = piece
            self.pieces.remove(piece)
            self.check_completion()

    def check_completion(self):
        if not self.pieces:
            self.is_complete = True

    def reset_board(self):
        self.placed_pieces.clear()
        self.is_complete = False

    def get_board_state(self):
        return {
            'placed_pieces': self.placed_pieces,
            'is_complete': self.is_complete
        }