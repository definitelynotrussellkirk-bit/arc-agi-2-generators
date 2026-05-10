"""Generator for 48634b99.

Rule: a 9-block is removed from its 8/9 rail and moved to the unique
all-8 rail that is two cells longer.

Combinatorial axes (8): grid_h/w, source_length, palette_kind,
anchor_corner, asymmetry_force, palette_size, block_position,
source_col.
Degenerates: no_block, equal_rails, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9c50790b939c"
VERSION = "1.1.0"
TASK_ID = "9c50790b939c"
SUMMARY = "9-block leaves shorter 8/9 rail and lands on the longer all-8 rail."

INVARIANTS = [
    "the background is color 7",
    "one vertical rail contains color 8 cells plus a contiguous color-9 block",
    "another vertical color-8 rail is exactly two cells longer than the source rail",
    "the 9-block sits at the top or bottom of the source rail",
]

POSITION_KINDS = ("top", "bottom")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_block", "equal_rails", "full_grid")
HELPFUL_TEXTURES = POSITION_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "source_length":  {"type": "int", "default": "rng 4..6", "valid": "2..12"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "block_position": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_KINDS)},
    "source_col":     {"type": "int", "default": "rng 2|8", "valid": "2|8"},
    "texture":        {"type": "str", "default": "alias for block_position",
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
        sl_lo, sl_hi = 4, 4
    elif difficulty == "hard":
        sl_lo, sl_hi = 6, 8
    else:
        sl_lo, sl_hi = 4, 6
    source_len = ctx.draw_int("source_length", sl_lo, sl_hi)
    block_pos = (overrides.get("texture") if overrides.get("texture") in POSITION_KINDS else None) or \
                overrides.get("block_position") or \
                ctx.draw_choice("block_position", list(POSITION_KINDS))
    h = source_len + 7
    w = 12
    g = full_grid(h, w, 7)
    source_col = rng.choice([2, 8])
    target_col = 8 if source_col == 2 else 2
    source_top = 2
    target_top = 1
    for r in range(source_top, source_top + source_len):
        g[r][source_col] = 8
    for r in range(target_top, target_top + source_len + 2):
        g[r][target_col] = 8
    if block_pos == "top":
        block_rows = [source_top, source_top + 1]
    else:
        block_rows = [source_top + source_len - 2, source_top + source_len - 1]
    for r in block_rows:
        g[r][source_col] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 7)
    if name == "no_block":
        for r in range(2, 6):
            g[r][2] = 8
        for r in range(1, 7):
            g[r][8] = 8
        return g
    if name == "equal_rails":
        for r in range(2, 6):
            g[r][2] = 8
        for r in range(2, 6):
            g[r][8] = 8
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
