"""Generator for puzzle 760b3cac.

Rule: yellow plus-arrow with apex offset indicates direction (left/right).
Reflect cyan blob across cyan's right edge (right-arrow) or left edge.

Combinatorial axes (8): grid_h/w, direction, cyan_h, cyan_w,
cyan_density, arrow_position, anchor_corner, asymmetry_force.
Degenerates: no_arrow, no_cyan, ambiguous_arrow.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0ed4fa8c0b40"
VERSION = "1.1.0"
TASK_ID = "0ed4fa8c0b40"
SUMMARY = "Cyan blob + yellow arrow; rule reflects cyan based on arrow direction."

INVARIANTS = [
    "background is 0",
    "exactly one cyan blob with 3-7 cells",
    "yellow arrow: plus + apex offset by +1 or -1 (left/right)",
    "cyan position chosen so reflected cells fit in-bounds",
]

DIRECTION_KINDS = ("left", "right", "rng")
ARROW_POSITIONS = ("center", "lower_center", "upper_center")
DEGENERATE_TEXTURES = ("no_arrow", "no_cyan", "ambiguous_arrow")
HELPFUL_TEXTURES = DIRECTION_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..18"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTION_KINDS)},
    "cyan_h":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "cyan_w":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "cyan_density":   {"type": "float", "default": "rng 0.5..0.9",
                       "valid": "0.3..1"},
    "arrow_position": {"type": "str", "default": "lower_center",
                       "valid": "|".join(ARROW_POSITIONS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 7, 9
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 3, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    direction_kind = (overrides.get("texture") or
                      overrides.get("direction")
                      or ctx.draw_choice("direction",
                                         list(DIRECTION_KINDS)))
    if direction_kind == "right":
        direction = 1
    elif direction_kind == "left":
        direction = -1
    else:
        direction = rng.choice([-1, 1])
    cyan_h = int(overrides.get("cyan_h",
                               ctx.draw_int("cyan_h", 2, 3)))
    cyan_w = int(overrides.get("cyan_w",
                               ctx.draw_int("cyan_w", 2, 3)))
    cyan_h = max(1, min(4, cyan_h))
    cyan_w = max(1, min(4, cyan_w))
    density = float(overrides.get("cyan_density",
                                  ctx.draw_rng("cyan_density")
                                  .uniform(0.5, 0.9)))
    arrow_pos = overrides.get("arrow_position", "lower_center")
    g = full_grid(h, w, 0)
    if direction == 1:
        cyan_c_start = rng.randint(2, max(2, w // 2 - cyan_w))
    else:
        cyan_c_start = rng.randint(min(w // 2, w - cyan_w - 2),
                                   max(w // 2, w - cyan_w - 2))
    cyan_r = rng.randint(0, max(0, 1))
    cells_pool = [(r, c) for r in range(cyan_r, cyan_r + cyan_h)
                  for c in range(cyan_c_start, cyan_c_start + cyan_w)]
    n = max(3, int(len(cells_pool) * density))
    n = min(n, len(cells_pool))
    chosen = rng.sample(cells_pool, n)
    for r, c in chosen:
        g[r][c] = 8
    yc_center = w // 2
    if arrow_pos == "center":
        yr_top = h // 2 - 1
    elif arrow_pos == "upper_center":
        yr_top = 1
    else:
        yr_top = h - 4
    if yr_top < 0:
        yr_top = 0
    if yr_top + 2 >= h:
        yr_top = h - 3
    g[yr_top + 1][yc_center - 1] = 4
    g[yr_top + 1][yc_center] = 4
    g[yr_top + 1][yc_center + 1] = 4
    if yr_top + 2 < h:
        g[yr_top + 2][yc_center] = 4
    apex_col = yc_center + direction
    if 0 <= apex_col < w and yr_top >= 0:
        g[yr_top][apex_col] = 4
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_arrow":
        g[0][1] = 8
        g[0][2] = 8
        return g
    if name == "no_cyan":
        yc = w // 2; yr = h - 4
        g[yr + 1][yc - 1] = 4
        g[yr + 1][yc] = 4
        g[yr + 1][yc + 1] = 4
        g[yr + 2][yc] = 4
        g[yr][yc + 1] = 4
        return g
    if name == "ambiguous_arrow":
        # Two apex cells (one on each side)
        yc = w // 2; yr = h - 4
        g[yr + 1][yc - 1] = 4
        g[yr + 1][yc] = 4
        g[yr + 1][yc + 1] = 4
        g[yr][yc - 1] = 4
        g[yr][yc + 1] = 4
        g[0][1] = 8; g[0][2] = 8
        return g
    return g
