"""Generator for v3_rich_schema:hard_05_symmetric_object_mirror — mirror obj across vertical 5-bar.

Rule: a vertical color-5 bar splits the grid. Color-4 motifs on the left
side are mirrored to the right in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_bar (no full color-5 column → rule's mirror axis is
undefined), no_motifs (bar present but no color-4 motifs → rule has
nothing to mirror), motif_at_bar (motif overlaps bar column → rule's
"left side" condition violated).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "298700c0dc02"
VERSION = "1.1.0"
TASK_ID = "298700c0dc02"

SUMMARY = "Vertical color-5 bar + 1-2 vertically symmetric color-4 motifs on the left side."

INVARIANTS = [
    "background is 0",
    "exactly one full color-5 column (the bar)",
    "1-2 vertically symmetric color-4 motifs entirely left of the bar",
    "mirror landing cells on the right side are empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bar", "no_motifs", "motif_at_bar")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "n":                 {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "bar_plus_left_motifs",
                          "valid": "bar_plus_left_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
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


SYMMETRIC_MOTIFS = [
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        n = ctx.draw_int("n", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 13, 13)
        n = ctx.draw_int("n", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        n = ctx.draw_int("n", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        bar_col = rng.randint(w // 2, w - 4)
        for r in range(h):
            g[r][bar_col] = 5
        ok = True
        for _ in range(n):
            cells = rng.choice(SYMMETRIC_MOTIFS)
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, bar_col - sw)
                cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
                if any(g[r][c] != 0 for r, c in cells_p): continue
                if not all(0 <= 2 * bar_col - c < w for r, c in cells_p): continue
                if any(g[r][2 * bar_col - c] != 0 for r, c in cells_p): continue
                for r, c in cells_p:
                    g[r][c] = 4
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_bar":
        # No full color-5 column — rule's mirror axis undefined.
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
            g[2 + dr][2 + dc] = 4
        return g
    if name == "no_motifs":
        # Bar present but no color-4 motifs.
        for r in range(h):
            g[r][6] = 5
        return g
    if name == "motif_at_bar":
        # Motif overlaps bar column — "left side" condition violated.
        for r in range(h):
            g[r][6] = 5
        g[3][5] = 4; g[3][6] = 4; g[3][7] = 4
        g[4][6] = 4
        return g
    return g
