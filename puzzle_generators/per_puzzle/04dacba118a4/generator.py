"""Generator for arc_puzzle_bank_21_set22_bundle:hard_p02 — (0,0) key + 2 motifs (colors 2 and 3).

Rule: (0, 0) holds an op key (1 or 2). Two motifs in colors 2 and 3 are
combined; output uses overlay-priority based on key.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, missing_motif, identical_motifs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "04dacba118a4"
VERSION = "1.1.0"
TASK_ID = "04dacba118a4"

SUMMARY = "(0,0)=op key (1 or 2) + color-2 motif + color-3 motif at distinct positions."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds an op key (1 or 2)",
    "≥3 color-2 cells (a connected motif) and ≥3 color-3 cells",
    "no other non-bg colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "missing_motif", "identical_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "key_corner_with_two_motifs",
                       "valid": "key_corner_with_two_motifs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        g[0][0] = rng.choice([1, 2])
        for color in (2, 3):
            cells = _build_motif(rng, rng.randint(3, 5))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(80):
                r0 = rng.randint(1, h - sh); c0 = rng.randint(0, w - sw)
                cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
                if any(g[r][c] != 0 for r, c in cells_p): continue
                for r, c in cells_p:
                    g[r][c] = color
                placed = True; break
            if not placed:
                break
        else:
            return g
    raise ValueError("could not realize set22 p02 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_key":
        # Both motifs but (0,0) empty — rule's op key lookup
        # fails; overlay priority undefined.
        for r, c in [(2, 2), (3, 2), (3, 3)]: g[r][c] = 2
        for r, c in [(5, 6), (6, 6), (6, 7)]: g[r][c] = 3
        return g
    if name == "missing_motif":
        # Key + only one motif — rule's combine has only one
        # operand; output trivially that operand.
        g[0][0] = 1
        for r, c in [(2, 2), (3, 2), (3, 3)]: g[r][c] = 2
        return g
    if name == "identical_motifs":
        # Both motifs at the exact same positions (encoded by
        # placing 2 then 3 over 2) — overlap means rule's
        # priority key actually decides; degenerate yields all-3
        # or all-2 depending on key.
        g[0][0] = 1
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 2
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 3
        return g
    return g
