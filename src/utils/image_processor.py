from PIL import Image
import os

def slice_image(image_path, rows, cols):
    image = Image.open(image_path)
    img_width, img_height = image.size
    piece_width = img_width // cols
    piece_height = img_height // rows

    pieces = []
    for row in range(rows):
        for col in range(cols):
            left = col * piece_width
            upper = row * piece_height
            right = left + piece_width
            lower = upper + piece_height
            piece = image.crop((left, upper, right, lower))
            pieces.append(piece)

    return pieces

def save_pieces(pieces, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for index, piece in enumerate(pieces):
        piece.save(os.path.join(output_dir, f'piece_{index}.png'))

def load_image(image_path):
    return Image.open(image_path)

def resize_image(image, size):
    return image.resize(size, Image.ANTIALIAS)