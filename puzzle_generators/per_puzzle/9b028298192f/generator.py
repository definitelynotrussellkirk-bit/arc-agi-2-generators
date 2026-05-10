"""Generator for puzzle cdecee7f.

Rule: take all non-bg cells, sort by column then row, pack their
colors into a 3x3 output grid in row-major snake order.

Combinatorial axes (8): grid_h/w, palette_kind, n_cells, position_bias,
spread_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: collinear, tight_cluster, edge_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9b028298192f"
VERSION = "1.1.0"
TASK_ID = "9b028298192f"
SUMMARY = "9 colored non-bg cells; rule outputs 3x3 in snake order."

INVARIANTS = [
    "background is 0",
    "exactly 9 non-bg cells",
    "9 distinct colors (1..9)",
    "all cells at distinct (row, col) — sort is deterministic",
]

PALETTE_KINDS = ("warm", "cool", "broad", "pastel", "rainbow")
POSITION_BIASES = ("spread", "diagonal", "corners_first", "center", "edge")
DEGENERATE_TEXTURES = ("collinear", "tight_cluster", "edge_only")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..10", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 5..10", "valid": "3..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "spread_factor":  {"type": "float", "default": "rng 0.3..1.0",
                       "valid": "0.1..1"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 9, 14
    else:
        h_lo, h_hi = 5, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    h = max(3, h); w = max(3, w)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    palette = _build_palette(palette_kind, rng)
    g = full_grid(h, w, 0)
    positions = _pick_positions(bias, h, w, rng)
    if bool(overrides.get("anchor_corner", False)) and (0, 0) not in positions:
        positions[0] = (0, 0)
    used = set(); final = []
    for r, c in positions:
        if (r, c) in used:
            continue
        used.add((r, c)); final.append((r, c))
        if len(final) == 9:
            break
    while len(final) < 9:
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if (r, c) not in used:
            used.add((r, c)); final.append((r, c))
    for i, (r, c) in enumerate(final):
        g[r][c] = palette[i]
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [1, 2, 3, 4, 6, 7, 8, 9, 5]
    elif kind == "cool":
        pool = [1, 5, 7, 8, 9, 2, 3, 4, 6]
    elif kind == "pastel":
        pool = [3, 5, 7, 1, 8, 6, 2, 4, 9]
    elif kind == "rainbow":
        pool = [1, 2, 3, 4, 6, 7, 8, 9, 5]
    else:
        pool = list(range(1, 10))
    rng.shuffle(pool)
    return pool[:9]


def _pick_positions(bias, h, w, rng):
    positions = [(r, c) for r in range(h) for c in range(w)]
    if bias == "spread":
        rng.shuffle(positions)
        return positions
    if bias == "diagonal":
        n = min(h, w)
        diag = [(i, i) for i in range(n)]
        anti = [(i, n - 1 - i) for i in range(n)]
        seen = list(set(diag + anti))
        rng.shuffle(seen)
        rest = [p for p in positions if p not in seen]
        rng.shuffle(rest)
        return seen + rest
    if bias == "corners_first":
        corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
        rest = [p for p in positions if p not in corners]
        rng.shuffle(rest)
        return corners + rest
    if bias == "center":
        cr, cc = h // 2, w // 2
        positions.sort(key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))
        return positions
    if bias == "edge":
        positions.sort(key=lambda p: -min(p[0], p[1], h - 1 - p[0], w - 1 - p[1]))
        return positions
    rng.shuffle(positions)
    return positions


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = list(range(1, 10)); rng.shuffle(palette)
    if name == "collinear":
        r = h // 2
        cs = list(range(w)); rng.shuffle(cs)
        for i, c in enumerate(cs[:9]):
            if c < w:
                g[r][c] = palette[i % 9]
        return g
    if name == "tight_cluster":
        cluster = [(r, c) for r in range(min(3, h)) for c in range(min(3, w))]
        rng.shuffle(cluster)
        for i, (r, c) in enumerate(cluster[:9]):
            g[r][c] = palette[i % 9]
        return g
    if name == "edge_only":
        edges = [(0, c) for c in range(w)] + [(h - 1, c) for c in range(w)] \
              + [(r, 0) for r in range(1, h - 1)] + [(r, w - 1) for r in range(1, h - 1)]
        rng.shuffle(edges)
        for i, (r, c) in enumerate(edges[:9]):
            g[r][c] = palette[i % 9]
        return g
    return g
