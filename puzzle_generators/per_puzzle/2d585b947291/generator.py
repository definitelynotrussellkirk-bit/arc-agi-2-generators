"""Generator for arc_puzzle_bank_21_set23_bundle:medium_p06 — set-op on color-2 and color-3 cells.

Rule: (0, 0) holds the op (1=union, 2=intersect, 3=symmetric-diff, else=diff).
Color-2 cells (excluding (0, 0)) form set a; color-3 cells form set b. Both
normalized to bbox top-left and combined per the op; output is the result
painted color 4 on a bbox-canvas.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_op (cell (0,0) is bg → rule's op selector returns
nothing, op is undefined), missing_color (no color-2 OR no color-3
cells → rule's set-op has only one operand, undefined for 2-arg ops),
identical_sets (normalized 2-cells == normalized 3-cells → union ==
intersect == that set, sym-diff is empty; op-selection contrast
collapses).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2d585b947291"
VERSION = "1.1.0"
TASK_ID = "2d585b947291"

SUMMARY = "(0,0)=op key; color-2 cluster + color-3 cluster."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds op key (1, 2, 3, or 4)",
    "≥3 color-2 cells (a connected motif) and ≥3 color-3 cells",
    "no other non-bg colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_op", "missing_color", "identical_sets")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "op_marker_plus_two_clusters",
                          "valid": "op_marker_plus_two_clusters"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _build_motif(rng, k):
    cells = [(0, 0)]
    seen = {(0, 0)}
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        n_lo, n_hi = 3, 4
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        n_lo, n_hi = 4, 5
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_lo, n_hi = 3, 5
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        op = rng.choice([1, 2, 3, 4])
        g[0][0] = op
        n_a = rng.randint(n_lo, n_hi)
        cells_a = _build_motif(rng, n_a)
        rs = [r for r, _ in cells_a]; cs = [c for _, c in cells_a]
        sh_a = max(rs) - min(rs) + 1; sw_a = max(cs) - min(cs) + 1
        placed_a = False
        for _ in range(80):
            r0 = rng.randint(1, h - sh_a); c0 = rng.randint(0, w - sw_a)
            cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells_a]
            if any(g[r][c] != 0 for r, c in cells_p):
                continue
            for r, c in cells_p:
                g[r][c] = 2
            placed_a = True; break
        if not placed_a:
            continue
        n_b = rng.randint(n_lo, n_hi)
        cells_b = _build_motif(rng, n_b)
        rs = [r for r, _ in cells_b]; cs = [c for _, c in cells_b]
        sh_b = max(rs) - min(rs) + 1; sw_b = max(cs) - min(cs) + 1
        for _ in range(80):
            r0 = rng.randint(1, h - sh_b); c0 = rng.randint(0, w - sw_b)
            cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells_b]
            if any(g[r][c] != 0 for r, c in cells_p):
                continue
            for r, c in cells_p:
                g[r][c] = 3
            return g
    raise ValueError("could not realize set19 p04 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_op":
        # (0,0) is bg — rule's op selector returns nothing; op undefined.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[5 + dr][7 + dc] = 3
        return g
    if name == "missing_color":
        # No color-3 cells — rule's set-op has only one operand;
        # 2-arg ops are undefined.
        g[0][0] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[3 + dr][3 + dc] = 2
        return g
    if name == "identical_sets":
        # Normalized 2-cells == 3-cells — union == intersect == that
        # set, sym-diff is empty; op-selection contrast collapses.
        g[0][0] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][7 + dc] = 3
        return g
    return g
