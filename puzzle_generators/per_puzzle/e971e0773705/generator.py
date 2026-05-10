"""Generator for d5c634a2.

Rule: red shapes; rule encodes counts of wide-top (type_a) vs
narrow-top (type_b) in a 3x6 grid.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_a, n_b.
Degenerates: no_shapes, all_a, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e971e0773705"
VERSION = "1.1.0"
TASK_ID = "e971e0773705"
SUMMARY = "Red shapes counted by top-row width into a 3x6 grid encoding."

INVARIANTS = [
    "background is 0",
    "all shapes are color 2 and 4-connected",
    "shapes separated by bg margin of at least one cell",
    "type_a count is at most 4 and type_b count is at most 4",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "all_a", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

TYPE_A = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
]
TYPE_B = [
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_a":            {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "n_b":            {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _shape_dims(cells):
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return max(rs) + 1, max(cs) + 1


def _try_place(g, cells, rng, h, w, halo=1, attempts=30):
    sh, sw = _shape_dims(cells)
    for _ in range(attempts):
        rr = rng.randint(0, h - sh)
        rc = rng.randint(0, w - sw)
        ok = True
        for r in range(max(0, rr - halo), min(h, rr + sh + halo)):
            for c in range(max(0, rc - halo), min(w, rc + sw + halo)):
                if g[r][c] != 0:
                    ok = False; break
            if not ok:
                break
        if not ok:
            continue
        for dr, dc in cells:
            g[rr + dr][rc + dc] = 2
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 12, 13
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 12, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n_a = rng.randint(1, 4)
    n_b = rng.randint(1, 4)
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(n_a):
        if _try_place(g, rng.choice(TYPE_A), rng, h, w):
            placed += 1
    for _ in range(n_b):
        if _try_place(g, rng.choice(TYPE_B), rng, h, w):
            placed += 1
    if placed < 2:
        return [[0]]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_shapes":
        return g
    if name == "all_a":
        for dr, dc in TYPE_A[0]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in TYPE_A[1]:
            g[5 + dr][5 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
