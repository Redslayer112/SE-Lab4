from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        # All positions are 0-based (row, col).

        # Player fleet: sizes 3, 2, 2.
        self.player.place_ship({(0, 0), (0, 1), (0, 2)})
        self.player.place_ship({(2, 0), (2, 1)})
        self.player.place_ship({(4, 3), (4, 4)})

        # Enemy fleet: sizes 3, 2, 2.
        self.enemy.place_ship({(1, 1), (1, 2), (1, 3)})
        self.enemy.place_ship({(3, 0), (3, 1)})
        self.enemy.place_ship({(5, 3), (5, 4)})

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Enemy ship cells remaining:", self.enemy.remaining_cells())

    def _report_shot(self, result, shooter):
        status, sunk_size = result

        if status == "miss":
            print(f"{shooter}: MISS!")
        elif status == "hit":
            print(f"{shooter}: HIT!")
        elif status == "sunk":
            print(f"{shooter} sank a ship of size {sunk_size}.")
        elif status == "repeat":
            print("Already fired there.")

    def run(self):
        print("Battleship")

        while True:
            self.show()
            raw = input("> ").strip().lower()

            if raw == "q":
                return

            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col.")
                continue

            if not (
                0 <= pos[0] < Board.SIZE
                and 0 <= pos[1] < Board.SIZE
            ):
                print("Outside board.")
                continue

            if pos in self.enemy.shots:
                print("Already fired there.")
                continue

            # Player's shot: resolve and report exactly once.
            result = self.enemy.fire(pos)
            self._report_shot(result, "You")

            if self.enemy.all_sunk():
                print("You sank the entire enemy fleet. You win!")
                return

            # AI chooses a coordinate without printing anything.
            ai_pos = self.ai.choose()

            if ai_pos is None:
                print("AI has no remaining shots.")
                continue

            print(f"AI fired at {ai_pos[0] + 1},{ai_pos[1] + 1}")

            # Resolve the actual shot before informing the AI.
            result = self.player.fire(ai_pos)
            self.ai.observe(ai_pos, result)

            # Only game.py reports the result.
            self._report_shot(result, "AI")

            if self.player.all_sunk():
                print("Your entire fleet has been sunk. AI wins!")
                return
