"""Generator for arc_puzzle_bank_21_set5_s:S5_E4.

Rule: each yellow emitter shoots a cyan ray rightward until it hits a
maroon blocker or the right edge.

Combinatorial axes (8): grid_h/w, palette_kind, n_emitters,
palette_size, position_bias, n_distinct_colors, blocker_density, texture.
Degenerates: no_emitters, blocker_at_emitter, all_blockers_left.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "302ddfbe2baa"
VERSION = "1.1.0"
TASK_ID = "302ddfbe2baa"
SUMMARY = "Yellow emitters paint cyan rays rightward until a maroon blocker or edge."

INVARIANTS = [
    "background is 0",
    "each active row has one yellow emitter",
    "some active rows have a maroon blocker to the right",
    "ray cells between the emitter and blocker or edge are initially empty",
]

PALETTE_KINDS = ("default", "sparse", "dense", "all_blocked")
DEGENERATE_TEXTURES = ("no_emitters", "blocker_at_emitter", "all_blockers_left")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "6..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "emitter_count":  {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "blocker_density": {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
    count = ctx.draw_int("emitter_count", 2, min(4, h))
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in rng.sample(range(h), count):
        c = rng.randint(0, w - 3)
        g[r][c] = 4
        if rng.random() < 0.7:
            g[r][rng.randint(c + 2, w - 1)] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_emitters":
        # blockers but no yellow emitters — no rays generated
        g[2][7] = 9
        g[4][8] = 9
        return g
    if name == "blocker_at_emitter":
        # yellow + maroon adjacent — ray length zero
        g[2][3] = 4
        g[2][4] = 9
        return g
    if name == "all_blockers_left":
        # blockers placed LEFT of emitter — ray fires right unhindered
        g[3][8] = 9  # blocker
        g[3][2] = 4  # emitter to right of blocker
        return g
    return g
