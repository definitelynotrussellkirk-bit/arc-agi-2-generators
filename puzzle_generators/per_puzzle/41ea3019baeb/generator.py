"""Generator for arc_puzzle_bank_21_set10_s:S10_H1 — laser-bounce trail with mirrors.

Rule: each color-2 emitter shoots a ray; mirrors (5, 6, 7) deflect; trail
painted color 8 on bg cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_emitters,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_emitters, no_mirrors, emitter_at_mirror.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "41ea3019baeb"
VERSION = "1.1.0"
TASK_ID = "41ea3019baeb"

SUMMARY = "1-2 color-2 emitters + 1-3 mirrors (5, 6, or 7)."

INVARIANTS = [
    "background is 0",
    "1-2 color-2 emitter cells",
    "1-3 mirror cells in colors {5, 6, 7}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_emitters", "no_mirrors", "emitter_at_mirror")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_emitters":     {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "n_mirrors":      {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "emitters_plus_mirrors",
                       "valid": "emitters_plus_mirrors"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 9)
        n_emitters = ctx.draw_int("n_emitters", 1, 1)
        n_mirrors = ctx.draw_int("n_mirrors", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        n_emitters = ctx.draw_int("n_emitters", 2, 2)
        n_mirrors = ctx.draw_int("n_mirrors", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        n_emitters = ctx.draw_int("n_emitters", 1, 2)
        n_mirrors = ctx.draw_int("n_mirrors", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(n_emitters):
        for _t in range(60):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = 2
            break
    for _ in range(n_mirrors):
        for _t in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice([5, 6, 7])
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_emitters":
        # mirrors only, no emitters → no rays to trace
        g[2][3] = 5
        g[5][7] = 6
        return g
    if name == "no_mirrors":
        # emitters only, no mirrors → ray trail is undefined direction
        g[3][3] = 2
        g[5][7] = 2
        return g
    if name == "emitter_at_mirror":
        # emitter and mirror at same logical cell impossible → place adjacent which makes ray immediately deflected with no straight segment
        g[3][3] = 2
        g[3][4] = 5  # mirror immediately to the right of emitter
        return g
    return g
