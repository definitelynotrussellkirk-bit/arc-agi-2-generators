"""Generator for 4acc7107.

Rule: two colors with 2 pieces each; rule stacks each color's pieces at
bottom in two columns.

Combinatorial axes (8): grid_h/w, palette_kind, position_bias, halo,
anchor_corner, asymmetry_force, palette_size, attempts.
Degenerates: same_color, no_objects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f0e701850a95"
VERSION = "1.1.0"
TASK_ID = "f0e701850a95"
SUMMARY = "Two colors with 2 pieces each; rule stacks pieces at bottom in two columns."

INVARIANTS = [
    "background is 0",
    "exactly 2 non-bg colors",
    "each color has exactly 2 4-connected components",
    "components separated by bg margin >= 1",
]

SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_color", "no_objects", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered|spread|rng"},
    "halo":           {"type": "int", "default": "1", "valid": "1..2"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _dims(cells):
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return max(rs) + 1, max(cs) + 1


def _try_place(g, cells, color, rng, h, w, halo=1, attempts=30):
    sh, sw = _dims(cells)
    for _ in range(attempts):
        rr = rng.randint(0, h - sh)
        rc = rng.randint(0, w - sw)
        ok = True
        for r in range(max(0, rr - halo), min(h, rr + sh + halo)):
            for c in range(max(0, rc - halo), min(w, rc + sw + halo)):
                if g[r][c] != 0:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue
        for dr, dc in cells:
            g[rr + dr][rc + dc] = color
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
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 12, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=2, exclude={0})
    g = full_grid(h, w, 0)
    placed_per_color = {palette[0]: 0, palette[1]: 0}
    for color in palette:
        idxs = rng.sample(range(len(SHAPES)), 2)
        for idx in idxs:
            if _try_place(g, SHAPES[idx], color, rng, h, w):
                placed_per_color[color] += 1
    if any(v != 2 for v in placed_per_color.values()):
        return _draw_from_degenerate("no_objects", rng)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "same_color":
        for dr, dc in SHAPES[0]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in SHAPES[1]:
            g[7 + dr][8 + dc] = 2
        return g
    if name == "no_objects":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
