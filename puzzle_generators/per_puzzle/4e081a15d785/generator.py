"""Generator for puzzle 746b3537.

Rule: each row is uniform color; rule dedupes consecutive duplicates.

Combinatorial axes (8): grid_h/w, base_color_count, palette_kind,
n_duplicates, color_sequence_kind, anchor_endpoints, asymmetry_force,
duplicate_position_bias.
Degenerates: monochrome, all_unique, single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx

GENERATOR_ID = "4e081a15d785"
VERSION = "1.1.0"
TASK_ID = "4e081a15d785"
SUMMARY = "Solid-color rows with consecutive duplicates; rule dedupes."

INVARIANTS = [
    "each row uniformly one color",
    ">=2 distinct colors after dedup",
    ">=1 consecutive duplicate row pair",
]

COLOR_SEQUENCE_KINDS = ("alternating", "ascending", "shuffled",
                        "stripes", "blocks")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("monochrome", "all_unique", "single_row")
HELPFUL_TEXTURES = COLOR_SEQUENCE_KINDS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 4..15", "valid": "2..18"},
    "grid_w":             {"type": "int", "default": "rng 3..18", "valid": "1..22"},
    "base_color_count":   {"type": "int", "default": "rng 2..6", "valid": "2..9"},
    "palette_kind":       {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PALETTE_KINDS)},
    "color_sequence_kind": {"type": "str", "default": "rng helpful",
                            "valid": "|".join(COLOR_SEQUENCE_KINDS)},
    "n_duplicates":       {"type": "int", "default": "rng 1..4", "valid": "0..8"},
    "anchor_endpoints":   {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "duplicate_position_bias": {"type": "str",
                                "default": "rng spread|center|edge",
                                "valid": "spread|center|edge"},
    "texture":            {"type": "str", "default": "alias for color_sequence_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 2, 5, 1, 5
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 18, 14, 22
    else:
        h_lo, h_hi, w_lo, w_hi = 4, 15, 3, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = list(range(10))
    rng.shuffle(pool)
    n_colors = int(overrides.get("base_color_count",
                                 ctx.draw_int("base_color_count", 2, 6)))
    palette = pool[:max(2, n_colors)]
    seq_kind = (overrides.get("texture") or
                overrides.get("color_sequence_kind")
                or ctx.draw_choice("color_sequence_kind",
                                   list(COLOR_SEQUENCE_KINDS)))
    cols = _draw_color_sequence(seq_kind, h, palette, rng)
    n_dup = int(overrides.get("n_duplicates",
                              ctx.draw_int("n_duplicates", 1, 4)))
    n_dup = max(0, min(8, n_dup))
    bias = overrides.get("duplicate_position_bias",
                         ctx.draw_choice("duplicate_position_bias",
                                         ["spread", "center", "edge"]))
    for _ in range(n_dup):
        if len(cols) >= 30:
            break
        loc = _pick_dup_loc(bias, len(cols), rng)
        cols = cols[:loc + 1] + [cols[loc]] + cols[loc + 1:]
    g = [[c] * w for c in cols]
    return g


def _draw_color_sequence(kind, n, palette, rng):
    cols = []
    last = -1
    if kind == "alternating":
        for i in range(n):
            cols.append(palette[i % len(palette)])
        return cols
    if kind == "ascending":
        for i in range(n):
            cols.append(palette[min(i, len(palette) - 1)])
        return cols
    if kind == "stripes":
        block_size = max(1, n // 3)
        for i in range(n):
            cols.append(palette[(i // block_size) % len(palette)])
        return cols
    if kind == "blocks":
        for i in range(n):
            cols.append(palette[(i // 2) % len(palette)])
        return cols
    for _ in range(n):
        choices = [c for c in palette if c != last]
        c = rng.choice(choices) if choices else palette[0]
        cols.append(c)
        last = c
    return cols


def _pick_dup_loc(bias, n, rng):
    if n <= 0:
        return 0
    if bias == "center":
        return n // 2
    if bias == "edge":
        return rng.choice([0, n - 1])
    return rng.randint(0, n - 1)


def _draw_from_degenerate(name, h, w, rng):
    if name == "monochrome":
        c = rng.choice(list(range(1, 10)))
        return [[c] * w for _ in range(h)]
    if name == "all_unique":
        cols = []
        last = -1
        for _ in range(h):
            choices = [c for c in range(10) if c != last]
            c = rng.choice(choices)
            cols.append(c)
            last = c
        return [[c] * w for c in cols]
    if name == "single_row":
        c = rng.choice(list(range(10)))
        return [[c] * w]
    return [[0] * w for _ in range(h)]
