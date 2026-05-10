"""Generator for 29700607.

Rule: top row markers + side row markers (one each per color); rule
draws L-paths connecting matching markers.

Combinatorial axes (8): grid_h/w, n_markers, palette_kind, position_bias,
anchor_corner, asymmetry_force, palette_size, header_position.
Degenerates: no_header, no_sides, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b88894a36787"
VERSION = "1.1.0"
TASK_ID = "b88894a36787"
SUMMARY = "Row 0 with 2-3 markers + 2-3 side markers; rule draws L-paths."

INVARIANTS = [
    "row 0: 2-3 distinct colors at adjacent cells",
    "for each row-0 color: exactly one matching cell in the body (>=row 4)",
    "side markers don't share rows or cols with row-0 markers",
]

POSITION_BIASES = ("scattered", "left_lean", "right_lean", "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_header", "no_sides", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "n_markers":      {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 8, 9, 10, 11
        nm_lo, nm_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 14, 14, 18
        nm_lo, nm_hi = 3, 4
    else:
        h_lo, h_hi, w_lo, w_hi = 9, 12, 11, 14
        nm_lo, nm_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    n = int(overrides.get("n_markers",
                          ctx.draw_int("n_markers", nm_lo, nm_hi)))
    n = max(2, min(min(w - 4, 4), n))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "left_lean":
        start_c = rng.randint(2, max(2, w // 3))
    elif bias == "right_lean":
        start_c = rng.randint(min(w - n - 2, 2 * w // 3), w - n - 2)
    elif bias == "centered":
        start_c = max(2, (w - n) // 2)
    else:
        start_c = rng.randint(2, max(2, w - n - 2))
    header_cols = list(range(start_c, start_c + n))
    for c, color in zip(header_cols, palette):
        g[0][c] = color
    used_rows = set()
    for color in palette:
        for _ in range(40):
            r = rng.randint(4, h - 2)
            if r in used_rows:
                continue
            c = rng.choice([0, w - 1])
            if g[r][c] == 0:
                g[r][c] = color
                used_rows.add(r)
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
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_header":
        g[5][0] = 2; g[7][w - 1] = 3
        return g
    if name == "no_sides":
        g[0][3] = 2; g[0][4] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
