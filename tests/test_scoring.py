import unittest
from src.game.scoring import Scoring

class TestScoring(unittest.TestCase):

    def setUp(self):
        self.scoring = Scoring()

    def test_initial_score(self):
        self.assertEqual(self.scoring.get_score(), 0)

    def test_score_increase(self):
        self.scoring.increase_score(10)
        self.assertEqual(self.scoring.get_score(), 10)

    def test_score_decrease(self):
        self.scoring.increase_score(20)
        self.scoring.decrease_score(5)
        self.assertEqual(self.scoring.get_score(), 15)

    def test_high_score_update(self):
        self.scoring.increase_score(50)
        self.scoring.update_high_score()
        self.assertEqual(self.scoring.get_high_score(), 50)

    def test_high_score_not_updated(self):
        self.scoring.increase_score(30)
        self.scoring.update_high_score()
        self.scoring.increase_score(20)
        self.scoring.update_high_score()
        self.assertEqual(self.scoring.get_high_score(), 50)

if __name__ == '__main__':
    unittest.main()