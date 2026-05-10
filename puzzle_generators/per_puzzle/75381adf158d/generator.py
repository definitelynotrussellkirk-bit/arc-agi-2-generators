"""Generator for arc_puzzle_bank_21_set11_s:S11_M2 — Fill Only Enclosed Holes.

Rule: `(rule! (fill-all-enclosed g 8 0))`
  Every bg(0) cell that is NOT reachable from the grid border by a
  bg-cell path becomes color 8. Open frames (which bg can reach via
  the gap) stay un-filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_closed,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_closed_frame, frame_touches_border, all_open_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "75381adf158d"
VERSION = "1.1.0"
TASK_ID = "75381adf158d"
SUMMARY = "Closed rectangle frames (and optional open frames); fill enclosed bg with 8."

INVARIANTS = [
    "at least one closed rectangle of size >= 3x3 (interior cell exists)",
    "rectangles never overlap",
    "rectangles never touch the grid border (so open-side detection is well-defined)",
    "frame colors in 1..9 \\ {8}, distinct per rectangle",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_closed_frame", "frame_touches_border", "all_open_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 10..16", "valid": "6..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_closed":       {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
        n_closed = ctx.draw_int("n_closed", 1, 2)
        n_open = ctx.draw_int("n_open", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 14, 16)
        n_closed = ctx.draw_int("n_closed", 2, 3)
        n_open = ctx.draw_int("n_open", 1, 2)
    else:
        h = ctx.draw_int("grid_h", 8, 14)
        w = ctx.draw_int("grid_w", 10, 16)
        n_closed = ctx.draw_int("n_closed", 1, 3)
        n_open = ctx.draw_int("n_open", 0, 2)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used: list[tuple[int, int, int, int]] = []

    def overlaps_existing(r1, c1, r2, c2):
        for ur1, uc1, ur2, uc2 in used:
            if not (r2 + 1 < ur1 or ur2 + 1 < r1
                    or c2 + 1 < uc1 or uc2 + 1 < c1):
                return True
        return False

    def place_rect():
        for _ in range(50):
            rh = rng.randint(3, max(3, min(5, h - 2)))
            rw = rng.randint(3, max(3, min(7, w - 2)))
            r1 = rng.randint(1, h - rh - 1)
            c1 = rng.randint(1, w - rw - 1)
            r2 = r1 + rh - 1
            c2 = c1 + rw - 1
            if not overlaps_existing(r1, c1, r2, c2):
                return (r1, c1, r2, c2)
        return None

    color_rng = ctx.draw_rng("colors")
    available_colors = [c for c in range(1, 10) if c != 8]
    color_rng.shuffle(available_colors)
    color_iter = iter(available_colors)

    n_closed_placed = 0
    for _ in range(n_closed):
        rect = place_rect()
        if rect is None:
            break
        r1, c1, r2, c2 = rect
        try:
            color = next(color_iter)
        except StopIteration:
            break
        for c in range(c1, c2 + 1):
            g[r1][c] = color
            g[r2][c] = color
        for r in range(r1, r2 + 1):
            g[r][c1] = color
            g[r][c2] = color
        used.append(rect)
        n_closed_placed += 1

    if n_closed_placed == 0:
        if h >= 5 and w >= 5:
            r1, c1 = (h // 2) - 1, (w // 2) - 1
            r2, c2 = r1 + 2, c1 + 2
            color = available_colors[0]
            for c in range(c1, c2 + 1):
                g[r1][c] = color; g[r2][c] = color
            for r in range(r1, r2 + 1):
                g[r][c1] = color; g[r][c2] = color
            used.append((r1, c1, r2, c2))

    for _ in range(n_open):
        rect = place_rect()
        if rect is None:
            break
        r1, c1, r2, c2 = rect
        try:
            color = next(color_iter)
        except StopIteration:
            break
        side = rng.choice(("top", "bottom", "left", "right"))
        for c in range(c1, c2 + 1):
            if side != "top":    g[r1][c] = color
            if side != "bottom": g[r2][c] = color
        for r in range(r1, r2 + 1):
            if side != "left":   g[r][c1] = color
            if side != "right":  g[r][c2] = color
        used.append(rect)

    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_closed_frame":
        # nothing to fill — only stray segments, no enclosed interior
        for c in range(2, 6):
            g[3][c] = 4
        for r in range(5, 8):
            g[r][8] = 5
        return g
    if name == "frame_touches_border":
        # frame against border → bg leaks out, "interior" is grid-connected
        for c in range(0, 6):
            g[0][c] = 3
            g[4][c] = 3
        for r in range(0, 5):
            g[r][0] = 3
            g[r][5] = 3
        return g
    if name == "all_open_frames":
        # every frame missing one side → bg fills all interiors via gap
        for c in range(2, 6):
            g[2][c] = 6
            g[5][c] = 6
        for r in range(2, 6):
            g[r][2] = 6  # right side missing
        return g
    return g
