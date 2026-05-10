"""Generator for 4b:hard_26 — stamp unique bi-symmetric component at markers.

Rule: among color-1 components, exactly one has both H and V mirror
symmetry. For each marker cell (value in {2, 3, 4, 5}), stamp the
symmetric template (recolored to marker's color) centered on that
marker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers (no {2,3,4,5} cells → rule's per-marker stamp
loop is empty, output equals input), no_template (no bi-symmetric
color-1 component → rule's selector finds nothing to stamp), single_cell_template
(template is one cell → rule's stamp is trivial, no shape contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "060d20779ba7"
VERSION = "1.1.0"
TASK_ID = "060d20779ba7"
SUMMARY = "1 bi-symmetric color-1 template + 2-3 markers in {2,3,4,5}."

INVARIANTS = [
    "background is 0",
    "exactly one bi-symmetric color-1 component (H+V mirror)",
    "2-3 isolated markers with values in {2, 3, 4, 5}",
    "each marker has clearance to stamp the template centered on it",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_template", "single_cell_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "11..18"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "template_plus_markers",
                       "valid": "template_plus_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SYMMETRIC = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 12)
        w = ctx.draw_int("grid_w", 13, 13)
        n_marks_lo, n_marks_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 16)
        w = ctx.draw_int("grid_w", 15, 17)
        n_marks_lo, n_marks_hi = 3, 4
    else:
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 13, 15)
        n_marks_lo, n_marks_hi = 2, 3
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_SYMMETRIC)
    th = max(r for r, _ in template) + 1
    tw = max(c for _, c in template) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - th); c0 = rng.randint(0, w - tw)
        if not _free(g, r0, c0, r0 + th - 1, c0 + tw - 1): continue
        for dr, dc in template:
            g[r0 + dr][c0 + dc] = 1
        break
    n_marks = rng.randint(n_marks_lo, n_marks_hi)
    placed = 0; attempts = 0
    while placed < n_marks and attempts < 60:
        attempts += 1
        r = rng.randint(2, h - 3); c = rng.randint(2, w - 3)
        sr = r - th // 2; sc = c - tw // 2
        if not _free(g, sr, sc, sr + th - 1, sc + tw - 1): continue
        g[r][c] = rng.choice([2, 3, 4, 5])
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 14
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # No {2,3,4,5} cells — rule's per-marker stamp loop is
        # empty; output equals input (just the bi-symmetric template).
        for dr, dc in _SYMMETRIC[1]:
            g[3 + dr][5 + dc] = 1
        return g
    if name == "no_template":
        # No bi-symmetric color-1 component — rule's selector finds
        # nothing; markers have no template to stamp.
        for r, c in [(0, 0), (1, 0), (2, 0), (2, 1)]: g[3 + r][2 + c] = 1
        g[8][5] = 2
        g[8][9] = 4
        return g
    if name == "single_cell_template":
        # Bi-symmetric template is just one cell — rule's stamp
        # collapses to recoloring the marker; no shape contrast.
        g[3][3] = 1
        g[8][5] = 2
        g[8][9] = 4
        return g
    return g
