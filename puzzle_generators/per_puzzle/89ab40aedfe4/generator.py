"""Generator for 85b81ff1.

Rule: paired top-row markers define hidden columns, sorted by foreground
population.

Combinatorial axes (8): slot_count, fg_color, grid_h, slot_spacing,
row_jitter, palette_kind, anchor_corner, asymmetry_force.
Degenerates: zero_counts, all_same_count, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "89ab40aedfe4"
VERSION = "1.1.0"
TASK_ID = "89ab40aedfe4"
SUMMARY = "Paired top-row markers; rule sorts hidden columns by foreground population."

INVARIANTS = [
    "background is color 0",
    "the foreground color is taken from the top-left cell",
    "top-row marker pairs start each sortable column slot",
    "the second column of each pair is copied into slots ordered by ascending fg count",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("zero_counts", "all_same_count", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "slot_count":     {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "fg_color":       {"type": "color", "default": "rng 1..9", "valid": "1..9"},
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "slot_spacing":   {"type": "int", "default": "3", "valid": "2..4"},
    "row_jitter":     {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        sc_lo, sc_hi = 2, 3
        h_jitter_lo, h_jitter_hi = 0, 1
    elif difficulty == "hard":
        sc_lo, sc_hi = 5, 6
        h_jitter_lo, h_jitter_hi = 2, 3
    else:
        sc_lo, sc_hi = 3, 4
        h_jitter_lo, h_jitter_hi = 0, 2
    slot_count = int(overrides.get("slot_count",
                                   ctx.draw_int("slot_count", sc_lo, sc_hi)))
    slot_count = max(2, min(6, slot_count))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    fg = int(overrides.get("fg_color", rng.choice(pal)))
    spacing = int(overrides.get("slot_spacing", 3))
    jitter = int(overrides.get("row_jitter",
                               ctx.draw_int("row_jitter",
                                            h_jitter_lo, h_jitter_hi)))
    h = 7 + jitter
    w = slot_count * spacing - 1
    g = full_grid(h, w, 0)
    counts = list(range(1, slot_count + 1))
    rng.shuffle(counts)
    for idx, count in enumerate(counts):
        start = idx * spacing
        g[0][start] = fg
        g[0][start + 1] = fg
        rows = list(range(1, h))
        rng.shuffle(rows)
        for r in rows[:count]:
            g[r][start + 1] = fg
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
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "zero_counts":
        g[0][0] = 2; g[0][1] = 2
        g[0][3] = 2; g[0][4] = 2
        return g
    if name == "all_same_count":
        for slot in range(3):
            start = slot * 3
            g[0][start] = 2
            g[0][start + 1] = 2
            g[1][start + 1] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
