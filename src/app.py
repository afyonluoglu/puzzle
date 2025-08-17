from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkOptionMenu, filedialog, CTkComboBox, CTkScrollableFrame, CTkImage, CTkToplevel, CTkSwitch
import os
import time
from game.puzzle_generator import PuzzleGenerator
from data.save_manager import SaveManager
from data.score_manager import ScoreManager
from utils.audio_manager import AudioManager
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw


# pip install customtkinter Pillow playsound

class JigsawPuzzleGame(CTk):
    def __init__(self):
        super().__init__()
        self.title("Jigsaw Puzzle Game")
        self.geometry("1000x800")
        self.center_window(self, width=1000, height=800)
        
        # Initialize to None and create later when user selects image
        self.puzzle_generator = None
        self.save_manager = SaveManager(self)
        self.score_manager = ScoreManager()
        self.audio_manager = AudioManager()
        
        self.current_score = 0
        self.high_score = self.score_manager.get_high_score()
        self.selected_image_path = None
        self.current_save_file = None # Track current save file for resuming games
        
        self.hint_count = 0
        self.wrong_attempt_count = 0
        self.cols_and_rows = 0

        # Track placed pieces
        self.placed_pieces = {}  # Maps position_idx to piece_idx
        self.total_pieces = 0
        
        self.create_widgets()
        self.audio_manager.play_background_music()

    def clear_scr_and_create_widgets(self):
        """Clear the main frame and recreate widgets"""
        if hasattr(self, 'target_window'):
            self.target_window.destroy()   

        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.destroy()
        
        # Recreate widgets
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = CTkLabel(self.main_frame, text="Welcome to Jigsaw Puzzle Game", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.start_button = CTkButton(self.main_frame, text="Start New Game", command=self.setup_new_game, hover_color="#008628")
        self.start_button.pack(pady=10)

        self.continue_button = CTkButton(self.main_frame, text="Continue Saved Game", command=self.continue_game, hover_color="#E59438")
        self.continue_button.pack(pady=10)

        self.high_score_label = CTkLabel(
            self.main_frame, 
            text=f"    High Score: {self.high_score}    ", 
            font=("Arial", 18), 
            fg_color=("#003785", "#006006"), 
            text_color=("#B1F98F", "#FF9191"),
            corner_radius=10,
        )
        self.high_score_label.pack(pady=10, padx=10)

        self.high_scores_button = CTkButton(self.main_frame, text="High Scores", command=self.show_high_scores, hover_color="#A80000")
        self.high_scores_button.pack(pady=10)

        self.quit_button = CTkButton(self.main_frame, text="Quit", command=self.quit, fg_color="#606060", text_color="white", hover_color="#000000")
        self.quit_button.pack(pady=10)

        
    def setup_new_game(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Create setup frame
        setup_label = CTkLabel(self.main_frame, text="Setup New Game", font=("Arial", 20))
        setup_label.pack(pady=20)
        
        # Image selection
        image_frame = CTkFrame(self.main_frame)
        image_frame.pack(pady=10, fill="x", padx=20)
        
        image_label = CTkLabel(image_frame, text="Select Image:")
        image_label.pack(side="left", padx=10)
        
        self.image_path_label = CTkLabel(image_frame, text="❗ No image selected", width=300)
        self.image_path_label.pack(side="left", padx=10)
        
        browse_button = CTkButton(image_frame, text="Browse", command=self.browse_image)
        browse_button.pack(side="left", padx=10)
        
        # Grid size selection
        grid_frame = CTkFrame(self.main_frame)
        grid_frame.pack(pady=10, fill="x", padx=20)
        
        grid_label = CTkLabel(grid_frame, text="Grid Size:")
        grid_label.pack(side="left", padx=10)
        
        self.grid_sizes = ["3x3", "4x4", "5x5", "6x6", "8x8", "10x10","14x14"]
        self.grid_combobox = CTkComboBox(grid_frame, values=self.grid_sizes)
        self.grid_combobox.set("4x4")
        self.grid_combobox.pack(side="left", padx=10)
        
        # Start button
        start_game_button = CTkButton(self.main_frame, text="Start Game", command=self.start_new_game)
        start_game_button.pack(pady=20)
        
        # Back button
        back_button = CTkButton(self.main_frame, text="Back to Main Menu", command=self.clear_scr_and_create_widgets)
        back_button.pack(pady=10)

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            self.selected_image_path = file_path
            # Display only the filename, not the full path
            filename = os.path.basename(file_path)
            self.image_path_label.configure(text=filename)
            self.show_image_crop_preview(file_path)            

    def show_image_crop_preview(self, file_path):
        pil_image = Image.open(file_path)
        width, height = pil_image.size

        # Eğer kare değilse, kullanıcıya kırpma yönünü sor
        if width != height:
            # Kırpma yönünü seçmek için yeni bir pencere aç
            self.grab_release()

            crop_window = CTkToplevel(self)
            crop_window.title("Crop Image")
            # crop_window.geometry("500x600")
            self.center_window(crop_window, width=500, height=600)

            crop_window.deiconify()  				# Pencereyi göster
            crop_window.attributes('-topmost', True)  	# En üste getir
            crop_window.focus_force()  				# Focus ver


            info_label = CTkLabel(crop_window, text="Image is not square. Choose crop direction:", font=("Arial", 14))
            info_label.pack(pady=10)

            preview_label = CTkLabel(crop_window, text="")
            preview_label.pack(pady=10)

            crop_direction = {"value": "vertical" if height > width else "horizontal"}

            def update_preview():
                w, h = pil_image.size
                if crop_direction["value"] == "vertical":
                    size = w
                    left = 0
                    top = (h - w) // 2
                    right = w
                    bottom = top + w
                else:
                    size = h
                    left = (w - h) // 2
                    top = 0
                    right = left + h
                    bottom = h

                cropped = pil_image.crop((left, top, right, bottom)).resize((400, 400), Image.Resampling.LANCZOS)
                draw = ImageDraw.Draw(cropped)
                draw.rectangle([0, 0, 399, 399], outline="red", width=4)
                ctk_image = CTkImage(light_image=cropped, dark_image=cropped, size=(400, 400))
                preview_label.configure(image=ctk_image)
                preview_label.image = ctk_image

            def set_vertical():
                crop_direction["value"] = "vertical"
                update_preview()

            def set_horizontal():
                crop_direction["value"] = "horizontal"
                update_preview()

            btn_frame = CTkFrame(crop_window)
            btn_frame.pack(pady=10)
            vertical_btn = CTkButton(btn_frame, text="Vertical Crop", command=set_vertical)
            vertical_btn.pack(side="left", padx=10)
            horizontal_btn = CTkButton(btn_frame, text="Horizontal Crop", command=set_horizontal)
            horizontal_btn.pack(side="left", padx=10)

            def confirm_crop():
                w, h = pil_image.size
                if crop_direction["value"] == "vertical":
                    size = w
                    left = 0
                    top = (h - w) // 2
                    right = w
                    bottom = top + w
                else:
                    size = h
                    left = (w - h) // 2
                    top = 0
                    right = left + h
                    bottom = h
                cropped = pil_image.crop((left, top, right, bottom))
                # Geçici olarak cropped image'ı kaydet ve yolunu güncelle
                temp_path = os.path.join(os.path.dirname(file_path), "cropped_preview_temp.png")
                cropped.save(temp_path)
                self.selected_image_path = temp_path
                crop_window.destroy()
                self.image_path_label.configure(text=os.path.basename(temp_path))

            confirm_btn = CTkButton(crop_window, text="Confirm Crop", command=confirm_crop)
            confirm_btn.pack(pady=20)

            update_preview()
        else:
            # Kare ise önizleme göster
            preview_window = CTkToplevel(self)
            preview_window.title("Image Preview")
            preview_window.geometry("420x420")
            cropped = pil_image.resize((400, 400), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(cropped)
            draw.rectangle([0, 0, 399, 399], outline="red", width=4)
            ctk_image = CTkImage(light_image=cropped, dark_image=cropped, size=(400, 400))
            preview_label = CTkLabel(preview_window, image=ctk_image, text="")
            preview_label.image = ctk_image
            preview_label.pack(expand=True, fill="both", padx=10, pady=10)
        pil_image.close()  


    def start_new_game(self):
        if not self.selected_image_path:
            self.show_message("Please select an image first!")
            return
        
        # Parse grid size
        grid_size = self.grid_combobox.get()
        rows, cols = map(int, grid_size.split("x"))
        self.cols_and_rows = rows
        
        # Create puzzle generator with selected options
        self.puzzle_generator = PuzzleGenerator(
            image_path=self.selected_image_path,
            rows=rows,
            cols=cols
        )
        
        self.puzzle_generator.generate_new_puzzle()
        self.current_score = 0
        self.wrong_attempt_count = 0
        self.hint_count = 0
        self.current_save_file = None  # Reset current save filename
        
        # Initialize tracking variables
        self.placed_pieces = {}
        self.total_pieces = rows * cols
        
        self.show_game_screen()

    def center_window(self, window, width=None, height=None):
        """Bir Toplevel penceresini ekranın ortasına yerleştirir."""
        window.update_idletasks() # Pencere boyutlarının hesaplanmasını bekle
        w = width or window.winfo_width()
        h = height or window.winfo_height()
        ws = window.winfo_screenwidth() # Ekran genişliği
        hs = window.winfo_screenheight() # Ekran yüksekliği
        # Ortalanmış x ve y koordinatlarını hesapla
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # Pencereyi konumlandır
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        window.deiconify() # Gizlenmişse göster

    def continue_game(self):
        # Oyun kayıtlarının bulunduğu klasörü belirle
        tmp1 = os.path.dirname(os.path.dirname(__file__))
        save_dir = os.path.join(tmp1, "src\\saves")
        print(f"🔄 Save directory: {save_dir}")
        if not os.path.exists(save_dir):
            print("🔄 Creating save directory...")
            os.makedirs(save_dir)

        # Kayıtlı pkl dosyalarını bul
        save_files = [f for f in os.listdir(save_dir) if f.endswith(".pkl")]
        if not save_files:
            self.show_message("No saved game found.")
            return
        print(f"🔄 Found saved game files: {save_files}")

        # Modal grab'ı geçici olarak kaldır
        self.grab_release()

        # Seçim penceresi oluştur
        select_window = CTkToplevel(self)
        select_window.title("Select Saved Game")
        # select_window.geometry("400x250")
        self.center_window(select_window, width=400, height=250)

        select_window.deiconify()  # Pencereyi göster
        select_window.attributes('-topmost', True)  # En üste getir
        select_window.focus_force()  # Focus ver

        label = CTkLabel(select_window, text="Choose a saved game to continue:", font=("Arial", 14))
        label.pack(pady=10)

        # Liste kutusu
        from tkinter import Listbox
        listbox = Listbox(select_window, height=10, font=("Arial", 12))
        for f in save_files:
            listbox.insert("end", f)
        listbox.pack(pady=10, fill="x", padx=20)

        def on_double_click(event):
            load_selected_game()

        listbox.bind("<Double-Button-1>", on_double_click)

        def load_selected_game():
            selection = listbox.curselection()
            select_window.destroy()
            if not selection:
                self.show_message("Please select a saved game file!")
                return
            game_file = save_files[selection[0]]

            game_data = self.save_manager.load_game(os.path.join(save_dir, game_file))

            if game_data:
                self.current_save_file = self.save_manager.save_file  # Devam edilen oyunun dosya adı
                # Recreate puzzle generator with saved data
                self.puzzle_generator = PuzzleGenerator(
                    image_path=game_data['image_path'],
                    rows=game_data['rows'],
                    cols=game_data['cols']
                )
                self.cols_and_rows = game_data['rows']
                self.puzzle_generator.load_puzzle(game_data['puzzle'])
                self.current_score = game_data['score']
                self.placed_pieces = game_data.get('placed_pieces', {}) 
                self.total_pieces = game_data['rows'] * game_data['cols']     
                self.hint_count = game_data.get('hint_count', 0)
                self.wrong_attempt_count = game_data.get('wrong_attempt_count', 0)
                self.show_game_screen()

        load_btn = CTkButton(select_window, text="Load Selected Game", command=load_selected_game)
        load_btn.pack(pady=10)

    def show_game_screen(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Stop background music when game starts
        self.audio_manager.stop_background_music()
                    
        # Create a game frame that contains everything
        self.game_frame = CTkFrame(self.main_frame)
        self.game_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header with game info
        header_frame = CTkFrame(self.game_frame)
        header_frame.pack(fill="x", pady=5)
        
        game_label = CTkLabel(header_frame, text="Jigsaw Puzzle Game", font=("Arial", 16))
        game_label.pack(side="left", padx=10)
        
        self.score_label = CTkLabel(header_frame, text=f"Score: {self.current_score}", font=("Arial", 14))
        self.score_label.pack(side="right", padx=10)
        
        self.hint_label = CTkLabel(header_frame, text=f"Hints Used: {self.hint_count}", font=("Arial", 12))
        self.hint_label.pack(side="right", padx=10)
        self.wrong_label = CTkLabel(header_frame, text=f"Wrong Attempts: {self.wrong_attempt_count}", font=("Arial", 12))
        self.wrong_label.pack(side="right", padx=10)

        # Add game controls at the top for better visibility
        controls_frame = CTkFrame(self.game_frame)
        controls_frame.pack(fill="x", pady=5)
        
        hint_button = CTkButton(controls_frame, text="Hint", command=self.give_hint, width=80, height=30)
        hint_button.pack(side="left", padx=5)
        
        save_button = CTkButton(controls_frame, text="Save Game", command=self.save_game, width=80, height=30)
        save_button.pack(side="left", padx=5)
        
        menu_button = CTkButton(controls_frame, text="Back to Menu", command=self.clear_scr_and_create_widgets, width=80, height=30)
        menu_button.pack(side="left", padx=5)
        
        show_target_button = CTkButton(controls_frame, text="Hedefi Göster", command=self.show_target_image, width=120, height=30)
        show_target_button.pack(side="left", padx=5)

        # Main game area with two sections: puzzle board and piece tray
        game_area = CTkFrame(self.game_frame)
        game_area.pack(fill="both", expand=True, pady=5)
        
        # Left side: Puzzle board (where pieces should be placed)
        # Reduce the width to make more room for the tray
        self.board_frame = CTkFrame(game_area)
        self.board_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Right side: Piece tray (where unplaced pieces are)
        # Give the tray a minimum width to ensure it's visible
        self.tray_frame = CTkFrame(game_area, width=340)
        self.tray_frame.pack(side="right", fill="both", padx=5)
        self.tray_frame.pack_propagate(False)  # Prevent shrinking
        
        # Create the puzzle board grid
        self.create_puzzle_board()
        
        # Create the piece tray with shuffled pieces
        self.create_piece_tray()
        
        # Start timer if it's a new game
        self.start_time = time.time()

        # Eğer kaydedilmiş yerleştirilmiş parçalar varsa onları tahtaya yerleştir
        # if hasattr(self.puzzle_generator, "placed_pieces"):
        for position_idx, piece_idx in self.placed_pieces.items():
            self.place_piece_in_slot(piece_idx, position_idx)        

    def show_target_image(self):
        """Show the original image in a new window"""
        if not self.puzzle_generator or not self.puzzle_generator.image_path:
            self.show_message("No target image available!")
            print("❗❗ No target image available!")
            return

        # Varsayılan olarak ızgara açık olsun
        self.show_grid = False

        def redraw_image():
            try:
                pil_image = Image.open(self.puzzle_generator.image_path)
                width, height = pil_image.size
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                right = left + size
                bottom = top + size
                square_image = pil_image.crop((left, top, right, bottom))
                target_size = min(600, 800)
                puzzle_width = (target_size // self.cols_and_rows) * self.cols_and_rows
                puzzle_height = (target_size // self.cols_and_rows) * self.cols_and_rows
                resized_image = square_image.resize((puzzle_width, puzzle_height), Image.Resampling.LANCZOS)

                if self.show_grid:
                    draw = ImageDraw.Draw(resized_image)
                    line_color = (99, 193, 255)
                    line_width = 2
                    # Dikey çizgiler
                    for i in range(self.cols_and_rows + 1):
                        x = i * (resized_image.width // self.cols_and_rows)
                        draw.line([(x, 0), (x, resized_image.height)], fill=line_color, width=line_width)
                    # Yatay çizgiler
                    for i in range(self.cols_and_rows + 1):
                        y = i * (resized_image.height // self.cols_and_rows)
                        draw.line([(0, y), (resized_image.width, y)], fill=line_color, width=line_width)

                ctk_image = CTkImage(light_image=resized_image, dark_image=resized_image, size=resized_image.size)
                image_label.configure(image=ctk_image)
                image_label.image = ctk_image
                pil_image.close()
            except Exception as e:
                self.show_message(f"Hedef görüntü gösterilemedi: {e}")


        self.grab_release()  # Modal grab'ı geçici olarak kaldır

        self.target_window = CTkToplevel(self)
        self.target_window.title("Hedef Görüntü")
        self.target_window.geometry("600x670")

        self.target_window.deiconify()  				# Pencereyi göster
        self.target_window.attributes('-topmost', True)  	# En üste getir
        self.target_window.focus_force()  				# Focus ver

        image_label = CTkLabel(self.target_window, text="")
        image_label.pack(expand=True, fill="both", padx=10, pady=10)

        # Switch ekle
        def on_switch():
            self.show_grid = grid_switch.get()
            redraw_image()

        grid_switch = CTkSwitch(
            self.target_window, 
            text="Izgara Göster", 
            command=on_switch)
        grid_switch.pack(pady=10)
        grid_switch.deselect()  # Varsayılan olarak kapalı

        redraw_image()

    def create_puzzle_board(self):
        """Create the grid where puzzle pieces should be placed"""
        self.board_slots = {}
        
        # Get puzzle dimensions
        rows = self.puzzle_generator.rows
        cols = self.puzzle_generator.cols
        
        # Get the standardized piece size from puzzle generator
        piece_size = self.puzzle_generator.get_piece_size()
        if piece_size:
            slot_width, slot_height = piece_size
        else:
            # Fallback if piece size not available
            slot_width = slot_height = 80
        
        # Calculate total board size
        board_width = cols * slot_width
        board_height = rows * slot_height
        
        print(f"✨ Creating board: {board_width}x{board_height} with {rows}x{cols} slots of {slot_width}x{slot_height}")
        
        # Create a container frame to hold the grid with fixed size
        self.grid_container = CTkFrame(self.board_frame, width=board_width, height=board_height)
        self.grid_container.pack(pady=10, padx=10)
        self.grid_container.pack_propagate(False)  # Keep size fixed
        self.grid_container.grid_propagate(False)  # Prevent grid from changing container size
        
        # Configure grid weights to maintain equal distribution
        for i in range(cols):
            self.grid_container.columnconfigure(i, weight=1, minsize=slot_width)
        for i in range(rows):
            self.grid_container.rowconfigure(i, weight=1, minsize=slot_height)
        
        # Create a slot for each position in the grid
        for row in range(rows):
            for col in range(cols):
                # Create a frame for this slot with exact piece dimensions
                slot_frame = CTkFrame(
                    self.grid_container, 
                    width=slot_width,
                    height=slot_height,
                    border_width=1,
                    border_color="#bebebe",
                    fg_color=("gray90", "gray30"),
                    corner_radius=0  # Sharp corners
                )
                slot_frame.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                slot_frame.grid_propagate(False)  # Keep the size fixed
                slot_frame.pack_propagate(False)  # Prevent internal widgets from changing size
                
                # Store the slot by its position
                position_idx = row * cols + col
                self.board_slots[position_idx] = slot_frame
                
                # Add position number in small text 
                pos_label = CTkLabel(
                    slot_frame, 
                    text=f"{position_idx}", 
                    font=("Arial", 8),
                    text_color="gray60"
                )
                pos_label.place(x=2, y=2)
                
                # Bind the slot to receive pieces
                slot_frame.bind("<Button-1>", lambda e, pos=position_idx: self.slot_clicked(pos))
                        
    def create_piece_tray(self):
        """Create the tray with shuffled puzzle pieces"""
        # Get pieces from the puzzle generator
        pieces = self.puzzle_generator.get_pieces()
        
        if not pieces:
            print("❗❗ No pieces found from puzzle generator!")
            return
        
        # print(f"🚩 Creating tray with {len(pieces)} pieces")

        # Create a scrollable frame for the pieces
        tray_scroll = CTkScrollableFrame(self.tray_frame)
        tray_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Use consistent piece size for tray pieces (smaller than actual)
        # Tray'in toplam boyutu için "show_game_screen" metodunda "tray_frame" genişliğini artır
        tray_piece_size = 90  # Increased size for better visibility
        
        # Create a label for each piece
        self.piece_buttons = []
        for i, piece in enumerate(pieces):
            try:
                # Convert PIL image to CTkImage (smaller size for tray)
                tk_image = self.pil_to_ctk_image(piece, size=(tray_piece_size, tray_piece_size))
                
                # Create a frame to hold the piece for better control
                piece_frame = CTkFrame(tray_scroll, width=tray_piece_size+10, height=tray_piece_size+10)
                piece_frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
                piece_frame.grid_propagate(False)
                
                # Create a label with the piece image
                piece_label = CTkLabel(piece_frame, image=tk_image, text="")
                piece_label.image = tk_image  # Keep a reference
                piece_label.pack(fill="both", expand=True, padx=2, pady=2)
                
                # Make it draggable
                piece_label.bind("<ButtonPress-1>", lambda event, idx=i: self.start_drag(event, idx))
                piece_label.bind("<B1-Motion>", self.drag)
                piece_label.bind("<ButtonRelease-1>", self.drop)
                
                # Also make the frame draggable
                piece_frame.bind("<ButtonPress-1>", lambda event, idx=i: self.start_drag(event, idx))
                piece_frame.bind("<B1-Motion>", self.drag)
                piece_frame.bind("<ButtonRelease-1>", self.drop)
                
                self.piece_buttons.append({
                    'label': piece_label,
                    'frame': piece_frame,
                    'piece_idx': i,
                    'selected': False,
                    'placed': False
                })
                
                # print(f"🚩 Created piece {i} in tray")
                
            except Exception as e:
                print(f"❗ Error creating piece {i}: {e}")
    
        # Configure grid weights for the tray
        for i in range(3):  # 3 columns
            tray_scroll.columnconfigure(i, weight=1)
    
        # Initialize drag variables
        self.drag_data = {"x": 0, "y": 0, "item": None, "piece_idx": None}
        
        print(f"🚩 Tray created with {len(self.piece_buttons)} piece buttons")

    def pil_to_ctk_image(self, pil_image, size=(100, 100)):
        """Convert PIL Image to CTkImage for display in CTkButton/CTkLabel"""
        try:
            # Ensure the image is in RGB mode
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Resize the image to fit in the display area
            resized_image = pil_image.resize(size, Image.Resampling.LANCZOS)
            
            # Convert to CTkImage
            ctk_image = CTkImage(light_image=resized_image, dark_image=resized_image, size=size)
            return ctk_image
        except Exception as e:
            print(f"Error converting PIL image to CTkImage: {e}")
            # Return a placeholder image if conversion fails
            from PIL import Image as PILImage
            placeholder = PILImage.new('RGB', size, color='gray')
            return CTkImage(light_image=placeholder, dark_image=placeholder, size=size)

    def start_drag(self, event, piece_idx):
        """Begin dragging a puzzle piece"""
        # Don't drag if already placed
        for piece in self.piece_buttons:
            if piece['piece_idx'] == piece_idx and piece['placed']:
                return
        
        # print(f"Starting drag for piece {piece_idx}")
        
        # Get the piece info
        self.drag_data["piece_idx"] = piece_idx
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
        # Mark this piece as selected
        for piece in self.piece_buttons:
            if piece['selected']:
                piece['label'].configure(fg_color=("gray85", "gray25"))  # Reset to default colors
                piece['selected'] = False
            
            if piece['piece_idx'] == piece_idx:
                piece['selected'] = True
                piece['label'].configure(fg_color="light blue")  # Highlight with color
    
        # Create a floating preview of the piece
        self.create_drag_image(event, piece_idx)

    def create_drag_image(self, event, piece_idx):
        """Create a floating image of the piece being dragged"""
        piece = self.puzzle_generator.get_piece(piece_idx)
        tk_image = self.pil_to_ctk_image(piece, size=(80, 80))
    
        # Create a toplevel window for the dragged piece
        if hasattr(self, 'drag_window') and self.drag_window:
            self.drag_window.destroy()
    
        self.drag_window = CTkToplevel(self)
        self.drag_window.overrideredirect(True)  # No window decorations
        self.drag_window.attributes('-topmost', True)  # Keep on top
        self.drag_window.attributes('-alpha', 0.7)  # Make it semi-transparent
    
        # Add the image to the window
        drag_label = CTkLabel(self.drag_window, image=tk_image, text="")
        drag_label.image = tk_image
        drag_label.pack()
    
        # Position the window at the cursor
        x = self.winfo_pointerx() - 40  # Center the image on cursor
        y = self.winfo_pointery() - 40
        self.drag_window.geometry(f"80x80+{x}+{y}")

    def drag(self, event):
        """Handle dragging the piece"""
        if not hasattr(self, 'drag_window') or not self.drag_window:
            return
    
        # Move the drag window with the cursor
        x = self.winfo_pointerx() - 40
        y = self.winfo_pointery() - 40
        self.drag_window.geometry(f"80x80+{x}+{y}")

    def drop(self, event):
        """Handle dropping the piece"""
        if not hasattr(self, 'drag_window') or not self.drag_window:
            return
        
        piece_idx = self.drag_data["piece_idx"]
        
        # Close the drag window first
        self.drag_window.destroy()
        self.drag_window = None
        
        # Update the window to ensure coordinates are current
        self.update_idletasks()
        
        # Get mouse position relative to the grid container
        mouse_x = self.winfo_pointerx() - self.grid_container.winfo_rootx()
        mouse_y = self.winfo_pointery() - self.grid_container.winfo_rooty()
        
        # print(f"Mouse position relative to grid: {mouse_x}, {mouse_y}")
        
        # Check if we're over a slot in the board
        found_slot = False
        for position_idx, slot in self.board_slots.items():
            # Calculate slot position relative to grid container
            slot_x = slot.winfo_x()
            slot_y = slot.winfo_y()
            slot_width = slot.winfo_width()
            slot_height = slot.winfo_height()
            
            # Check if the mouse is inside this slot
            if (slot_x <= mouse_x <= slot_x + slot_width and
                slot_y <= mouse_y <= slot_y + slot_height):
                
                print(f"✅ Found slot {position_idx} for piece {piece_idx}")
                found_slot = True
                
                # Check if this is the correct position
                is_correct = self.puzzle_generator.is_piece_in_correct_position(piece_idx, position_idx)
                
                # print(f"Is piece {piece_idx} correct for position {position_idx}? {is_correct}")
                
                if is_correct:
                    # Place the piece in the slot
                    self.place_piece_in_slot(piece_idx, position_idx)
                    
                    # Update score
                    self.current_score += 10
                    self.score_label.configure(text=f"Score: {self.current_score}")
                    
                    # Play sound effect
                    self.audio_manager.play_sound_effect('piece_placed')
                    
                    # Check if puzzle is complete
                    if self.is_puzzle_complete():
                        self.puzzle_completed()
                        return
                else:
                    # Wrong position - show feedback
                    self.wrong_attempt_count += 1
                    self.wrong_label.configure(text=f"Wrong Attempts: {self.wrong_attempt_count}")                    
                    print(f"❗ Piece {piece_idx} dropped in wrong slot {position_idx}")
                    # self.show_message("That's not the right spot for this piece!")
                
                break
        
        # if not found_slot:
            # print("No slot found at drop position")

    def give_hint(self):
        """Provide a hint to the player by placing a selected piece in its correct position"""
        # Find a piece that's selected
        selected_piece = None
        for piece in self.piece_buttons:
            if piece['selected']:
                selected_piece = piece['piece_idx']
                break
        
        if selected_piece is None:
            self.show_message("Select a piece first to get a hint!")
            return
        
        print(f"🎉 Giving hint for piece {selected_piece}")
        
        # Check if piece is already placed
        for piece in self.piece_buttons:
            if piece['piece_idx'] == selected_piece and piece['placed']:
                self.show_message("This piece is already placed correctly!")
                return
        
        # Find the correct position for this piece
        correct_position = self.puzzle_generator.get_correct_position_for_piece(selected_piece)
        
        if correct_position != -1:
            print(f"  ➡️ Correct position is {correct_position}")
            
            # Check if the slot is already occupied
            if correct_position in self.placed_pieces:
                self.show_message("❗ The correct slot is already occupied!")
                return
            
            # Highlight the correct slot first
            slot = self.board_slots[correct_position]
            
            # Create a temporary colored frame inside the slot
            hint_frame = CTkFrame(slot, fg_color="green", corner_radius=0)
            hint_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            
            # Flash the hint frame briefly before placing the piece
            def flash_and_place(count):
                if count <= 0:
                    hint_frame.destroy()
                    # Actually place the piece in the correct slot
                    self.place_piece_in_slot(selected_piece, correct_position)
                    
                    # Update score
                    self.current_score += 10
                    self.score_label.configure(text=f"Score: {self.current_score}")
                    
                    # Play sound effect
                    self.audio_manager.play_sound_effect('piece_placed')
                    
                    # Check if puzzle is complete
                    if self.is_puzzle_complete():
                        self.puzzle_completed()
                else:
                    if hint_frame.winfo_exists():  # Check if widget still exists
                        visible = count % 2 == 0
                        if visible:
                            hint_frame.configure(fg_color="green")
                        else:
                            hint_frame.configure(fg_color="transparent")
                        self.after(200, lambda: flash_and_place(count - 1))
            
            # Start flashing and then place the piece
            flash_and_place(4)  # Flash fewer times before placing
            
            # Play hint sound
            self.audio_manager.play_sound_effect('hint_used')
            
            self.hint_count += 1            
            self.hint_label.configure(text=f"Hints Used: {self.hint_count}")
            # Show message
            self.show_message("Hint: Placing piece in the correct slot!")
        else:
            self.show_message("Couldn't find the correct position for this piece!")

    def save_game(self):
        if self.puzzle_generator:
            game_data = {
                'puzzle': self.puzzle_generator.get_current_state(),
                'score': self.current_score,
                'image_path': self.puzzle_generator.image_path,
                'rows': self.puzzle_generator.rows,
                'cols': self.puzzle_generator.cols,
                'placed_pieces': self.placed_pieces,
                'hint_count': self.hint_count,
                'wrong_attempt_count': self.wrong_attempt_count                
            }
            self.save_manager.sm_save_game(game_data)

        else:
            self.show_message("No game in progress to save!")

    def show_message(self, message):
        messagebox.showinfo("💫 Jigsaw Puzzle Game", message)

    def piece_selected(self, piece_idx):
        """Handle when a piece is selected from the tray"""
        # First, unselect any previously selected piece
        for piece in self.piece_buttons:
            if piece['selected']:
                piece['label'].configure(fg_color=("gray85", "gray25"))  # Reset to default colors
                piece['selected'] = False
        
        # Mark this piece as selected
        for piece in self.piece_buttons:
            if piece['piece_idx'] == piece_idx:
                piece['label'].configure(fg_color="light blue")  # Highlight with color
                piece['selected'] = True
                self.selected_piece = piece_idx
                break

    def slot_clicked(self, position_idx):
        """Handle when a board slot is clicked"""
        # Check if a piece is selected
        selected_piece = None
        for piece in self.piece_buttons:
            if piece['selected']:
                selected_piece = piece
                break
    
        if not selected_piece:
            self.show_message("Select a puzzle piece first!")
            return
    
        # Try to place the piece
        piece_idx = selected_piece['piece_idx']
    
        # Check if this is the correct position
        is_correct = self.puzzle_generator.is_piece_in_correct_position(piece_idx, position_idx)
    
        if is_correct:
            # Place the piece in the slot
            self.place_piece_in_slot(piece_idx, position_idx)
            
            # Update score
            self.current_score += 10
            self.score_label.configure(text=f"Score: {self.current_score}")
            
            # Play sound effect
            self.audio_manager.play_sound_effect('piece_placed')
            
            # Check if puzzle is complete
            if self.is_puzzle_complete():
                self.puzzle_completed()
        else:
            # Wrong position - shake or show feedback
            self.wrong_attempt_count += 1
            self.wrong_label.configure(text=f"Wrong Attempts: {self.wrong_attempt_count}")     
            self.show_message("That's not the right spot for this piece!")

    def place_piece_in_slot(self, piece_idx, position_idx):
        """Place a piece in a board slot and remove from tray"""
        # Get the piece image
        piece = self.puzzle_generator.get_piece(piece_idx)
        
        # Clear any existing content in the slot (except position label)
        slot = self.board_slots[position_idx]
        for widget in slot.winfo_children():
            if isinstance(widget, CTkLabel) and widget.cget("text") and widget.cget("text").isdigit():
                continue  # Keep position label
            widget.destroy() 
        
        # Get exact piece dimensions from puzzle generator
        piece_size = self.puzzle_generator.get_piece_size()
        if piece_size:
            piece_width, piece_height = piece_size
        else:
            piece_width = piece_height = 80
        
        # Create piece image with exact dimensions (no padding)
        # tk_image = self.pil_to_ctk_image(piece, size=(piece_width-4, piece_height-4))  # Slightly smaller to fit with border
        tk_image = self.pil_to_ctk_image(piece, size=(piece_width, piece_height))  
        

        # Add image to the slot with exact fit
        piece_label = CTkLabel(slot, image=tk_image, text="")
        piece_label.image = tk_image  
        piece_label.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Track this placement
        self.placed_pieces[position_idx] = piece_idx
        
        # Mark the piece as placed in the tray and hide it
        for i, p in enumerate(self.piece_buttons):
            if p['piece_idx'] == piece_idx:
                # Hide the piece from tray instead of just disabling
                p['frame'].grid_remove()  # Remove from grid but keep the widget
                p['selected'] = False
                p['placed'] = True
                break
    
        print(f"  🔸 Placed piece {piece_idx} in slot {position_idx}")

    def is_puzzle_complete(self):
        """Check if all pieces are correctly placed"""
        if len(self.placed_pieces) != self.total_pieces:
            return False
        
        # Check if all placed pieces are in correct positions
        for position_idx, piece_idx in self.placed_pieces.items():
            if not self.puzzle_generator.is_piece_in_correct_position(piece_idx, position_idx):
                return False
        
        return True

    def puzzle_completed(self):
        """Handle when the puzzle is completed"""
        # Calculate time taken
        end_time = time.time()
        time_taken = end_time - self.start_time
        self.last_time_taken = time_taken 
        
        # Show completion message
        message = f"Congratulations! You completed the puzzle!\n\n" \
                  f"Score: {self.current_score}\n" \
                  f"Time: {int(time_taken)} seconds"
        
        # Play completion sound
        self.audio_manager.play_sound_effect('level_complete')
        
        # Show message and ask for name
        messagebox.showinfo("Puzzle Completed!", message)
        
        # Ask for player name for high score
        self.ask_for_player_name()

    def ask_for_player_name(self):
        """Ask for player name to save high score"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
        name_frame = CTkFrame(self.main_frame)
        name_frame.pack(pady=100)
    
        name_label = CTkLabel(name_frame, text="Enter your name for the high score:", font=("Arial", 16))
        name_label.pack(pady=10)
    
        name_entry = CTkEntry(name_frame, width=200)
        name_entry.pack(pady=10)
        name_entry.focus()
    
        submit_button = CTkButton(name_frame, text="Submit", 
                                 command=lambda: self.save_high_score(name_entry.get()))
        submit_button.pack(pady=10)

    def save_high_score(self, player_name):
        """Save the high score with player name"""
        if not player_name:
            player_name = "Anonymous"
    
        # Prepare puzzle info
        puzzle_info = f"{self.puzzle_generator.rows}x{self.puzzle_generator.cols} " + \
                      os.path.basename(self.puzzle_generator.image_path)
    
        # Add score to high scores
        print(f"Oyun Süresi: {self.last_time_taken} saniye")
        self.score_manager.add_score(
            player_name, 
            self.current_score,
            puzzle_info,
            int(self.last_time_taken),
            self.hint_count,
            self.wrong_attempt_count            
        )
    
        # Show high scores
        self.show_high_scores()

    def show_high_scores(self):
        """Display high scores screen"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
        high_scores_frame = CTkFrame(self.main_frame)
        high_scores_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
        title_label = CTkLabel(high_scores_frame, text="High Scores Table", font=("Arial", 24))
        title_label.pack(pady=20)
    
        scores = self.score_manager.get_high_scores()
    
        if not scores:
            no_scores_label = CTkLabel(high_scores_frame, text="No high scores yet!")
            no_scores_label.pack(pady=40)
        else:
            col_widths = [30, 135, 50, 215, 75, 50, 50, 165]  # Widths for each column
            # Create a table-like display
            headers = ["Rank", "Player", "Score", "Puzzle Size & File Name", "Duration", "Hints", "Wrongs", "Date-Time"]
            header_frame = CTkFrame(high_scores_frame)
            header_frame.pack(fill="x", padx=20, pady=5)
            
            for i, header in enumerate(headers):
                header_label = CTkLabel(header_frame, text=header, width=col_widths[i]-10, font=("Arial", 14, "bold"))
                header_label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            
            scores_frame = CTkScrollableFrame(high_scores_frame, height=500)
            scores_frame.pack(fill="x", padx=20, pady=20)
            
            for i, score in enumerate(scores):
                bg_color1 = "lightblue" if i % 2 == 0 else "#6ab7d8"
                bg_color2 = "lightgray" if i % 2 == 0 else "#A4A4A4"

                rank_label = CTkLabel(scores_frame, text=f"{i+1}", width=col_widths[0], fg_color=bg_color1)
                rank_label.grid(row=i, column=0, padx=2, sticky="w")

                player_label = CTkLabel(scores_frame, text=score['player'], width=col_widths[1], fg_color=bg_color2, anchor="w", justify="left" )
                player_label.grid(row=i, column=1, padx=2, sticky="w")

                score_label = CTkLabel(scores_frame, text=str(score['score']), width=col_widths[2], fg_color=bg_color1)
                score_label.grid(row=i, column=2, padx=2, sticky="w")

                puzzle_label = CTkLabel(scores_frame, text=score['puzzle'], width=col_widths[3], fg_color=bg_color2, anchor="w", justify="left" )
                puzzle_label.grid(row=i, column=3, padx=2, sticky="e")

                time_label = CTkLabel(scores_frame, text=f"{score.get('time', '-')} sn.", width=col_widths[4], fg_color=bg_color1)
                time_label.grid(row=i, column=4, padx=2, sticky="w")

                hint_label = CTkLabel(scores_frame, text=f"{score.get('hint_count', 0)}", width=col_widths[5], fg_color=bg_color2)
                hint_label.grid(row=i, column=5, padx=2, sticky="w")

                wrong_label = CTkLabel(scores_frame, text=f"{score.get('wrong_attempt_count', 0)}", width=col_widths[6], fg_color=bg_color1)
                wrong_label.grid(row=i, column=6, padx=2, sticky="w")

                date_label = CTkLabel(scores_frame, text=score['date'], width=col_widths[7], fg_color=bg_color2)
                date_label.grid(row=i, column=7, padx=2, sticky="w")

        menu_button = CTkButton(high_scores_frame, text="Back to Main Menu", command=self.clear_scr_and_create_widgets)
        menu_button.pack(pady=10)


# Add this at the end of your file after all class methods
if __name__ == "__main__":
    app = JigsawPuzzleGame()
    app.mainloop()
