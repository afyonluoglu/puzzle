from PIL import Image
import random
import os

class PuzzleGenerator:
    def __init__(self, image_path, rows, cols):
        self.image_path = image_path
        self.rows = rows
        self.cols = cols
        self.pieces = []
        self.original_pieces = []  # Store the original pieces in correct order
        self.shuffled_pieces = []  # Store the shuffled pieces
        self.piece_to_position_map = {}  # Maps piece index to its correct position
        self.piece_size = None

    def generate_new_puzzle(self):
        """Generate a new puzzle and shuffle the pieces"""
        self.pieces = []
        self.original_pieces = []
        self.shuffled_pieces = []
        self.piece_to_position_map = {}
        
        try:
            image = Image.open(self.image_path)
            print(f"  🟢 Loaded image: {image.size}")
            
            # Make the image square and resize it to ensure equal piece sizes
            target_size = min(600, 800)  # Maximum puzzle size
            
            # Make image square by cropping/padding
            width, height = image.size
            size = min(width, height)
            
            # Crop to square from center
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            
            square_image = image.crop((left, top, right, bottom))
            print(f"  🟢 Square image : {square_image.size}")
            
            # Resize to target size ensuring it's divisible by grid dimensions
            puzzle_width = (target_size // self.cols) * self.cols
            puzzle_height = (target_size // self.rows) * self.rows
            
            resized_image = square_image.resize((puzzle_width, puzzle_height), Image.Resampling.LANCZOS)
            print(f"  🟡 Resized image: {resized_image.size}")
            
            # Calculate exact piece dimensions
            piece_width = puzzle_width // self.cols
            piece_height = puzzle_height // self.rows
            
            # Store piece size for consistent use
            self.piece_size = (piece_width, piece_height)
            
            print(f"  🟠 Puzzle size : {puzzle_width}x{puzzle_height}")
            print(f"  🔴 Piece size  : {piece_width}x{piece_height}")

            # Create pieces in correct order (0 to n-1)
            for row in range(self.rows):
                for col in range(self.cols):
                    left = col * piece_width
                    upper = row * piece_height
                    right = left + piece_width
                    lower = upper + piece_height

                    piece = resized_image.crop((left, upper, right, lower))
                    
                    # Ensure all pieces are exactly the same size
                    if piece.size != (piece_width, piece_height):
                        piece = piece.resize((piece_width, piece_height), Image.Resampling.LANCZOS)
                    
                    # Calculate the correct position index for this piece
                    correct_position = row * self.cols + col
                    
                    # Store the piece with its correct position
                    self.original_pieces.append(piece.copy())
                    
                    # Map this piece to its correct position
                    self.piece_to_position_map[len(self.original_pieces) - 1] = correct_position
            
            # Create a shuffled list of pieces for the game
            self.shuffled_pieces = self.original_pieces.copy()
            random.shuffle(self.shuffled_pieces)
            
            # Set pieces to the shuffled version
            self.pieces = self.shuffled_pieces
            
            # print(f"Created {len(self.pieces)} pieces")
            # print(f"Piece to position map: {self.piece_to_position_map}")
            
            return self.pieces
            
        except Exception as e:
            print(f"Error generating puzzle: {e}")
            return []
    
    def get_piece_size(self):
        """Return the standardized piece size"""
        return self.piece_size
    
    def get_current_state(self):
        """Return the current state of the puzzle for saving"""
        return {
            'original_pieces': self.original_pieces,
            'shuffled_pieces': self.shuffled_pieces,
            'pieces': self.pieces,
            'piece_to_position_map': self.piece_to_position_map,
            'piece_size': self.piece_size
        }
    
    def load_puzzle(self, puzzle_state):
        """Load a puzzle from saved state"""
        self.original_pieces = puzzle_state['original_pieces']
        self.shuffled_pieces = puzzle_state['shuffled_pieces']
        self.pieces = puzzle_state['pieces']
        self.piece_to_position_map = puzzle_state['piece_to_position_map']
        self.piece_size = puzzle_state.get('piece_size', (100, 100))
    
    def is_piece_in_correct_position(self, piece_idx, position_idx):
        """Check if a piece is in the correct position"""
        # Find which original piece this shuffled piece corresponds to
        if piece_idx < len(self.pieces):
            # Get the actual piece from shuffled pieces
            piece = self.pieces[piece_idx]
            
            # Find this piece in the original pieces list
            for original_idx, original_piece in enumerate(self.original_pieces):
                # Compare the pieces by converting to bytes for exact match
                if self._pieces_equal(piece, original_piece):
                    # Check if this original piece belongs in the given position
                    correct_position = self.piece_to_position_map.get(original_idx, -1)
                    return correct_position == position_idx
        
        return False
    
    def _pieces_equal(self, piece1, piece2):
        """Check if two PIL images are equal"""
        return piece1.tobytes() == piece2.tobytes()
    
    def get_pieces(self):
        """Return all puzzle pieces"""
        return self.pieces
    
    def get_piece(self, index):
        """Get a specific piece by index"""
        if 0 <= index < len(self.pieces):
            return self.pieces[index]
        return None
    
    # def is_complete(self):
    #     """Check if the puzzle is complete"""
    #     # This will be checked by the main app based on placed pieces
    #     return True  # Placeholder - actual completion check done in app
    
    def get_correct_position_for_piece(self, piece_idx):
        """Get the correct position for a given piece"""
        if piece_idx < len(self.pieces):
            piece = self.pieces[piece_idx]
            
            # Find this piece in the original pieces list
            for original_idx, original_piece in enumerate(self.original_pieces):
                if self._pieces_equal(piece, original_piece):
                    return self.piece_to_position_map.get(original_idx, -1)
        
        return -1