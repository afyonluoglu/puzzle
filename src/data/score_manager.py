from typing import List, Tuple
import json
import os
import time

class ScoreManager:
    def __init__(self, max_scores=10):
        self.max_scores = max_scores
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.scores_file = os.path.join(self.data_dir, "high_scores.json")
        self.scores = self._load_scores()
    
    def _load_scores(self):
        """Load scores from file"""
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_scores(self):
        """Save scores to file"""
        with open(self.scores_file, 'w') as f:
            json.dump(self.scores, f)
    
    def add_score(self, player_name, score, puzzle_info, time_taken, hint_count, wrong_count):
        """Add a new score to the high scores"""
        new_score = {
            'player': player_name,
            'score': score,
            'puzzle': puzzle_info,
            'time': time_taken,    #time.time(),
            'date': time.strftime('%d-%m-%Y - %H:%M'),
            'hint_count': hint_count,
            'wrong_attempt_count': wrong_count,
        }
        
        self.scores.append(new_score)
        # Sort by score (highest first)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only the top scores
        if len(self.scores) > self.max_scores:
            self.scores = self.scores[:self.max_scores]
        
        self._save_scores()
        return True
    
    def get_high_scores(self):
        """Get all high scores"""
        return self.scores
    
    def get_high_score(self):
        """Get the highest score"""
        if not self.scores:
            return 0
        return self.scores[0]['score']
    
    def clear_scores_OLD(self):
        """Clear all high scores"""
        self.scores = []
        self._save_scores()