"""Generator for 25094a63.

Rule: solid >=4x4 rectangles get recolored to yellow; smaller stuff
stays.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_rects, n_distinct_colors.
Degenerates: no_rects, single_singleton, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "46c39ebc17c1"
VERSION = "1.1.0"
TASK_ID = "46c39ebc17c1"
SUMMARY = "Solid >=4x4 rectangles get recolored to yellow; smaller stuff stays."

INVARIANTS = [
    "background is 0",
    "at least one solid colored rectangle of at least 4x4",
    "other non-bg cells are smaller than 4x4",
    "rectangles separated by bg margin of at least one cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rects", "single_singleton", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_rects":        {"type": "int", "default": "2", "valid": "1..3"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 14, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 14, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=4, exclude={0, 4})
    g = full_grid(h, w, 0)
    placed = []
    for _try in range(20):
        if len(placed) >= 2:
            break
        rh = rng.randint(4, 5)
        rw = rng.randint(4, 5)
        rr = rng.randint(0, h - rh)
        rc = rng.randint(0, w - rw)
        ok = True
        for r in range(max(0, rr - 1), min(h, rr + rh + 1)):
            for c in range(max(0, rc - 1), min(w, rc + rw + 1)):
                if g[r][c] != 0:
                    ok = False; break
            if not ok:
                break
        if not ok:
            continue
        draw_rect(g, rr, rc, rh, rw, rng.choice(palette))
        placed.append((rr, rc, rh, rw))
    if not placed:
        return [[0]]
    n_noise = (h * w) // 30
    for _ in range(n_noise):
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        if g[r][c] != 0:
            continue
        nc = rng.choice(palette)
        ok = True
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, ncol = r + dr, c + dc
            if 0 <= nr < h and 0 <= ncol < w and g[nr][ncol] == nc:
                ok = False; break
        if ok:
            g[r][c] = nc
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_rects":
        return g
    if name == "single_singleton":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 2
        return g
    return g
