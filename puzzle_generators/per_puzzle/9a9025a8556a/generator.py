"""Generator for 558ea9b3.

Rule: magenta(6) components are recolored by bbox aspect: tall (h>w)→2,
wide (w>h)→8, square stays magenta.

Combinatorial axes (8): grid_h/w, n_tall, n_wide, n_square,
component_size_range, position_bias, decoy_density, decoy_palette_size.
Degenerates: all_square, all_tall, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9a9025a8556a"
VERSION = "1.1.0"
TASK_ID = "9a9025a8556a"
SUMMARY = "Magenta components by bbox aspect: tall→2, wide→8, square unchanged."

INVARIANTS = [
    "all components are magenta(6), 4-connected",
    "components separated by >=1 bg cell",
    ">=1 tall AND >=1 wide component (so rule branches both ways)",
    ">=1 square component (so rule's no-op branch fires)",
]

# Pattern templates for variety
TALL_PATTERNS = (
    [[1, 0], [1, 1], [1, 0], [1, 0]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 0], [1, 1], [1, 0]],
)
WIDE_PATTERNS = (
    [[1, 1, 1, 1], [0, 1, 0, 1]],
    [[1, 1, 1, 1, 1]],
    [[1, 0, 1, 1, 1], [1, 1, 1, 0, 1]],
)
SQUARE_PATTERNS = (
    [[1, 1], [1, 1]],
    [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
)
DEGENERATE_TEXTURES = ("all_square", "all_tall", "single_object")
HELPFUL_TEXTURES = ("balanced", "tall_heavy", "wide_heavy", "many_components")

AXES = {
    "grid_h":             {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":             {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "n_tall":             {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "n_wide":             {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "n_square":           {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "position_bias":      {"type": "str", "default": "rng spread|center|edge",
                           "valid": "spread|center|edge"},
    "decoy_palette_size": {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "decoy_density":      {"type": "float", "default": "rng 0..0.05",
                           "valid": "0..0.15"},
    "texture":            {"type": "str", "default": "rng helpful",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _can_place(grid, pattern, top, left):
    h, w = len(grid), len(grid[0])
    ph, pw = len(pattern), len(pattern[0])
    if top < 1 or left < 1 or top + ph >= h or left + pw >= w:
        return False
    for r in range(top - 1, top + ph + 1):
        for c in range(left - 1, left + pw + 1):
            if grid[r][c] != 0:
                return False
    return True


def _stamp(grid, pattern, top, left, color=6):
    for rr, row in enumerate(pattern):
        for cc, bit in enumerate(row):
            if bit:
                grid[top + rr][left + cc] = color


def _place(grid, pattern, bias, rng):
    h, w = len(grid), len(grid[0])
    ph, pw = len(pattern), len(pattern[0])
    spots = [(r, c) for r in range(1, h - ph)
             for c in range(1, w - pw)
             if _can_place(grid, pattern, r, c)]
    if not spots:
        return False
    if bias == "center":
        cr, cc = h // 2, w // 2
        spots.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        top, left = spots[rng.randint(0, min(2, len(spots) - 1))]
    elif bias == "edge":
        spots.sort(key=lambda rc: min(rc[0], h - 1 - rc[0], rc[1], w - 1 - rc[1]))
        top, left = spots[rng.randint(0, min(2, len(spots) - 1))]
    else:
        top, left = rng.choice(spots)
    _stamp(grid, pattern, top, left)
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    if texture == "tall_heavy":
        n_tall, n_wide, n_square = 3, 1, 1
    elif texture == "wide_heavy":
        n_tall, n_wide, n_square = 1, 3, 1
    elif texture == "many_components":
        n_tall, n_wide, n_square = 2, 2, 2
    else:  # balanced
        n_tall = int(overrides.get("n_tall", ctx.draw_int("n_tall", 1, 2)))
        n_wide = int(overrides.get("n_wide", ctx.draw_int("n_wide", 1, 2)))
        n_square = int(overrides.get("n_square", ctx.draw_int("n_square", 1, 2)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 2)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.05)))
    g = full_grid(h, w, 0)
    plan = []
    for _ in range(n_tall):
        plan.append(rng.choice(TALL_PATTERNS))
    for _ in range(n_wide):
        plan.append(rng.choice(WIDE_PATTERNS))
    for _ in range(n_square):
        plan.append(rng.choice(SQUARE_PATTERNS))
    rng.shuffle(plan)
    for pattern in plan:
        _place(g, pattern, bias, rng)
    decoy_pool = [c for c in range(1, 10) if c not in (0, 2, 6, 8)]
    rng.shuffle(decoy_pool)
    decoy_palette = decoy_pool[:max(0, n_decoy)]
    if decoy_palette and decoy_d > 0:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0 and rng.random() < decoy_d:
                    if not any(g[nr][nc] == 6
                               for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                               if 0 <= nr < h and 0 <= nc < w):
                        g[r][c] = rng.choice(decoy_palette)
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "all_square":
        _place(g, SQUARE_PATTERNS[0], "spread", rng)
        _place(g, SQUARE_PATTERNS[1], "spread", rng)
        return g
    if name == "all_tall":
        for _ in range(3):
            _place(g, TALL_PATTERNS[0], "spread", rng)
        return g
    if name == "single_object":
        _place(g, SQUARE_PATTERNS[0], "center", rng)
        return g
    return g
