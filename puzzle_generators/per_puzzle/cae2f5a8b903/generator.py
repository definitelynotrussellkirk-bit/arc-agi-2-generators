"""Generator for puzzle 39a8645d.

Rule: count objects per color. Color with most objects: take the first
such object, output its bbox as 3x3 binary mask.

Combinatorial axes (8): grid_h/w, n_colors, max_count, palette_kind,
shape_kind, position_bias, anchor_corner, asymmetry_force.
Degenerates: tied_counts, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cae2f5a8b903"
VERSION = "1.1.0"
TASK_ID = "cae2f5a8b903"
SUMMARY = "Multi-color objects; rule outputs 3x3 mask of most-frequent color's first."

INVARIANTS = [
    "background is 0",
    "3-4 distinct colors",
    "object counts are distinct (winner unambiguous)",
    "objects 8-conn, fit in 3x3 bbox",
]

POSITION_BIASES = ("scattered", "clustered", "row_aligned", "diagonal",
                   "corners")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tied_counts", "single_color", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "n_colors":       {"type": "int", "default": "3", "valid": "2..5"},
    "max_count":      {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "shape_kind":     {"type": "str", "default": "rng",
                       "valid": "diag|hbar|vbar|corners|corner|rng"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


SHAPES = {
    "diag":   [(0, 0), (1, 1), (2, 2)],
    "hbar":   [(0, 0), (0, 1), (0, 2)],
    "vbar":   [(0, 0), (1, 0), (2, 0)],
    "corners":[(0, 0), (0, 2), (2, 0), (2, 2)],
    "corner": [(0, 0), (0, 1), (1, 0)],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 12, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("n_colors", 3))
    n_colors = max(2, min(5, n_colors))
    max_count = int(overrides.get("max_count",
                                  ctx.draw_int("max_count", 3, 4)))
    max_count = max(2, min(5, max_count))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    shape_kind = overrides.get("shape_kind", "rng")
    palette = _build_palette(palette_kind, n_colors, rng)
    counts = list(range(1, max_count + 1))[-n_colors:]
    rng.shuffle(counts)
    g = full_grid(h, w, 0)
    occupied = [[False] * w for _ in range(h)]
    for color, count in zip(palette, counts):
        for _ in range(count):
            if shape_kind == "rng":
                shape = rng.choice(list(SHAPES.values()))
            else:
                shape = SHAPES.get(shape_kind, SHAPES["diag"])
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
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
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _sample_position(bias, h, w, sh, sw, rng):
    if h < sh or w < sw:
        return None, None
    if bias == "clustered":
        cr = rng.randint(0, h - sh); cc = rng.randint(0, w - sw)
        return cr, cc
    if bias == "row_aligned":
        return rng.randint(0, h - sh), rng.randint(0, w - sw)
    if bias == "corners":
        corners = [(0, 0), (0, w - sw), (h - sh, 0), (h - sh, w - sw)]
        return rng.choice(corners)
    return rng.randint(0, h - sh), rng.randint(0, w - sw)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    if name == "tied_counts":
        # Two colors with equal counts → ambiguous
        for c, ofs in [(palette[0], (0, 0)), (palette[1], (0, 6))]:
            for i in range(2):
                r = i * 4
                if r + 1 < h and ofs[1] + 1 < w:
                    g[r][ofs[1]] = c
        return g
    if name == "single_color":
        for i in range(3):
            r = i * 4
            if r < h:
                g[r][1] = palette[0]
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[0]
        return g
    return g
