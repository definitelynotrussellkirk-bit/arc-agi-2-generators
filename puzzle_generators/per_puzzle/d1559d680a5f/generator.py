"""Generator for 2697da3f.

Rule: a single-color motif is stamped with rotations and reflection
into a larger square.

Combinatorial axes (8): motif, color, palette_kind, grid_size,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_motif, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d1559d680a5f"
VERSION = "1.1.0"
TASK_ID = "d1559d680a5f"
SUMMARY = "Single-color motif stamped with rotations and reflection into a larger square."

INVARIANTS = [
    "all nonzero cells share one color",
    "the source motif has a compact bounding box",
    "the output size is determined by the motif bounding box",
    "the rule stamps the motif, both quarter rotations, and a left-right reflection",
]

MOTIFS = {
    "l": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    "t": [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    "stair": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    "zig": [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
}
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_motif", "full_grid", "single_cell")
HELPFUL_TEXTURES = tuple(MOTIFS.keys())

AXES = {
    "motif":          {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES)},
    "color":          {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "grid_size":      {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "centered|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for motif",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    motif_name = (overrides.get("texture") if overrides.get("texture") in MOTIFS else None) or \
                 overrides.get("motif") or \
                 ctx.draw_choice("motif", tuple(MOTIFS))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    color = int(overrides.get("color",
                              rng.choice(pal) if pal else
                              ctx.draw_color("color", exclude={0})))
    if difficulty == "easy":
        s_lo, s_hi = 5, 7
    elif difficulty == "hard":
        s_lo, s_hi = 9, 14
    else:
        s_lo, s_hi = 6, 9
    size = int(overrides.get("grid_size",
                             rng.randint(s_lo, s_hi)))
    size = max(5, min(14, size))
    g = full_grid(size, size, 0)
    r0 = rng.randint(1, max(1, size - 4))
    c0 = rng.randint(1, max(1, size - 4))
    for dr, dc in MOTIFS[motif_name]:
        if r0 + dr < size and c0 + dc < size:
            g[r0 + dr][c0 + dc] = color
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    size = 7
    g = full_grid(size, size, 0)
    if name == "no_motif":
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = 2
        return g
    if name == "single_cell":
        g[3][3] = 2
        return g
    return g
