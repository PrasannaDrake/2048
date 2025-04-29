import tkinter as tk
import random

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.window.configure(bg="#FFDDA0")  # Caramel color

        self.grid = [[0] * 4 for _ in range(4)]
        self.cells = [[None] * 4 for _ in range(4)]

        self.score = 0

        self.main_frame = tk.Frame(self.window, bg="#FFDDA0")
        self.main_frame.pack(padx=10, pady=10)

        self.create_gui()
        self.new_game()

        self.window.bind("<Key>", self.key_handler)
        self.window.bind("r", lambda event: self.new_game())
        self.window.mainloop()

    def create_gui(self):
        grid_frame = tk.Frame(self.main_frame, bg="#FFDDA0")
        grid_frame.grid(row=0, column=0, rowspan=2)

        for i in range(4):
            for j in range(4):
                frame = tk.Frame(grid_frame, bg="#FFEBCD", width=100, height=100)
                frame.grid(row=i, column=j, padx=5, pady=5)
                label = tk.Label(frame, text="", bg="#FFEBCD", font=("Arial", 24, "bold"), width=4, height=2)
                label.pack()
                self.cells[i][j] = label

        side_panel = tk.Frame(self.main_frame, bg="#FFDDA0")
        side_panel.grid(row=0, column=1, padx=10, sticky="ne")

        score_frame = tk.Frame(side_panel, bg="white", bd=2, relief="ridge")
        score_frame.pack(pady=(0, 10))
        self.score_label = tk.Label(score_frame, text="Score:\n0", bg="white", fg="#00008B", font=("Arial", 14))
        self.score_label.pack(padx=10, pady=5)

        reset_button = tk.Button(self.main_frame, text="Reset", command=self.new_game, font=("Arial", 12))
        reset_button.grid(row=1, column=1, pady=20, sticky="se")

    def update_gui(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                bg_color, fg_color = self.get_color(value)
                label = self.cells[i][j]
                label.config(text=str(value) if value != 0 else "", bg=bg_color, fg=fg_color)
        self.score_label.config(text=f"Score:\n{self.score}")

    def get_color(self, value):
        color_cycle = [
            ("#F0F8FF", "#00008B"),  # 2: aliceblue, darkblue
            ("#FFA07A", "#8B0000"),  # 4: lightorange (lightsalmon), red
            ("#8FBC8F", "#043927"),  # 8: hemlock (darkseagreen), Sacramento
            ("#87CEEB", "#8A2BE2")   # 16: skyblue, berryblue
        ]
        if value == 0:
            return ("#FFEBCD", "#00008B")  # almond for empty, darkblue
        index = (value.bit_length() - 2) % len(color_cycle)
        return color_cycle[index]

    def new_game(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        self.update_gui()

    def add_random_tile(self):
        empty = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.grid[i][j] = random.choice([2, 4,8])

    def key_handler(self, event):
        key = event.keysym
        if key == "Up":
            moved = self.move_up()
        elif key == "Down":
            moved = self.move_down()
        elif key == "Left":
            moved = self.move_left()
        elif key == "Right":
            moved = self.move_right()
        else:
            return

        if moved:
            self.add_random_tile()
            self.update_gui()
            if self.check_game_over():
                self.game_over()

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (4 - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(3):
            if row[i] != 0 and row[i] == row[i+1]:
                row[i] *= 2
                self.score += row[i]
                row[i+1] = 0
        return row

    def move_left(self):
        moved = False
        for i in range(4):
            original = self.grid[i][:]
            compressed = self.compress(self.grid[i])
            merged = self.merge(compressed)
            final = self.compress(merged)
            self.grid[i] = final
            if final != original:
                moved = True
        return moved

    def move_right(self):
        moved = False
        for i in range(4):
            original = self.grid[i][:]
            reversed_row = original[::-1]
            compressed = self.compress(reversed_row)
            merged = self.merge(compressed)
            final = self.compress(merged)
            self.grid[i] = final[::-1]
            if self.grid[i] != original:
                moved = True
        return moved

    def transpose(self):
        self.grid = [list(row) for row in zip(*self.grid)]

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def check_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
                if j < 3 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
        return True

    def game_over(self):
        popup = tk.Toplevel(self.window)
        popup.title("Game Over")
        popup.geometry("200x100")
        tk.Label(popup, text="Game Over!", font=("Arial", 14)).pack(pady=10)
        tk.Button(popup, text="New Game", command=lambda:[popup.destroy(), self.new_game()]).pack()

if __name__ == "__main__":
    Game2048()
