import random
import sys

class CityRiotGame:
    def __init__(self, width=8, height=8, n_rioters=4, n_police=3):
        self.width = width
        self.height = height
        self.n_rioters = n_rioters
        self.n_police = n_police
        self.rioters = set()
        self.police = []
        self._init_game()

    def _init_game(self):
        # Place rioters on bottom two rows
        available = [(r, c) for r in range(self.height-2, self.height) for c in range(self.width)]
        random.shuffle(available)
        for i in range(self.n_rioters):
            pos = available[i]
            self.rioters.add(pos)

        # Place police on top two rows
        available = [(r, c) for r in range(0, 2) for c in range(self.width)]
        random.shuffle(available)
        self.police = []
        used = set(self.rioters)
        i = 0
        while len(self.police) < self.n_police and i < len(available):
            pos = available[i]
            if pos not in used:
                self.police.append(pos)
                used.add(pos)
            i += 1
        if len(self.police) < self.n_police:
            # fill from middle if needed
            for r in range(0, self.height):
                for c in range(0, self.width):
                    pos = (r, c)
                    if pos not in used:
                        self.police.append(pos)
                        used.add(pos)
                        if len(self.police) == self.n_police:
                            break
                if len(self.police) == self.n_police:
                    break

    def draw(self):
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for (r, c) in self.rioters:
            grid[r][c] = 'R'
        for idx, (r, c) in enumerate(self.police):
            grid[r][c] = 'P{}'.format(idx) if idx < 10 else 'P*'
        # Print board
        print("\nCity Grid:")
        for r in range(self.height):
            row = []
            for c in range(self.width):
                cell = grid[r][c]
                row.append(cell if len(cell) == 1 else cell)  # keep 'R' or 'P' with possible index
            print(' '.join(row))
        print()

    def ai_turn(self):
        if not self.rioters:
            return False  # Police already won
        new_positions = set()
        occupied = self.rioters.union(self.police)
        # Simple movement: each rioter tries to move up if possible, else up-left/up-right, else stay
        rioters_sorted = sorted(list(self.rioters), key=lambda x: (x[0], x[1]))
        for (r, c) in rioters_sorted:
            moved = False
            targets = []
            if r > 0:
                targets.append((r-1, c))      # up
                if c-1 >= 0:
                    targets.append((r-1, c-1))  # up-left
                if c+1 < self.width:
                    targets.append((r-1, c+1))  # up-right
            # If none of targets available, try sideways
            if not targets:
                if c > 0:
                    targets.append((r, c-1))
                if c+1 < self.width:
                    targets.append((r, c+1))
            for tr, tc in targets:
                if (tr, tc) in occupied or (tr, tc) in new_positions:
                    continue
                # Do not move into a police-occupied cell
                if (tr, tc) in self.police:
                    continue
                # Move
                new_positions.add((tr, tc))
                moved = True
                break
            if not moved:
                # stay in place if cannot move
                new_positions.add((r, c))
        # Update rioters
        self.rioters = new_positions
        # Check win condition: any rioter reached top row
        for (r, _) in self.rioters:
            if r == 0:
                return True  # Rioters win
        return False

    def police_move(self, index, direction):
        if index < 0 or index >= len(self.police):
            return False
        r, c = self.police[index]
        dr, dc = 0, 0
        if direction == 'w':
            dr, dc = -1, 0
        elif direction == 's':
            dr, dc = 1, 0
        elif direction == 'a':
            dr, dc = 0, -1
        elif direction == 'd':
            dr, dc = 0, 1
        else:
            return False
        nr, nc = r + dr, c + dc
        if not (0 <= nr < self.height and 0 <= nc < self.width):
            return False
        # Check cell occupancy
        if (nr, nc) in self.rioters:
            # capture rioter
            self.rioters.discard((nr, nc))
        if (nr, nc) in self.police:
            return False
        # Move
        self.police[index] = (nr, nc)
        return True

    def play_round(self):
        # AI turn first
        rioters_won = self.ai_turn()
        if rioters_won:
            self.draw()
            print("Riots have reached the city center. Rioters win!")
            return True
        self.draw()
        # If all rioters eliminated
        if not self.rioters:
            print("All rioters are subdued. Police win!")
            return True

        # Player turn
        while True:
            try:
                print("Police units:")
                for idx, (r, c) in enumerate(self.police):
                    print("  {}: ({}, {})".format(idx, r, c))
                inp = input("Enter police index and direction (e.g., 0 w) to move, or 'q' to quit: ").strip()
                if inp.lower() == 'q':
                    print("Game exited.")
                    sys.exit(0)
                parts = inp.split()
                if len(parts) != 2:
                    print("Invalid input. Try again.")
                    continue
                pidx = int(parts[0])
                dirc = parts[1].lower()
                if dirc not in ('w','a','s','d'):
                    print("Invalid direction. Use w/a/s/d.")
                    continue
                if not self.police_move(pidx, dirc):
                    print("Move invalid or blocked. Try a different move.")
                    continue
                break
            except Exception as e:
                print("Error:", e)
                continue

        # After police move, check capture again
        if not self.rioters:
            self.draw()
            print("All rioters are subdued. Police win!")
            return True

        # End of round
        self.draw()
        return False

def main():
    random.seed()
    game = CityRiotGame(width=8, height=8, n_rioters=4, n_police=3)
    print("Welcome to City Riot — computer moves first.")
    game.draw()
    game_over = False
    while not game_over:
        game_over = game.play_round()

if __name__ == "__main__":
    main()