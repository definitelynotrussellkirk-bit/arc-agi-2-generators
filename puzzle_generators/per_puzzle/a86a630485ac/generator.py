"""Generator for arc_puzzle_bank_next21:M12 — keep vertically-symmetric objects.

Rule: only objects that are vertically symmetric (mirror-LR through their
own bbox center column) are kept; others are erased.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_symmetric (every motif is LR-symmetric → rule keeps
everything, no erasure contrast), all_asymmetric (no motif is
LR-symmetric → rule erases everything, output is empty), single_motif
(only one motif → trivial selection, no candidate contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a86a630485ac"
VERSION = "1.1.0"
TASK_ID = "a86a630485ac"

SUMMARY = "Mix of LR-symmetric motifs and asymmetric motifs in distinct colors."

INVARIANTS = [
    "background is 0",
    "1-2 LR-symmetric motifs (e.g., plus, T, vertical bar) in distinct colors",
    "1-2 asymmetric motifs (e.g., L, J) in distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_symmetric", "all_asymmetric", "single_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":            {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "sym_plus_asym_motifs",
                          "valid": "sym_plus_asym_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "3..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


SYM_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 1)],          # T
    [(0, 1), (1, 0), (1, 1), (1, 2)],          # T inverted
    [(0, 0), (1, 0), (2, 0)],                  # vertical line
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],  # plus
]
ASYM_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],                  # L
    [(0, 0), (0, 1), (1, 1)],                  # corner
    [(0, 0), (0, 1), (0, 2), (1, 0)],          # J
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 8, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
        n_sym = 2; n_asym = 2
        all_shapes = (
            [(rng.choice(SYM_SHAPES), colors[i]) for i in range(n_sym)] +
            [(rng.choice(ASYM_SHAPES), colors[n_sym + i]) for i in range(n_asym)]
        )
        ok = True
        for shape, color in all_shapes:
            rs = [r for r, _ in shape]; cs = [c for _, c in shape]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in shape:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize M12 layout")


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "all_symmetric":
        # Every motif is LR-symmetric — rule keeps everything;
        # no erasure contrast.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1)]:
            g[1 + dr][1 + dc] = 2
        for dr, dc in [(0, 0), (1, 0), (2, 0)]:
            g[1 + dr][6 + dc] = 4
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
            g[4 + dr][3 + dc] = 6
        return g
    if name == "all_asymmetric":
        # No motif is LR-symmetric — rule erases everything;
        # output is empty.
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[2 + dr][5 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 0)]:
            g[5 + dr][3 + dc] = 6
        return g
    if name == "single_motif":
        # Only one motif — trivial selection, no candidate contrast.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1)]:
            g[3 + dr][3 + dc] = 4
        return g
    return g
