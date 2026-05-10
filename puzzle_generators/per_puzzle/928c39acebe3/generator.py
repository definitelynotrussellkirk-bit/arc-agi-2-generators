"""Generator for arc_puzzle_bank_21_set15_bundle:hard_o07 — laser-bounce trail.

Rule: each color-2 emitter shoots a beam to the right; color-4 reflects /,
color-5 reflects \\, color-6 stops it. Path painted color 8 in 0-cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_emitters, n_mirrors,
n_blockers, texture.
Degenerates: no_emitter, no_mirrors, blocker_at_emitter.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "928c39acebe3"
VERSION = "1.1.0"
TASK_ID = "928c39acebe3"

SUMMARY = "1-2 color-2 emitters + a few mirrors (4 or 5) + 0-2 blockers (6)."

INVARIANTS = [
    "background is 0",
    "1-2 color-2 emitter cells",
    "1-3 mirror cells (color 4 or 5)",
    "0-2 blocker cells (color 6)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_emitter", "no_mirrors", "blocker_at_emitter")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_emitters":     {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "n_mirrors":      {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "n_blockers":     {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "left_emitter_right_targets",
                       "valid": "left_emitter_right_targets"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..4"},
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
        w = ctx.draw_int("grid_w", 10, 11)
        n_emitters = ctx.draw_int("n_emitters", 1, 1)
        n_mirrors = ctx.draw_int("n_mirrors", 1, 1)
        n_blockers = ctx.draw_int("n_blockers", 0, 0)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 16)
        n_emitters = ctx.draw_int("n_emitters", 2, 3)
        n_mirrors = ctx.draw_int("n_mirrors", 3, 4)
        n_blockers = ctx.draw_int("n_blockers", 1, 2)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
        n_emitters = ctx.draw_int("n_emitters", 1, 2)
        n_mirrors = ctx.draw_int("n_mirrors", 1, 3)
        n_blockers = ctx.draw_int("n_blockers", 0, 2)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for _ in range(n_emitters):
        for _t in range(60):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 4)
            if g[r][c] != 0: continue
            g[r][c] = 2
            break
    for _ in range(n_mirrors):
        for _t in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(1, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice([4, 5])
            break
    for _ in range(n_blockers):
        for _t in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(1, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = 6
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_emitter":
        # Mirrors + blockers but no color-2 emitter — rule has no
        # beam to trace.
        g[3][5] = 4; g[6][7] = 5
        g[5][9] = 6
        return g
    if name == "no_mirrors":
        # Emitter + blocker but no mirrors — rule's reflection step
        # never fires; beam goes in a straight line until blocker
        # or edge.
        g[3][1] = 2
        g[3][8] = 6
        return g
    if name == "blocker_at_emitter":
        # Emitter and blocker share the same row at adjacent column —
        # beam stops immediately, rule's path has zero painted cells.
        g[3][1] = 2
        g[3][2] = 6
        return g
    return g
