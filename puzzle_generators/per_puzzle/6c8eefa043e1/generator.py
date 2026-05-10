"""Generator for puzzle e69241bd.

Rule: gray walls + colored seeds; flood-fill from each seed through bg
cells, blocked by walls, paint with seed color.

Combinatorial axes (8): grid_h/w, n_walls, n_rooms, palette_size,
wall_orientation, palette_kind, position_bias, anchor_corner.
Degenerates: no_walls, all_walls, no_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6c8eefa043e1"
VERSION = "1.1.0"
TASK_ID = "6c8eefa043e1"
SUMMARY = "Gray walls + seeds; rule flood-fills each room with its seed color."

INVARIANTS = [
    "background is 0",
    "gray(5) walls partition into >=2 rooms",
    ">=2 distinct seed colors at single-cell positions",
    "seeds in distinct rooms",
]

WALL_ORIENTATIONS = ("vertical", "horizontal", "cross", "L_split")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_walls", "all_walls", "no_seeds")
HELPFUL_TEXTURES = WALL_ORIENTATIONS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "grid_w":            {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "wall_orientation":  {"type": "str", "default": "rng helpful",
                          "valid": "|".join(WALL_ORIENTATIONS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "wall_position_bias": {"type": "str", "default": "rng spread|center",
                           "valid": "spread|center"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for wall_orientation",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 14, 20
    else:
        h_lo, h_hi = 10, 16
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
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 3)))
    palette = pool[:max(2, n_palette)]
    orient = (overrides.get("texture") or
              overrides.get("wall_orientation")
              or ctx.draw_choice("wall_orientation",
                                 list(WALL_ORIENTATIONS)))
    bias = overrides.get("wall_position_bias",
                         ctx.draw_choice("wall_position_bias",
                                         ["spread", "center"]))
    g = full_grid(h, w, 0)
    rooms = _build_walls(g, orient, bias, h, w, rng)
    for i, room in enumerate(rooms[:len(palette)]):
        if not room:
            continue
        for _try in range(20):
            r, c = rng.choice(room)
            if g[r][c] == 0:
                g[r][c] = palette[i]
                break
    if not any(g[r][c] != 0 and g[r][c] != 5
               for r in range(h) for c in range(w)):
        # Force seeds
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0:
                    g[r][c] = palette[0]
                    break
            else:
                continue
            break
    return g


def _build_walls(g, orient, bias, h, w, rng):
    if orient == "vertical":
        wc = w // 2 if bias == "center" else rng.randint(2, w - 3)
        for r in range(h):
            g[r][wc] = 5
        return [
            [(r, c) for r in range(h) for c in range(wc)],
            [(r, c) for r in range(h) for c in range(wc + 1, w)],
        ]
    if orient == "horizontal":
        wr = h // 2 if bias == "center" else rng.randint(2, h - 3)
        for c in range(w):
            g[wr][c] = 5
        return [
            [(r, c) for r in range(wr) for c in range(w)],
            [(r, c) for r in range(wr + 1, h) for c in range(w)],
        ]
    if orient == "cross":
        wr = h // 2; wc = w // 2
        for r in range(h):
            g[r][wc] = 5
        for c in range(w):
            g[wr][c] = 5
        return [
            [(r, c) for r in range(wr) for c in range(wc)],
            [(r, c) for r in range(wr) for c in range(wc + 1, w)],
            [(r, c) for r in range(wr + 1, h) for c in range(wc)],
            [(r, c) for r in range(wr + 1, h) for c in range(wc + 1, w)],
        ]
    if orient == "L_split":
        wr = h // 2; wc = w // 2
        for r in range(wr + 1):
            g[r][wc] = 5
        for c in range(wc + 1):
            g[wr][c] = 5
        return [
            [(r, c) for r in range(wr) for c in range(wc)],
            [(r, c) for r in range(h) for c in range(wc + 1, w) if r != wr],
            [(r, c) for r in range(wr + 1, h) for c in range(wc)],
        ]
    return [[(r, c) for r in range(h) for c in range(w)]]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_walls":
        g[1][1] = rng.choice([1, 2, 3])
        g[h - 2][w - 2] = rng.choice([4, 6, 7])
        return g
    if name == "all_walls":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    if name == "no_seeds":
        wc = w // 2
        for r in range(h):
            g[r][wc] = 5
        return g
    return g
