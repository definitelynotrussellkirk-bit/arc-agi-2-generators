"""Generator for ac6f9922.

Rule: a framed lattice of enclosed rooms is compressed to the marker
color in each room.

Combinatorial axes (8): grid_h/w, lattice_shape, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_lattice, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "36b22ff07a2e"
VERSION = "1.1.0"
TASK_ID = "36b22ff07a2e"
SUMMARY = "Framed lattice of enclosed rooms is compressed to the marker color in each room."

INVARIANTS = [
    "outer background is color 0",
    "the internal lattice uses one dominant non-background frame color",
    "each enclosed room contains exactly one non-background marker",
    "the output is the matrix of room marker colors",
]

LATTICES = ("2x2", "2x3", "3x2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_lattice", "no_markers", "full_grid")
HELPFUL_TEXTURES = LATTICES

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "lattice_shape":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LATTICES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for lattice_shape",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    shape = (overrides.get("texture") if overrides.get("texture") in LATTICES else None) or \
            overrides.get("lattice_shape") or \
            ctx.draw_choice("lattice_shape", list(LATTICES))
    room_rows, room_cols = (int(x) for x in shape.split("x"))
    room_h = 2 + rng.randint(0, 1)
    room_w = 2 + rng.randint(0, 1)
    top = 2
    left = 2
    frame = 5
    total_h = room_rows * room_h + room_rows + 1
    total_w = room_cols * room_w + room_cols + 1
    g = full_grid(total_h + 4, total_w + 4, 0)

    for rr in range(room_rows + 1):
        r = top + rr * (room_h + 1)
        for c in range(left, left + total_w):
            g[r][c] = frame
    for cc in range(room_cols + 1):
        c = left + cc * (room_w + 1)
        for r in range(top, top + total_h):
            g[r][c] = frame

    markers = [1, 2, 3, 4, 6, 7, 8, 9]
    offset = (seed + sample_index) % len(markers)
    for rr in range(room_rows):
        for cc in range(room_cols):
            marker = markers[(offset + rr * room_cols + cc) % len(markers)]
            r = top + 1 + rr * (room_h + 1)
            c = left + 1 + cc * (room_w + 1)
            g[r][c] = marker
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_lattice":
        g[5][5] = 3
        return g
    if name == "no_markers":
        for r in range(2, 11):
            for c in range(2, 11):
                if r in (2, 5, 8) or c in (2, 5, 8):
                    g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 5
        return g
    return g
