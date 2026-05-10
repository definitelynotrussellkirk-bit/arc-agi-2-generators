"""Generator for arc_puzzle_bank_third_21_bundle:easy_15_exact_descending_diagonal_pairs.

Rule: red down-right diagonal runs of exact length 2 are recolored cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, only_distractor, anti_diag_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "20eea223d645"
VERSION = "1.1.0"
TASK_ID = "20eea223d645"

SUMMARY = "Red down-right diagonal runs of exact length two are recolored to cyan."

INVARIANTS = [
    "background is 0",
    "target clues are isolated down-right red pairs",
    "distractor red runs have length one or three",
    "all red runs are separated so exact-run detection is unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "only_distractor", "anti_diag_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..22"},
    "pairs":          {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "scattered_diagonal_runs",
                       "valid": "scattered_diagonal_runs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _can_place(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        if not (0 <= r < h and 0 <= c < w) or g[r][c] != 0:
            return False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        target = min(ctx.draw_int("pairs", 1, 2), max(1, min(h, w) // 2))
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 16)
        w = ctx.draw_int("grid_w", 12, 20)
        target = min(ctx.draw_int("pairs", 4, 7), max(1, min(h, w) // 2))
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        target = min(ctx.draw_int("pairs", 2, 3), max(1, min(h, w) // 2))
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    placed = 0
    for _ in range(120):
        if placed >= target:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        cells = [(r, c), (r + 1, c + 1)]
        if _can_place(g, cells):
            for rr, cc in cells:
                g[rr][cc] = 2
            placed += 1

    for length in (1, 3):
        for _ in range(80):
            r = rng.randint(0, h - length)
            c = rng.randint(0, w - length)
            cells = [(r + i, c + i) for i in range(length)]
            if _can_place(g, cells):
                for rr, cc in cells:
                    g[rr][cc] = 2
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no length-2 down-right pairs.
        return g
    if name == "only_distractor":
        # Only length-1 and length-3 down-right runs (no length-2)
        # — rule's exact-length filter excludes; output equals input.
        g[2][2] = 2
        for i in range(3): g[5 + i][5 + i] = 2
        return g
    if name == "anti_diag_pair":
        # Anti-diagonal (down-left) red pair — rule's "down-right"
        # direction filter excludes; rule's effect invisible.
        g[2][7] = 2; g[3][6] = 2
        return g
    return g
