"""Generator for puzzle d492a647.

Rule: one non-bg non-gray "marker" cell; rule fills bg cells with same
row+col parity as marker with marker color.

Combinatorial axes (8): grid_h/w, marker_color, marker_position_kind,
n_grays, palette_kind, gray_layout, anchor_corner, asymmetry_force.
Degenerates: no_marker, multiple_markers, all_grays.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c9034f0626e0"
VERSION = "1.1.0"
TASK_ID = "c9034f0626e0"
SUMMARY = "One marker + sparse grays; rule fills bg by marker's row+col parity."

INVARIANTS = [
    "background is 0",
    "exactly one non-bg, non-gray marker cell",
    "sparse gray(5) cells",
    "marker placed before any non-marker non-gray in row-major order",
]

MARKER_POSITION_KINDS = ("center", "spread", "edge", "corners")
GRAY_LAYOUTS = ("scattered", "row", "col", "diag")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_marker", "multiple_markers", "all_grays")
HELPFUL_TEXTURES = MARKER_POSITION_KINDS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 6..14", "valid": "4..18"},
    "grid_w":              {"type": "int", "default": "rng 6..14", "valid": "4..18"},
    "marker_color":        {"type": "color", "default": "rng (≠0,5)",
                            "valid": "1..9 (≠5)"},
    "marker_position_kind": {"type": "str", "default": "rng helpful",
                             "valid": "|".join(MARKER_POSITION_KINDS)},
    "n_grays":             {"type": "int", "default": "rng 2..5", "valid": "0..10"},
    "gray_layout":         {"type": "str", "default": "rng helpful",
                            "valid": "|".join(GRAY_LAYOUTS)},
    "palette_kind":        {"type": "str", "default": "rng helpful",
                            "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":       {"type": "bool", "default": "false",
                            "valid": "true|false"},
    "texture":             {"type": "str", "default": "alias for marker_position_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 6, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    marker_color = int(overrides.get("marker_color", pool[0]))
    if marker_color == 0 or marker_color == 5:
        marker_color = pool[0]
    pos_kind = (overrides.get("texture") or
                overrides.get("marker_position_kind")
                or ctx.draw_choice("marker_position_kind",
                                   list(MARKER_POSITION_KINDS)))
    if pos_kind == "center":
        mr, mc = h // 2, w // 2
    elif pos_kind == "edge":
        mr = rng.choice([0, h - 1])
        mc = rng.randint(0, w - 1)
    elif pos_kind == "corners":
        mr, mc = rng.choice([(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)])
    else:
        mr = rng.randint(0, h - 1)
        mc = rng.randint(0, w - 1)
    g = full_grid(h, w, 0)
    g[mr][mc] = marker_color
    n_grays = int(overrides.get("n_grays",
                                ctx.draw_int("n_grays", 2, 5)))
    n_grays = max(0, min(15, n_grays))
    gray_layout = overrides.get("gray_layout",
                                ctx.draw_choice("gray_layout",
                                                list(GRAY_LAYOUTS)))
    gray_positions = _layout_grays(gray_layout, h, w, n_grays, mr, mc, rng)
    placed_grays = 0
    for r, c in gray_positions:
        if g[r][c] == 0 and (r, c) != (mr, mc):
            g[r][c] = 5
            placed_grays += 1
        if placed_grays >= n_grays:
            break
    if bool(overrides.get("anchor_corner", False)):
        # Move marker to (0, 0) but ensure no other non-bg non-gray before
        for r in range(h):
            for c in range(w):
                if g[r][c] == marker_color:
                    g[r][c] = 0
        g[0][0] = marker_color
    return g


def _layout_grays(layout, h, w, n, mr, mc, rng):
    cells = [(r, c) for r in range(h) for c in range(w)
             if (r, c) != (mr, mc)]
    if layout == "row":
        target_r = (mr + h // 3) % h
        chosen = [(target_r, c) for c in range(w)]
        rest = [c for c in cells if c not in chosen]
        rng.shuffle(rest)
        return chosen + rest
    if layout == "col":
        target_c = (mc + w // 3) % w
        chosen = [(r, target_c) for r in range(h)]
        rest = [c for c in cells if c not in chosen]
        rng.shuffle(rest)
        return chosen + rest
    if layout == "diag":
        diag = [(k, k) for k in range(min(h, w)) if (k, k) != (mr, mc)]
        rest = [c for c in cells if c not in diag]
        rng.shuffle(rest)
        return diag + rest
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    if name == "no_marker":
        for _ in range(5):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = 5
        return g
    if name == "multiple_markers":
        g[0][0] = color
        g[h - 1][w - 1] = rng.choice([c for c in range(1, 10)
                                      if c != color and c != 5])
        return g
    if name == "all_grays":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.5:
                    g[r][c] = 5
        g[h // 2][w // 2] = color
        return g
    return g
