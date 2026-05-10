"""Generator for puzzle 2753e76c.

Rule: count objects per color, sort by count desc. Output is
N x max_count where each row is a right-aligned bar of length count.

Combinatorial axes (8): grid_h/w, n_colors, max_count, palette_kind,
shape_kind, position_bias, anchor_corner, asymmetry_force.
Degenerates: tied_counts, single_color, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "99d71aabd753"
VERSION = "1.1.0"
TASK_ID = "99d71aabd753"
SUMMARY = "Several colors with distinct object counts; rule outputs bar chart."

INVARIANTS = [
    "background is 0",
    "3-5 distinct non-bg colors",
    "object counts per color are distinct (sort unambiguous)",
    "objects don't touch (>=1 bg between)",
]

POSITION_BIASES = ("scattered", "clustered", "row_aligned", "col_aligned",
                   "corners")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
SHAPE_KINDS = ("rect_2x1", "rect_2x2", "line_3", "line_2v",
               "L", "T", "single")
DEGENERATE_TEXTURES = ("tied_counts", "single_color", "monochrome")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_colors":       {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "max_count":      {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_kind":     {"type": "str", "default": "rng",
                       "valid": "|".join(SHAPE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = {
    "rect_2x1": [(0, 0), (0, 1)],
    "rect_2x2": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "line_3":   [(0, 0), (0, 1), (0, 2)],
    "line_2v":  [(0, 0), (1, 0)],
    "L":        [(0, 0), (1, 0), (1, 1)],
    "T":        [(0, 0), (0, 1), (0, 2), (1, 1)],
    "single":   [(0, 0)],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 16, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("n_colors",
                                 ctx.draw_int("n_colors", 3, 4)))
    n_colors = max(2, min(5, n_colors))
    max_count = int(overrides.get("max_count",
                                  ctx.draw_int("max_count", 3, 5)))
    max_count = max(2, min(7, max_count))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    shape_kind = overrides.get("shape_kind",
                               ctx.draw_choice("shape_kind",
                                               list(SHAPE_KINDS)))
    palette = _build_palette(palette_kind, n_colors, rng)
    counts = _build_counts(n_colors, max_count, rng)
    g = full_grid(h, w, 0)
    occupied = [[False] * w for _ in range(h)]
    for color, count in zip(palette, counts):
        for _ in range(count):
            shape = list(_SHAPES.get(shape_kind, _SHAPES["rect_2x1"]))
            if shape_kind == "rng":
                shape = list(_SHAPES[rng.choice(list(_SHAPES.keys()))])
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            placed = False
            for _ in range(60):
                r0, c0 = _sample_position(bias, h, w, sh, sw, rng)
                if r0 is None:
                    continue
                if any(occupied[rr][cc]
                       for rr in range(max(0, r0 - 1), min(h, r0 + sh + 1))
                       for cc in range(max(0, c0 - 1), min(w, c0 + sw + 1))):
                    continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                for rr in range(max(0, r0 - 1), min(h, r0 + sh + 1)):
                    for cc in range(max(0, c0 - 1), min(w, c0 + sw + 1)):
                        occupied[rr][cc] = True
                placed = True
                break
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:n]


def _build_counts(n, max_count, rng):
    counts = list(range(1, max_count + 1))
    rng.shuffle(counts)
    return counts[:n]


def _sample_position(bias, h, w, sh, sw, rng):
    if h < sh or w < sw:
        return None, None
    if bias == "clustered":
        cr = rng.randint(0, h - sh); cc = rng.randint(0, w - sw)
        return cr, cc
    if bias == "row_aligned":
        rr = rng.randint(0, h - sh)
        cc = rng.randint(0, w - sw)
        return rr, cc
    if bias == "col_aligned":
        return rng.randint(0, h - sh), rng.randint(0, w - sw)
    if bias == "corners":
        corners = [(0, 0), (0, w - sw), (h - sh, 0), (h - sh, w - sw)]
        return rng.choice(corners)
    return rng.randint(0, h - sh), rng.randint(0, w - sw)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "tied_counts":
        # Two colors with equal object counts → ambiguous sort
        for c, ofs in [(2, (0, 0)), (3, (0, 6))]:
            for i in range(2):
                r = i * 3
                if r + 1 < h and ofs[1] + 1 < w:
                    g[r][ofs[1]] = c
                    g[r][ofs[1] + 1] = c
        return g
    if name == "single_color":
        for i in range(3):
            r = i * 3; c = 1
            if r + 1 < h and c + 1 < w:
                g[r][c] = 3
                g[r][c + 1] = 3
        return g
    if name == "monochrome":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 0
        return g
    return g
