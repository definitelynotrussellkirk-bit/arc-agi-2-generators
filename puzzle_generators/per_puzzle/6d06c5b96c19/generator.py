"""Generator for ARC task 6d1d5c90.

Rule: find the row with red(2) in col 0 (call it red_row). Output is
h × (w-1): drop col 0, and cyclically rotate rows so red_row ends at
the bottom.

Combinatorial axes: grid_h/w, red_row position (top/bottom/mid),
col0_palette (markers in col 0 for non-red rows), payload_pattern.
Degenerates: red_at_bottom_already, multiple_reds_col0, no_red_in_col0.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6d06c5b96c19"
VERSION = "1.1.0"
TASK_ID = "6d06c5b96c19"
SUMMARY = "Col 0 contains one red marker; rule rotates rows so red goes to bottom and drops col 0."

INVARIANTS = [
    "exactly one row has color 2 in column 0",
    "other rows have non-red markers in col 0",
    "≥1 cell of payload (cols 1..) so output has content",
]

PAYLOAD_PATTERNS = ("random", "stripes_per_row", "blob", "checker", "border")
RED_ROW_POSITIONS = ("top", "bottom", "mid", "any")
DEGENERATE_TEXTURES = ("red_at_bottom_already", "multiple_reds_col0", "no_red_in_col0")
HELPFUL_TEXTURES = PAYLOAD_PATTERNS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "grid_w":          {"type": "int", "default": "rng 5..14", "valid": "2..18"},
    "red_row_position": {"type": "str", "default": "rng top|bottom|mid|any",
                         "valid": "|".join(RED_ROW_POSITIONS)},
    "payload_pattern": {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PAYLOAD_PATTERNS)},
    "payload_palette_size": {"type": "int", "default": "rng 3..6", "valid": "2..9"},
    "texture":         {"type": "str", "default": "alias for payload_pattern",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 5, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    pos = overrides.get("red_row_position",
                        ctx.draw_choice("red_row_position", list(RED_ROW_POSITIONS)))
    if pos == "top":
        red_row = 0
    elif pos == "bottom":
        red_row = h - 1
    elif pos == "mid":
        red_row = h // 2
    else:
        red_row = rng.randint(0, h - 1)
    n_palette = int(overrides.get("payload_palette_size",
                                  ctx.draw_int("payload_palette_size", 3, 6)))
    palette = list(ctx.draw_distinct_colors("payload", n=max(2, n_palette), exclude={2}))
    pattern = (overrides.get("texture") or overrides.get("payload_pattern")
               or ctx.draw_choice("payload_pattern", list(PAYLOAD_PATTERNS)))
    g = full_grid(h, w, palette[0])
    # Col 0: red at red_row, others are non-red palette colors.
    for r in range(h):
        g[r][0] = 2 if r == red_row else rng.choice(palette)
    # Payload (cols 1..)
    if pattern == "random":
        for r in range(h):
            for c in range(1, w):
                g[r][c] = rng.choice(palette + [2])
    elif pattern == "stripes_per_row":
        for r in range(h):
            color = palette[r % len(palette)]
            for c in range(1, w):
                g[r][c] = color
    elif pattern == "blob":
        bh = max(1, h // 2); bw = max(1, (w - 1) // 2)
        r0 = rng.randint(0, h - bh); c0 = rng.randint(1, w - bw)
        color = rng.choice(palette)
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = color
    elif pattern == "checker":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        for r in range(h):
            for c in range(1, w):
                g[r][c] = a if (r + c) % 2 == 0 else b
    elif pattern == "border":
        c0 = palette[0]
        for c in range(1, w):
            g[0][c] = c0; g[h - 1][c] = c0
        for r in range(h):
            g[r][1] = c0; g[r][w - 1] = c0
    return g


def _draw_from_degenerate(name, h, w, rng):
    palette = list(range(1, 10))
    rng.shuffle(palette)
    g = full_grid(h, w, palette[0])
    if name == "red_at_bottom_already":
        for r in range(h):
            g[r][0] = 2 if r == h - 1 else rng.choice([c for c in palette if c != 2])
        for r in range(h):
            for c in range(1, w):
                g[r][c] = rng.choice(palette)
        return g
    if name == "multiple_reds_col0":
        for r in range(h):
            g[r][0] = 2 if r in (0, h // 2) else rng.choice([c for c in palette if c != 2])
        for r in range(h):
            for c in range(1, w):
                g[r][c] = rng.choice(palette)
        return g
    if name == "no_red_in_col0":
        for r in range(h):
            g[r][0] = rng.choice([c for c in palette if c != 2])
        for r in range(h):
            for c in range(1, w):
                g[r][c] = rng.choice(palette)
        return g
    return g
