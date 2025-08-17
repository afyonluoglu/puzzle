import unittest
from src.game.game_state import GameState

class TestGameState(unittest.TestCase):

    def setUp(self):
        self.game_state = GameState()

    def test_initial_state(self):
        self.assertEqual(self.game_state.score, 0)
        self.assertEqual(self.game_state.pieces, [])
        self.assertFalse(self.game_state.is_completed)

    def test_save_state(self):
        self.game_state.score = 100
        self.game_state.pieces = ['piece1', 'piece2']
        self.game_state.is_completed = True
        saved_state = self.game_state.save_state()
        
        self.assertEqual(saved_state['score'], 100)
        self.assertEqual(saved_state['pieces'], ['piece1', 'piece2'])
        self.assertTrue(saved_state['is_completed'])

    def test_load_state(self):
        state_to_load = {
            'score': 150,
            'pieces': ['piece3', 'piece4'],
            'is_completed': False
        }
        self.game_state.load_state(state_to_load)
        
        self.assertEqual(self.game_state.score, 150)
        self.assertEqual(self.game_state.pieces, ['piece3', 'piece4'])
        self.assertFalse(self.game_state.is_completed)

if __name__ == '__main__':
    unittest.main()