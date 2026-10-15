class Board:
    SIZE = 6

    def __init__(self):
        self.ships = []
        self.shots = set()

    def place_ship(self, cells):
        cells = set(cells)

        if not cells:
            raise ValueError("A ship must contain at least one cell.")

        for r, c in cells:
            if not (0 <= r < self.SIZE and 0 <= c < self.SIZE):
                raise ValueError("Ship cell is outside the board.")

        for ship in self.ships:
            if cells & ship["cells"]:
                raise ValueError("Ships cannot overlap.")

        self.ships.append({
            "cells": cells,
            "hits": set()
        })

    def fire(self, pos):
        # Return (status, sunk_size).
        # status: "miss", "hit", "sunk", or "repeat".

        if pos in self.shots:
            return ("repeat", None)

        self.shots.add(pos)

        for ship in self.ships:
            if pos in ship["cells"]:
                ship["hits"].add(pos)

                if ship["hits"] == ship["cells"]:
                    return ("sunk", len(ship["cells"]))

                return ("hit", None)

        return ("miss", None)

    def remaining_cells(self):
        return sum(
            len(ship["cells"] - ship["hits"])
            for ship in self.ships
        )

    def all_sunk(self):
        return all(
            ship["hits"] == ship["cells"]
            for ship in self.ships
        )
