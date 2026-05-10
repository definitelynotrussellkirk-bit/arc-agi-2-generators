"""Generator for 45737921.

Rule: for each 8-conn non-bg blob with exactly 2 colors {a, b},
swap a↔b within that blob.

Combinatorial axes (8): grid_h/w, n_blobs, blob_shape_kind,
palette_size, color_pair_distribution, position_bias,
inter_blob_margin, decoy_density.
Degenerates: single_color_blob, no_blobs, all_one_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import (
    H_LINE_3, L_TROMINO_SW, normalize, rect_cells,
)
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "d2a80a6f9495"
VERSION = "1.1.0"
TASK_ID = "d2a80a6f9495"
SUMMARY = "Multi-color 8-conn blobs with 2-color palette; rule swaps the 2 within."

INVARIANTS = [
    "background is 0",
    ">=1 8-conn non-bg blob",
    "each blob uses exactly 2 distinct non-bg colors",
    "blobs don't touch (8-conn separation)",
]

BLOB_SHAPES = ("rect_with_split", "L_pair", "T_pair",
               "block_pair", "diag_pair")
DEGENERATE_TEXTURES = ("single_color_blob", "no_blobs", "all_one_blob")
HELPFUL_TEXTURES = BLOB_SHAPES

AXES = {
    "grid_h":              {"type": "int", "default": "rng 6..14", "valid": "5..18"},
    "grid_w":              {"type": "int", "default": "rng 8..16", "valid": "6..20"},
    "n_blobs":             {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "blob_shape_kind":     {"type": "str", "default": "rng helpful",
                            "valid": "|".join(BLOB_SHAPES)},
    "palette_size":        {"type": "int", "default": "= 2 * n_blobs",
                            "valid": "2..7"},
    "color_pair_distribution": {"type": "str",
                                "default": "rng distinct|repeating",
                                "valid": "distinct|repeating"},
    "position_bias":       {"type": "str", "default": "rng spread|center|edge",
                            "valid": "spread|center|edge"},
    "inter_blob_margin":   {"type": "int", "default": "2", "valid": "1..3"},
    "texture":             {"type": "str", "default": "alias for blob_shape_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 8, 6, 10
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 18, 14, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 14, 8, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_blobs = int(overrides.get("n_blobs",
                                ctx.draw_int("n_blobs", 1, 3)))
    n_blobs = max(1, min(4, n_blobs))
    pair_dist = overrides.get("color_pair_distribution",
                              ctx.draw_choice("color_pair_distribution",
                                              ["distinct", "repeating"]))
    if pair_dist == "distinct":
        n_palette = 2 * n_blobs
    else:
        n_palette = max(2, n_blobs + 1)
    palette = list(ctx.draw_distinct_colors("palette",
                                            n=n_palette, exclude={0}))
    while len(palette) < 2 * n_blobs:
        palette.append(palette[0])
    shape_kind = (overrides.get("texture") or
                  overrides.get("blob_shape_kind")
                  or ctx.draw_choice("blob_shape_kind",
                                     list(BLOB_SHAPES)))
    margin = int(overrides.get("inter_blob_margin", 2))
    g = full_grid(h, w, 0)
    placed = 0
    for i in range(n_blobs):
        cells_a, cells_b = _shape_pair(shape_kind, rng)
        c_a = palette[(2 * i) % len(palette)]
        c_b = palette[(2 * i + 1) % len(palette)]
        for _ in range(20):
            r0 = rng.randint(0, h - 5)
            c0 = rng.randint(0, w - 5)
            full_cells_a = [(r0 + dr, c0 + dc) for dr, dc in cells_a]
            full_cells_b = [(r0 + dr, c0 + dc) for dr, dc in cells_b]
            all_cells = full_cells_a + full_cells_b
            if not all(0 <= r < h and 0 <= c < w for r, c in all_cells):
                continue
            if any(g[r][c] != 0 for r, c in all_cells):
                continue
            ok = True
            for r, c in all_cells:
                for dr in range(-margin, margin + 1):
                    for dc in range(-margin, margin + 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 0 \
                                and (nr, nc) not in all_cells:
                            ok = False; break
                    if not ok: break
                if not ok: break
            if not ok:
                continue
            for r, c in full_cells_a:
                g[r][c] = c_a
            for r, c in full_cells_b:
                g[r][c] = c_b
            placed += 1
            break
    if placed < 1:
        paint_at(g, 1, 1, H_LINE_3, palette[0])
        paint_at(g, 2, 1, [(0, 0), (0, 1), (0, 2)], palette[1])
    return g


def _shape_pair(kind, rng):
    if kind == "rect_with_split":
        a = [(0, 0), (0, 1), (0, 2)]
        b = [(1, 0), (1, 1), (1, 2)]
        return a, b
    if kind == "L_pair":
        a = list(L_TROMINO_SW)
        b = [(2, 1)]
        return a, b
    if kind == "T_pair":
        a = [(0, 0), (0, 1), (0, 2)]
        b = [(1, 1)]
        return a, b
    if kind == "block_pair":
        a = [(0, 0), (0, 1)]
        b = [(1, 0), (1, 1)]
        return a, b
    if kind == "diag_pair":
        a = [(0, 0), (1, 1)]
        b = [(0, 1), (1, 0)]
        return a, b
    return list(H_LINE_3), [(1, 0), (1, 1), (1, 2)]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    if name == "single_color_blob":
        for r in range(2, 5):
            for c in range(2, 5):
                if r < h and c < w:
                    g[r][c] = palette[0]
        return g
    if name == "no_blobs":
        return g
    if name == "all_one_blob":
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[0] if (r + c) % 2 == 0 else palette[1]
        return g
    return g
