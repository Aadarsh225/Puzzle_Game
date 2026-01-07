import tkinter as tk
import random
import os
from PIL import Image, ImageTk

# ---------------- CONFIG ----------------
RECORD_FILE = "best_record.txt"
IMAGE_FILE = "download.jpeg"

BG_COLOR = "#0f172a"
TEXT_COLOR = "#e5e7eb"
ACCENT = "#38bdf8"
INACTIVE = "#475569"

LEVELS = {
    "Easy": 30,
    "Medium": 80,
    "Hard": 150
}

# ---------------- GAME CLASS ----------------
class EightPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Puzzle Game")
        self.root.geometry("420x600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.goal = list(range(9))
        self.board = self.goal[:]
        self.moves = 0
        self.level = "Easy"
        self.best_record = self.load_record()

        self.tiles = []
        self.buttons = []
        self.level_buttons = {}

        self.load_image_tiles()
        self.create_ui()
        self.shuffle_board()

    # ---------------- IMAGE HANDLING ----------------
    def load_image_tiles(self):
        img = Image.open(IMAGE_FILE).convert("RGB")
        img = img.resize((300, 300), Image.LANCZOS)

        self.tiles = []
        tile_size = 100

        for r in range(3):
            for c in range(3):
                box = (
                    c * tile_size,
                    r * tile_size,
                    (c + 1) * tile_size,
                    (r + 1) * tile_size
                )
                tile = img.crop(box)
                self.tiles.append(ImageTk.PhotoImage(tile))

        self.tiles[0] = None  # blank tile

    # ---------------- UI ----------------
    def create_ui(self):
        tk.Label(
            self.root,
            text="🧩 Image Puzzle Game",
            font=("Segoe UI", 22, "bold"),
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=10)

        self.stats = tk.Label(
            self.root,
            text=f"Moves: 0    Best: {self.best_record if self.best_record else '-'}",
            font=("Segoe UI", 12),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        )
        self.stats.pack()

        level_frame = tk.Frame(self.root, bg=BG_COLOR)
        level_frame.pack(pady=10)

        for lvl in LEVELS:
            btn = tk.Button(
                level_frame,
                text=lvl,
                width=8,
                font=("Segoe UI", 10, "bold"),
                bg=ACCENT if lvl == self.level else INACTIVE,
                fg="#020617",
                relief="flat",
                command=lambda l=lvl: self.set_level(l)
            )
            btn.pack(side="left", padx=5)
            self.level_buttons[lvl] = btn

        self.board_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.board_frame.pack(pady=20)

        # 🔥 FIXED IMAGE BUTTONS (NO WIDTH / HEIGHT)
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                relief="flat",
                bg=BG_COLOR,
                bd=0,
                highlightthickness=0,
                command=lambda i=i: self.move_tile(i)
            )
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

    # ---------------- GAME LOGIC ----------------
    def set_level(self, level):
        self.level = level
        for l, b in self.level_buttons.items():
            b.config(bg=ACCENT if l == level else INACTIVE)
        self.shuffle_board()

    def update_ui(self):
        for i, val in enumerate(self.board):
            if val == 0:
                self.buttons[i].config(image="", state="disabled")
            else:
                self.buttons[i].config(image=self.tiles[val], state="normal")

        self.stats.config(
            text=f"Moves: {self.moves}    Best: {self.best_record if self.best_record else '-'}"
        )

    def move_tile(self, index):
        zero = self.board.index(0)
        if abs(index//3 - zero//3) + abs(index%3 - zero%3) == 1:
            self.board[zero], self.board[index] = self.board[index], self.board[zero]
            self.moves += 1
            self.update_ui()

            if self.board == self.goal:
                self.game_won()

    def shuffle_board(self):
        self.board = self.goal[:]
        for _ in range(LEVELS[self.level]):
            zero = self.board.index(0)
            neighbors = [
                i for i in range(9)
                if abs(i//3 - zero//3) + abs(i%3 - zero%3) == 1
            ]
            move = random.choice(neighbors)
            self.board[zero], self.board[move] = self.board[move], self.board[zero]

        self.moves = 0
        self.update_ui()

    # ---------------- RECORD ----------------
    def game_won(self):
        if self.best_record is None or self.moves < self.best_record:
            self.best_record = self.moves
            self.save_record()

        win = tk.Toplevel(self.root)
        win.configure(bg=BG_COLOR)
        win.geometry("300x180")
        win.title("You Win!")

        tk.Label(
            win,
            text="🎉 Image Completed!",
            font=("Segoe UI", 16, "bold"),
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=15)

        tk.Label(
            win,
            text=f"Level: {self.level}\nMoves: {self.moves}",
            font=("Segoe UI", 12),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        ).pack()

        tk.Button(
            win,
            text="OK",
            bg=ACCENT,
            fg="#020617",
            relief="flat",
            command=win.destroy
        ).pack(pady=15)

    def load_record(self):
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, "r") as f:
                return int(f.read())
        return None

    def save_record(self):
        with open(RECORD_FILE, "w") as f:
            f.write(str(self.best_record))


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    EightPuzzle(root)
    root.mainloop()
import tkinter as tk
import random
import os
from PIL import Image, ImageTk

# ---------------- CONFIG ----------------
RECORD_FILE = "best_record.txt"
IMAGE_FILE = "puzzle_image.jpg"

BG_COLOR = "#0f172a"
TEXT_COLOR = "#e5e7eb"
ACCENT = "#38bdf8"
INACTIVE = "#475569"

LEVELS = {
    "Easy": 30,
    "Medium": 80,
    "Hard": 150
}

# ---------------- GAME CLASS ----------------
class EightPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Puzzle Game")
        self.root.geometry("420x600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.goal = list(range(9))
        self.board = self.goal[:]
        self.moves = 0
        self.level = "Easy"
        self.best_record = self.load_record()

        self.tiles = []
        self.buttons = []
        self.level_buttons = {}

        self.load_image_tiles()
        self.create_ui()
        self.shuffle_board()

    # ---------------- IMAGE HANDLING ----------------
    def load_image_tiles(self):
        img = Image.open(IMAGE_FILE).convert("RGB")
        img = img.resize((300, 300), Image.LANCZOS)

        self.tiles = []
        tile_size = 100

        for r in range(3):
            for c in range(3):
                box = (
                    c * tile_size,
                    r * tile_size,
                    (c + 1) * tile_size,
                    (r + 1) * tile_size
                )
                tile = img.crop(box)
                self.tiles.append(ImageTk.PhotoImage(tile))

        self.tiles[0] = None  # blank tile

    # ---------------- UI ----------------
    def create_ui(self):
        tk.Label(
            self.root,
            text="🧩 Image Puzzle Game",
            font=("Segoe UI", 22, "bold"),
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=10)

        self.stats = tk.Label(
            self.root,
            text=f"Moves: 0    Best: {self.best_record if self.best_record else '-'}",
            font=("Segoe UI", 12),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        )
        self.stats.pack()

        level_frame = tk.Frame(self.root, bg=BG_COLOR)
        level_frame.pack(pady=10)

        for lvl in LEVELS:
            btn = tk.Button(
                level_frame,
                text=lvl,
                width=8,
                font=("Segoe UI", 10, "bold"),
                bg=ACCENT if lvl == self.level else INACTIVE,
                fg="#020617",
                relief="flat",
                command=lambda l=lvl: self.set_level(l)
            )
            btn.pack(side="left", padx=5)
            self.level_buttons[lvl] = btn

        self.board_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.board_frame.pack(pady=20)

        # 🔥 FIXED IMAGE BUTTONS (NO WIDTH / HEIGHT)
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                relief="flat",
                bg=BG_COLOR,
                bd=0,
                highlightthickness=0,
                command=lambda i=i: self.move_tile(i)
            )
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

    # ---------------- GAME LOGIC ----------------
    def set_level(self, level):
        self.level = level
        for l, b in self.level_buttons.items():
            b.config(bg=ACCENT if l == level else INACTIVE)
        self.shuffle_board()

    def update_ui(self):
        for i, val in enumerate(self.board):
            if val == 0:
                self.buttons[i].config(image="", state="disabled")
            else:
                self.buttons[i].config(image=self.tiles[val], state="normal")

        self.stats.config(
            text=f"Moves: {self.moves}    Best: {self.best_record if self.best_record else '-'}"
        )

    def move_tile(self, index):
        zero = self.board.index(0)
        if abs(index//3 - zero//3) + abs(index%3 - zero%3) == 1:
            self.board[zero], self.board[index] = self.board[index], self.board[zero]
            self.moves += 1
            self.update_ui()

            if self.board == self.goal:
                self.game_won()

    def shuffle_board(self):
        self.board = self.goal[:]
        for _ in range(LEVELS[self.level]):
            zero = self.board.index(0)
            neighbors = [
                i for i in range(9)
                if abs(i//3 - zero//3) + abs(i%3 - zero%3) == 1
            ]
            move = random.choice(neighbors)
            self.board[zero], self.board[move] = self.board[move], self.board[zero]

        self.moves = 0
        self.update_ui()

    # ---------------- RECORD ----------------
    def game_won(self):
        if self.best_record is None or self.moves < self.best_record:
            self.best_record = self.moves
            self.save_record()

        win = tk.Toplevel(self.root)
        win.configure(bg=BG_COLOR)
        win.geometry("300x180")
        win.title("You Win!")

        tk.Label(
            win,
            text="🎉 Image Completed!",
            font=("Segoe UI", 16, "bold"),
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=15)

        tk.Label(
            win,
            text=f"Level: {self.level}\nMoves: {self.moves}",
            font=("Segoe UI", 12),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        ).pack()

        tk.Button(
            win,
            text="OK",
            bg=ACCENT,
            fg="#020617",
            relief="flat",
            command=win.destroy
        ).pack(pady=15)

    def load_record(self):
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, "r") as f:
                return int(f.read())
        return None

    def save_record(self):
        with open(RECORD_FILE, "w") as f:
            f.write(str(self.best_record))


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    EightPuzzle(root)
    root.mainloop()
import tkinter as tk
import random
import os
from PIL import Image, ImageTk

# ---------------- CONFIG ----------------
RECORD_FILE = "best_record.txt"
IMAGE_FILE = "puzzle_image.jpg"

BG_COLOR = "#0f172a"
TEXT_COLOR = "#e5e7eb"
ACCENT = "#38bdf8"
INACTIVE = "#475569"

LEVELS = {
    "Easy": 30,
    "Medium": 80,
    "Hard": 150
}

# ---------------- GAME CLASS ----------------
class EightPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Puzzle Game")
        self.root.geometry("420x600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.goal = list(range(9))
        self.board = self.goal[:]
        self.moves = 0
        self.level = "Easy"
        self.best_record = self.load_record()

        self.tiles = []
        self.buttons = []
        self.level_buttons = {}

        self.load_image_tiles()
        self.create_ui()
        self.shuffle_board()

    # ---------------- IMAGE HANDLING ----------------
    def load_image_tiles(self):
        img = Image.open(IMAGE_FILE).convert("RGB")
        img = img.resize((300, 300), Image.LANCZOS)

        self.tiles = []
        tile_size = 100

        for r in range(3):
            for c in range(3):
                box = (
                    c * tile_size,
                    r * tile_size,
                    (c + 1) * tile_size,
                    (r + 1) * tile_size
                )
                tile = img.crop(box)
                self.tiles.append(ImageTk.PhotoImage(tile))

        self.tiles[0] = None  # blank tile

    # ---------------- UI ----------------
    def create_ui(self):
        tk.Label(
            self.root,
            text="🧩 Image Puzzle Game",
            font=("Segoe UI", 22, "bold"),
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=10)

        self.stats = tk.Label(
            self.root,
            text=f"Moves: 0    Best: {self.best_record if self.best_record else '-'}",
            font=("Segoe UI", 12),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        )
        self.stats.pack()

        level_frame = tk.Frame(self.root, bg=BG_COLOR)
        level_frame.pack(pady=10)

        for lvl in LEVELS:
            btn = tk.Button(
                level_frame,
                text=lvl,
                width=8,
                font=("Segoe UI", 10, "bold"),
                bg=ACCENT if lvl == self.level else INACTIVE,
                fg="#020617",
                relief="flat",
                command=lambda l=lvl: self.set_level(l)
            )
            btn.pack(side="left", padx=5)
            self.level_buttons[lvl] = btn

        self.board_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.board_frame.pack(pady=20)

        # 🔥 FIXED IMAGE BUTTONS (NO WIDTH / HEIGHT)
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                relief="flat",
                bg=BG_COLOR,
                bd=0,
                highlightthickness=0,
                command=lambda i=i: self.move_tile(i)
            )
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

    # ---------------- GAME LOGIC ----------------
    def set_level(self, level):
        self.level = level
        for l, b in self.level_buttons.items():
            b.config(bg=ACCENT if l == level else INACTIVE)
        self.shuffle_board()

    def update_ui(self):
        for i, val in enumerate(self.board):
            if val == 0:
                self.buttons[i].config(image="", state="disabled")
            else:
                self.buttons[i].config(image=self.tiles[val], state="normal")

        self.stats.config(
            text=f"Moves: {self.moves}    Best: {self.best_record if self.best_record else '-'}"
        )

    def move_tile(self, index):
        zero = self.board.index(0)
        if abs(index//3 - zero//3) + abs(index%3 - zero%3) == 1:
            self.board[zero], self.board[index] = self.board[index], self.board[zero]
            self.moves += 1
            self.update_ui()

            if self.board == self.goal:
                self.game_won()

    def shuffle_board(self):
        self.board = self.goal[:]
        for _ in range(LEVELS[self.level]):
            zero = self.board.index(0)
            neighbors = [
                i for i in range(9)
                if abs(i//3 - zero//3) + abs(i%3 - zero%3) == 1
            ]
            move = random.choice(neighbors)
            self.board[zero], self.board[move] = self.board[move], self.board[zero]

        self.moves = 0
        self.update_ui()

    # ---------------- RECORD ----------------
    def game_won(self):
        if self.best_record is None or self.moves < self.best_record:
            self.best_record = self.moves
            self.save_record()

        win = tk.Toplevel(self.root)
        win.configure(bg=BG_COLOR)
        win.geometry("300x180")
        win.title("You Win!")

        tk.Label(
            win,
            text="🎉 Image Completed!",
            font=("Segoe UI", 16, "bold"),
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=15)

        tk.Label(
            win,
            text=f"Level: {self.level}\nMoves: {self.moves}",
            font=("Segoe UI", 12),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        ).pack()

        tk.Button(
            win,
            text="OK",
            bg=ACCENT,
            fg="#020617",
            relief="flat",
            command=win.destroy
        ).pack(pady=15)

    def load_record(self):
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, "r") as f:
                return int(f.read())
        return None

    def save_record(self):
        with open(RECORD_FILE, "w") as f:
            f.write(str(self.best_record))


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    EightPuzzle(root)
    root.mainloop()