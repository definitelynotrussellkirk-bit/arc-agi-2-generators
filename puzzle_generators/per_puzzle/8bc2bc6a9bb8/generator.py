"""Generator for arc_puzzle_bank_tenth21:H70.

The top row is a left-to-right palette.  The body contains separated
placeholder-color shapes; the rule sorts those shapes by size, recolors them
with the palette, and packs them into the output.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8bc2bc6a9bb8"
VERSION = "1.1.0"
TASK_ID = "8bc2bc6a9bb8"

SUMMARY = "Palette row recolors size-sorted placeholder shapes into a packed inventory."

INVARIANTS = [
    "background is 0",
    "top row contains a nonzero palette read left-to-right",
    "body contains 2-4 separated placeholder-color 8 components",
    "placeholder components have distinct sizes to make the size order stable",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w": {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "n": {"type": "int", "default": "rng 3..4", "valid": "2..4"},
}

SHAPE_BANK = {
    5: [
        ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0)),
        ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)),
    ],
    4: [
        ((0, 0), (0, 1), (1, 0), (1, 1)),
        ((0, 0), (1, 0), (2, 0), (2, 1)),
        ((0, 0), (0, 1), (0, 2), (1, 1)),
    ],
    3: [
        ((0, 0), (1, 0), (1, 1)),
        ((0, 0), (0, 1), (0, 2)),
        ((0, 0), (1, 0), (2, 0)),
    ],
    2: [
        ((0, 0), (0, 1)),
        ((0, 0), (1, 0)),
    ],
}


def _normalized(cells):
    materialized = tuple(cells)
    r0 = min(r for r, _ in materialized)
    c0 = min(c for _, c in materialized)
    return tuple(sorted((r - r0, c - c0) for r, c in materialized))


def _turn_once(cells):
    return _normalized((c, -r) for r, c in cells)


def _maybe_orient(cells, turns):
    out = tuple(cells)
    for _ in range(turns % 4):
        out = _turn_once(out)
    return out


def _bbox(cells):
    return max(r for r, _ in cells) + 1, max(c for _, c in cells) + 1


def _can_place(grid, cells, r0, c0):
    h = len(grid)
    w = len(grid[0])
    for dr, dc in cells:
        r = r0 + dr
        c = c0 + dc
        if r < 1 or c < 0 or r >= h or c >= w:
            return False
    rs = [r0 + dr for dr, _ in cells]
    cs = [c0 + dc for _, dc in cells]
    for r in range(max(1, min(rs) - 1), min(h, max(rs) + 2)):
        for c in range(max(0, min(cs) - 1), min(w, max(cs) + 2)):
            if grid[r][c] != 0:
                return False
    return True


def _paint(grid, cells, r0, c0, color):
    for dr, dc in cells:
        grid[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    h = ctx.draw_int("grid_h", 8, 10)
    w = ctx.draw_int("grid_w", 12, 14)
    n = ctx.draw_int("n", 3, 4)
    rng = ctx.draw_rng("layout")

    grid = full_grid(h, w, 0)

    palette = list(ctx.draw_distinct_colors("palette", n=n, exclude={0, 8}))
    palette_cols = sorted(rng.sample(range(w), n))
    for col, color in zip(palette_cols, palette):
        grid[0][col] = color

    sizes = [5, 4, 3, 2][:n]
    pieces = []
    for size in sizes:
        base = rng.choice(SHAPE_BANK[size])
        pieces.append(_maybe_orient(base, rng.randint(0, 3)))

    for piece in pieces:
        ph, pw = _bbox(piece)
        placed = False
        for _ in range(200):
            r0 = rng.randint(1, h - ph)
            c0 = rng.randint(0, w - pw)
            if _can_place(grid, piece, r0, c0):
                _paint(grid, piece, r0, c0, 8)
                placed = True
                break
        if not placed:
            raise ValueError("could not place separated placeholder shapes")

    return grid
