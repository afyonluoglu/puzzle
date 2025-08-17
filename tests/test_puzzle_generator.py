import unittest
from src.game.puzzle_generator import PuzzleGenerator

class TestPuzzleGenerator(unittest.TestCase):

    def setUp(self):
        self.image_path = 'assets/images/default/sample_puzzle.jpg'
        self.puzzle_generator = PuzzleGenerator(self.image_path, rows=4, cols=4)

    def test_generate_puzzle_pieces(self):
        pieces = self.puzzle_generator.generate_puzzle_pieces()
        self.assertEqual(len(pieces), 16)  # 4x4 puzzle should have 16 pieces

    def test_shuffle_pieces(self):
        original_pieces = self.puzzle_generator.generate_puzzle_pieces()
        shuffled_pieces = self.puzzle_generator.shuffle_pieces(original_pieces)
        self.assertNotEqual(original_pieces, shuffled_pieces)

    def test_piece_dimensions(self):
        pieces = self.puzzle_generator.generate_puzzle_pieces()
        for piece in pieces:
            self.assertEqual(piece.size, (self.puzzle_generator.piece_width, self.puzzle_generator.piece_height))

    def test_invalid_image_path(self):
        with self.assertRaises(FileNotFoundError):
            invalid_generator = PuzzleGenerator('invalid/path/to/image.jpg', rows=4, cols=4)
            invalid_generator.generate_puzzle_pieces()

if __name__ == '__main__':
    unittest.main()