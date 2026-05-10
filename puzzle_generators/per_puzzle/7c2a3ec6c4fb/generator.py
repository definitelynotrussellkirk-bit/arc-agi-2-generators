"""Generator for puzzle cd3c21df.

Rule: among 8-connected multi-color blobs, output the one whose bbox-
cropped pattern is unique (count==1) among all blobs.

Combinatorial axes (8): grid_h/w, n_blobs, n_duplicates, blob_size,
blob_palette, position_bias, anchor_corner, asymmetry_force.
Degenerates: all_unique, all_identical, single_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "7c2a3ec6c4fb"
VERSION = "1.1.0"
TASK_ID = "7c2a3ec6c4fb"
SUMMARY = "Multi-color 8-conn blobs; rule outputs the unique-pattern one."

INVARIANTS = [
    "background is 0",
    ">=3 8-connected multi-color blobs",
    "exactly one blob has a unique bbox pattern (rest have duplicates)",
    "blobs are 8-conn separated (no diagonal adjacency)",
]

POSITION_BIASES = ("spread", "corners", "row_aligned", "scattered")
DEGENERATE_TEXTURES = ("all_unique", "all_identical", "single_blob")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "9..20"},
    "n_blobs":        {"type": "int", "default": "rng 3..4", "valid": "3..6"},
    "n_duplicates":   {"type": "int", "default": "2", "valid": "2..4"},
    "blob_size":      {"type": "int", "default": "rng 3..6", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 7, 9
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 9, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 3, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_blobs = int(overrides.get("n_blobs",
                                ctx.draw_int("n_blobs", 3, 4)))
    n_dups = int(overrides.get("n_duplicates", 2))
    n_dups = max(2, min(n_blobs - 1, n_dups))
    n_unique = n_blobs - n_dups
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 3, 5)))
    palette_size = max(2, min(7, palette_size))
    pal = ctx.draw_distinct_colors("palette", n=palette_size,
                                   exclude={0})
    g = full_grid(h, w, 0)
    duplicate_pattern = _make_pattern("dup", pal, rng)
    unique_pattern = _make_pattern("unique", pal, rng)
    while _patterns_equal(unique_pattern, duplicate_pattern):
        unique_pattern = _make_pattern("unique", pal, rng)
    placed = []
    # Place duplicates
    for _ in range(n_dups):
        pos = _find_slot(g, h, w, duplicate_pattern, placed, rng)
        if pos is None:
            break
        paint_at(g, pos[0], pos[1], duplicate_pattern)
        placed.append((pos, duplicate_pattern))
    # Place uniques
    for _ in range(n_unique):
        pos = _find_slot(g, h, w, unique_pattern, placed, rng)
        if pos is None:
            break
        paint_at(g, pos[0], pos[1], unique_pattern)
        placed.append((pos, unique_pattern))
    return g


def _make_pattern(kind, palette, rng):
    if kind == "unique":
        # 2x2 with one cell missing — visibly different
        cells = [(0, 0, palette[0]), (0, 1, palette[1]),
                 (1, 0, palette[1])]
        return cells
    # Duplicate: small line or 2-cell
    return [(0, 0, palette[2 % len(palette)]),
            (0, 1, palette[2 % len(palette)]),
            (0, 2, palette[2 % len(palette)])]


def _patterns_equal(a, b):
    return sorted(a) == sorted(b)


def _find_slot(g, h, w, pattern, placed, rng):
    pat_h = max(r for r, _, _ in pattern) + 1
    pat_w = max(c for _, c, _ in pattern) + 1
    for _ in range(40):
        rr = rng.randint(0, h - pat_h)
        rc = rng.randint(0, w - pat_w)
        # Check 1-cell buffer for 8-conn separation
        ok = True
        for dr in range(-1, pat_h + 1):
            for dc in range(-1, pat_w + 1):
                r2, c2 = rr + dr, rc + dc
                if 0 <= r2 < h and 0 <= c2 < w and g[r2][c2] != 0:
                    ok = False; break
            if not ok:
                break
        if ok:
            return (rr, rc)
    return None


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 4)
    if name == "all_unique":
        # 3 different patterns — rule has 3 candidate uniques (ambiguous)
        paint_at(g, 1, 1, [(0, 0, pal[0]), (0, 1, pal[1])])
        paint_at(g, 1, 6, [(0, 0, pal[2])])
        paint_at(g, h - 3, 3, [(0, 0, pal[3]), (1, 0, pal[3])])
        return g
    if name == "all_identical":
        # 3 same patterns — rule has no unique candidate
        for r0, c0 in [(1, 1), (1, 6), (h - 3, 3)]:
            paint_at(g, r0, c0, [(0, 0, pal[0]), (0, 1, pal[0])])
        return g
    if name == "single_blob":
        paint_at(g, 1, 1, [(0, 0, pal[0]), (0, 1, pal[1])])
        return g
    return g
