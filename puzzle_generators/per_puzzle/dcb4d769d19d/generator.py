"""Generator for arc_additional_puzzle_bank_volume10:E70.

Singleton red markers are replaced by yellow cardinal crosses.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_singletons, markers_at_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dcb4d769d19d"
VERSION = "1.1.0"
TASK_ID = "dcb4d769d19d"
SUMMARY = "Singleton red markers are replaced by yellow cardinal crosses."

INVARIANTS = [
    "background is 0",
    "target red components are singleton cells away from the border",
    "singleton markers are separated so crosses do not obscure each other",
    "larger red components are optional non-target distractors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_singletons", "markers_at_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "singleton_red_markers",
                       "valid": "singleton_red_markers"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_markers = ctx.draw_int("n_markers", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_markers = ctx.draw_int("n_markers", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_markers = ctx.draw_int("n_markers", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    cells: list[tuple[int, int]] = []
    for _ in range(180):
        if len(cells) >= n_markers:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in cells):
            continue
        g[r][c] = 2
        cells.append((r, c))
    if not cells:
        g[2][2] = 2
    # A red domino is a non-target component.
    for r in range(1, h - 1):
        for c in range(1, w - 2):
            if g[r][c] == 0 and g[r][c + 1] == 0:
                if all(abs(r - rr) >= 2 or abs(c - cc) >= 3 for rr, cc in cells):
                    g[r][c] = 2
                    g[r][c + 1] = 2
                    return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blank → no singletons to expand into crosses
        return g
    if name == "no_singletons":
        # only larger red components (dominoes/triples) → no singleton targets
        g[2][2] = 2; g[2][3] = 2
        g[5][6] = 2; g[5][7] = 2; g[6][6] = 2
        return g
    if name == "markers_at_border":
        # singletons on the border → cross arms would extend OOB
        g[0][3] = 2
        g[h - 1][6] = 2
        g[4][0] = 2
        return g
    return g
