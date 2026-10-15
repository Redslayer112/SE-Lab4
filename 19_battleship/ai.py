import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.hits = set()

    def choose(self):
        # Never choose a coordinate that was already tried.
        options = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if (r, c) not in self.tried
        ]

        if not options:
            return None

        # Prefer untried cells adjacent to previous hits.
        targets = set()

        for r, c in self.hits:
            for nr, nc in (
                (r - 1, c),
                (r + 1, c),
                (r, c - 1),
                (r, c + 1),
            ):
                if (
                    0 <= nr < self.size
                    and 0 <= nc < self.size
                    and (nr, nc) not in self.tried
                ):
                    targets.add((nr, nc))

        candidates = list(targets) if targets else options
        pos = random.choice(candidates)

        # Reserve the coordinate immediately to prevent repeats.
        self.tried.add(pos)
        return pos

    def observe(self, pos, result):
        # Called only after the actual shot has been resolved.
        status, _ = result

        if status == "hit":
            self.hits.add(pos)
        elif status == "sunk":
            # The current hit completed a ship.
            self.hits.discard(pos)
