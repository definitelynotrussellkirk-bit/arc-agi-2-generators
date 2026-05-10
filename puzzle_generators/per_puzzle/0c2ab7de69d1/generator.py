"""Generator for arc_additional_puzzle_bank_volume8:E56.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, source_below_divider, no_room_below.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0c2ab7de69d1"
VERSION = "1.1.0"
TASK_ID = "0c2ab7de69d1"
SUMMARY = "An object above a gray divider row is reflected below in cyan."

INVARIANTS = [
    "background is 0",
    "there is one full-width gray divider row",
    "source object cells are above the divider",
    "reflected destination cells are in bounds and empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "source_below_divider", "no_room_below")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 7..13", "valid": "4..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 4..8", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "above_divider",
                       "valid": "above_divider"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 7, 9)
        n_cells = ctx.draw_int("n_cells", 3, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 18)
        w = ctx.draw_int("grid_w", 11, 16)
        n_cells = ctx.draw_int("n_cells", 6, 10)
    else:
        h = ctx.draw_int("grid_h", 9, 14)
        w = ctx.draw_int("grid_w", 7, 13)
        n_cells = ctx.draw_int("n_cells", 4, 8)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    divider = rng.randint(3, h - 4)
    for c in range(w):
        g[divider][c] = 5
    min_r = max(0, 2 * divider - (h - 1))
    rows = list(range(min_r, divider))
    cells: set[tuple[int, int]] = set()
    start = (rng.choice(rows), rng.randint(1, w - 2))
    cells.add(start)
    frontier = [start]
    while len(cells) < n_cells and frontier:
        r, c = rng.choice(frontier)
        options = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            rr = 2 * divider - nr
            if min_r <= nr < divider and 0 <= nc < w and rr < h:
                options.append((nr, nc))
        rng.shuffle(options)
        made_progress = False
        for pos in options:
            if pos not in cells:
                cells.add(pos)
                frontier.append(pos)
                made_progress = True
                break
        if not made_progress:
            frontier.remove((r, c))
    colors = [2, 3, 4, 6, 7, 8, 9]
    for i, (r, c) in enumerate(sorted(cells)):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # No gray divider — rule has no reflection axis.
        g[2][3] = 4; g[3][3] = 4
        return g
    if name == "source_below_divider":
        # Source cells are below the divider — rule has no above-source.
        for c in range(w): g[5][c] = 5
        g[7][3] = 4; g[8][3] = 4
        return g
    if name == "no_room_below":
        # Divider near bottom; reflections fall out of grid bounds.
        for c in range(w): g[h - 2][c] = 5
        g[1][3] = 4; g[2][3] = 4; g[3][3] = 4
        return g
    return g
