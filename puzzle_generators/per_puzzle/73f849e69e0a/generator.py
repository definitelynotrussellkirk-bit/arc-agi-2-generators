"""Generator for puzzle b4a43f3b.

Rule: top 5-row icon (stride-2 sample) + 5-sep + bottom red(2) cells.
Output: stamp icon at each red position; 3*bot_h x 3*bot_w.

Combinatorial axes (8): grid_h/w, icon_density, palette_kind,
n_twos, bottom_position_bias, anchor_corner, asymmetry_force,
include_decoy.
Degenerates: empty_icon, no_twos, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "73f849e69e0a"
VERSION = "1.1.0"
TASK_ID = "73f849e69e0a"
SUMMARY = "Top icon + 5-sep + bottom 2s; rule stamps icon at each 2-position."

INVARIANTS = [
    "top rows 0..4 with non-zero only at stride-2 positions",
    "row 5 is all gray(5)",
    "bottom rows 6..h-1 have 1-3 red(2) cells",
    "icon has >=1 non-zero",
]

POSITION_BIASES = ("scattered", "diagonal", "row_aligned", "col_aligned",
                   "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_icon", "no_twos", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":           {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":           {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "icon_density":     {"type": "float", "default": "rng 0.4..0.7",
                         "valid": "0.2..1"},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "n_twos":           {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "bottom_position_bias":{"type": "str", "default": "rng helpful",
                            "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "asymmetry_force":  {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for bottom_position_bias",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 10, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo - 4, h_hi - 4)
    w = max(5, w)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 2, rng)
    icon_density = float(overrides.get("icon_density",
                                       ctx.draw_rng("icon_density")
                                       .uniform(0.4, 0.7)))
    n_twos = int(overrides.get("n_twos",
                               ctx.draw_int("n_twos", 1, 3)))
    n_twos = max(1, min(5, n_twos))
    bias = (overrides.get("texture") or
            overrides.get("bottom_position_bias")
            or ctx.draw_choice("bottom_position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    icon = []
    for dr in range(3):
        row = []
        for dc in range(3):
            if rng.random() < icon_density:
                row.append(rng.choice(palette))
            else:
                row.append(0)
        icon.append(row)
    if all(v == 0 for row in icon for v in row):
        icon[1][1] = palette[0]
    for dr in range(3):
        for dc in range(3):
            if icon[dr][dc] != 0 and 2 * dr < h and 2 * dc < w:
                g[2 * dr][2 * dc] = icon[dr][dc]
    sep_row = 5
    if sep_row < h:
        for c in range(w):
            g[sep_row][c] = 5
    bot_start = sep_row + 1
    placed_twos = 0
    candidates = _bottom_candidates(bias, h, w, bot_start, rng)
    for r, c in candidates:
        if placed_twos >= n_twos:
            break
        if 0 <= r < h and 0 <= c < w and g[r][c] == 0:
            g[r][c] = 2
            placed_twos += 1
    if placed_twos < 1:
        # Force one
        if bot_start < h:
            g[bot_start][0] = 2
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 3, 4]
    else:
        pool = [1, 3, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (2, 5)]
    rng.shuffle(pool)
    return pool[:n]


def _bottom_candidates(bias, h, w, bot_start, rng):
    if bias == "diagonal":
        return [(bot_start + i, i) for i in range(min(h - bot_start, w))]
    if bias == "row_aligned":
        r = (bot_start + h - 1) // 2
        return [(r, c) for c in range(0, w, 2)]
    if bias == "col_aligned":
        c = w // 2
        return [(r, c) for r in range(bot_start, h)]
    if bias == "centered":
        cr = (bot_start + h - 1) // 2; cc = w // 2
        cells = [(r, c) for r in range(bot_start, h) for c in range(w)]
        cells.sort(key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))
        return cells
    cells = [(r, c) for r in range(bot_start, h) for c in range(w)]
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    sep_row = 5
    if sep_row < h:
        for c in range(w):
            g[sep_row][c] = 5
    if name == "empty_icon":
        # No icon cells — rule has nothing to stamp
        bot_start = sep_row + 1
        if bot_start < h and w > 0:
            g[bot_start][0] = 2
        return g
    if name == "no_twos":
        # Icon but no 2s
        g[0][0] = 3
        g[0][2] = 3
        g[2][0] = 3
        g[2][2] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 4
        return g
    return g
