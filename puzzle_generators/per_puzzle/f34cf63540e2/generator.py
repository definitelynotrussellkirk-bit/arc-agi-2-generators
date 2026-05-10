"""Generator for arc_additional_puzzles_21_set18_bundle:H124 — sequential transforms from row-0 commands.

Rule: top-row commands (codes 2..6 mapped to cw/180/transpose/flip-lr/flip-ud)
are applied sequentially to the lower motif's bbox crop. Output the final crop.

Combinatorial axes (8): n_cmds, grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_commands, no_motif, identity_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f34cf63540e2"
VERSION = "1.1.0"
TASK_ID = "f34cf63540e2"

SUMMARY = "Row 0 has 1-3 transform codes (2..6) at random columns + a small motif below."

INVARIANTS = [
    "background is 0",
    "row 0 has 1-3 non-zero command cells with codes in {2, 3, 4, 5, 6} at distinct columns",
    "below row 0 is a connected motif (2-4 cells) in some non-bg color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_commands", "no_motif", "identity_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_cmds":         {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "= n_cmds+1", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "row0_cmds_motif_below",
                       "valid": "row0_cmds_motif_below"},
    "n_distinct_colors": {"type": "int", "default": "= n_cmds+1", "valid": "2..5"},
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
        n_cmds = ctx.draw_int("n_cmds", 1, 1)
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        n_cmds = ctx.draw_int("n_cmds", 3, 4)
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        n_cmds = ctx.draw_int("n_cmds", 1, 3)
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), n_cmds)
    cols.sort()
    for c in cols:
        g[0][c] = rng.randint(2, 6)
    motif_color = rng.choice([1, 7, 8, 9])
    cells = [(0, 0)]
    seen = {(0, 0)}
    target = rng.randint(2, 4)
    while len(cells) < target:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc))
            seen.add((nr, nc))
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
    r0 = rng.randint(2, h - sh)
    c0 = rng.randint(0, w - sw)
    for r, c in cells:
        g[r0 + r - min(rs)][c0 + c - min(cs)] = motif_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_commands":
        # Motif but row 0 is empty — rule's command sequence is empty,
        # transform pipeline degenerates to identity.
        for r, c in [(3, 2), (3, 3), (4, 3)]: g[r][c] = 1
        return g
    if name == "no_motif":
        # Commands but no motif below — rule has nothing to transform
        # and crop.
        g[0][2] = 3; g[0][7] = 5
        return g
    if name == "identity_only":
        # Motif is rotation/flip-symmetric — even after applying
        # commands, transformed crop equals original; rule's effect
        # is invisible.
        for r, c in [(3, 4), (3, 5), (4, 4), (4, 5)]: g[r][c] = 1
        g[0][2] = 4
        return g
    return g
