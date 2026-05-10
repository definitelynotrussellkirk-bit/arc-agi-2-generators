"""Generator for puzzle fb791726.

Rule: output is 2h × 2w. For separator rows in the input (empty rows
that have at least one non-empty row above), paint full row of 3s in
the tiled output. Other cells: g[tr][tc] when (br == bc) (i.e. on the
top-left/bottom-right diagonal of the 2x2 tile), else 0.

Combinatorial axes (8): grid_h/w, palette_size, base_color,
content_density, n_separators, separator_position, anchor_corner,
asymmetry_force.
Degenerates: no_separator, all_separators, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5d6fcce80b6a"
VERSION = "1.1.0"
TASK_ID = "5d6fcce80b6a"
SUMMARY = "Small grid with separator empty rows; rule tiles 2x2 + paints 3-rows."

INVARIANTS = [
    "h, w in [3, 6]",
    ">=1 colored row above >=1 empty row (creates separator)",
    "color in palette excluding 0 and 3",
    "the LAST row may be colored or empty (rule treats max-colored-row as anchor)",
]

CONTENT_PATTERNS = ("alternating", "dense", "sparse", "diagonal",
                    "stripes", "edges")
DEGENERATE_TEXTURES = ("no_separator", "all_separators", "monochrome")
HELPFUL_TEXTURES = CONTENT_PATTERNS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "grid_w":           {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "palette_size":     {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "base_color":       {"type": "color", "default": "rng (≠0,3)",
                         "valid": "1..9 (≠3)"},
    "content_pattern":  {"type": "str", "default": "rng helpful",
                         "valid": "|".join(CONTENT_PATTERNS)},
    "n_separators":     {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "asymmetry_force":  {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for content_pattern",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 4
    elif difficulty == "hard":
        h_lo, h_hi = 5, 7
    else:
        h_lo, h_hi = 3, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    h = max(3, h); w = max(3, w)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 1, 2)))
    palette_size = max(1, min(4, palette_size))
    palette_pool = [v for v in [1, 2, 4, 5, 6, 7, 8, 9] if v != 3]
    rng.shuffle(palette_pool)
    palette = palette_pool[:palette_size]
    pattern = (overrides.get("texture") or
               overrides.get("content_pattern")
               or ctx.draw_choice("content_pattern",
                                  list(CONTENT_PATTERNS)))
    n_sep = int(overrides.get("n_separators",
                              ctx.draw_int("n_separators", 1, 2)))
    n_sep = max(1, min(min(h - 2, 3), n_sep))
    g = full_grid(h, w, 0)
    # Place content in row 0 (always colored) and other non-separator rows
    sep_rows = set(rng.sample(range(1, h - 1), n_sep)) if h >= 3 else set()
    for r in range(h):
        if r in sep_rows:
            continue
        _fill_row(g, r, w, pattern, palette, rng)
    # Ensure row 0 has at least one cell
    if all(v == 0 for v in g[0]):
        g[0][rng.randint(0, w - 1)] = palette[0]
    return g


def _fill_row(g, r, w, pattern, palette, rng):
    if pattern == "alternating":
        for c in range(w):
            if c % 2 == 0:
                g[r][c] = rng.choice(palette)
    elif pattern == "dense":
        for c in range(w):
            if rng.random() < 0.7:
                g[r][c] = rng.choice(palette)
    elif pattern == "sparse":
        for c in range(w):
            if rng.random() < 0.35:
                g[r][c] = rng.choice(palette)
    elif pattern == "diagonal":
        c = r % w
        g[r][c] = palette[0]
    elif pattern == "stripes":
        if r % 2 == 0:
            for c in range(w):
                g[r][c] = palette[0]
        else:
            for c in range(0, w, 2):
                g[r][c] = palette[0]
    elif pattern == "edges":
        g[r][0] = palette[0]
        if w > 1:
            g[r][w - 1] = palette[0]
    else:
        for c in range(w):
            if rng.random() < 0.5:
                g[r][c] = rng.choice(palette)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 4, 5, 6, 7, 8, 9])
    if name == "no_separator":
        # All rows colored — no separator → no 3-row in output
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.5:
                    g[r][c] = color
            if all(v == 0 for v in g[r]):
                g[r][0] = color
        return g
    if name == "all_separators":
        # Only first row colored; rest empty; rule places many 3-rows
        for c in range(w):
            if rng.random() < 0.5:
                g[0][c] = color
        if all(v == 0 for v in g[0]):
            g[0][0] = color
        return g
    if name == "monochrome":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    return g
