class PuzzlePiece:
    def __init__(self, image, position, rotation=0):
        self.image = image
        self.position = position
        self.rotation = rotation
        self.is_placed = False

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360

    def place(self, new_position):
        self.position = new_position
        self.is_placed = True

    def reset(self):
        self.is_placed = False
        self.position = None
        self.rotation = 0

    def get_image(self):
        # This method would return the image of the piece with the current rotation applied
        return self.image.rotate(self.rotation) if self.is_placed else self.image