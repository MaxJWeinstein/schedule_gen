import random

BASE_COLORS = [
    "red",
    "lime",
    "blue",
    "fuchsia",
    "coral",
    "green"
    "#FF6F00", #orange
    "#00FFEC", #cyan
    "gold",
    "EF02FF", #pink
    "7417FF", #purple
]

class ColorGen:
    def __init__(self, base_list: list[str]|None = None):
        if base_list is None:
            base_list = BASE_COLORS
        self._list: list[str] = [c for c in base_list]
        self._iter = iter(self._list)
        self._rng = random.Random()

    def next(self) -> str:
        try:
            return next(self._iter)
        except StopIteration:
            return self._random_color()

    def _random_color(self) -> str:
        r = self._rng.randrange(256)
        g = self._rng.randrange(256)
        b = self._rng.randrange(256)
        return f"rgb({r}, {g}, {b})"
