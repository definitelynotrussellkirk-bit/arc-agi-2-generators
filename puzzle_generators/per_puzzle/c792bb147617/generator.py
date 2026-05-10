"""Generator for puzzle d364b489.

Rule: for each blue(1) pixel, set cardinal neighbors:
up=red(2), left=orange(7), right=magenta(6), down=cyan(8). Pixel
stays blue.

Combinatorial axes (8): grid_h/w, n_blues, position_bias,
min_separation, anchor_corner, asymmetry_force, palette_size,
include_decoy.
Degenerates: single_blue, adjacent_blues, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c792bb147617"
VERSION = "1.1.0"
TASK_ID = "c792bb147617"
SUMMARY = "Sparse blue pixels; rule paints compass neighbors with 4 colors."

INVARIANTS = [
    "background is 0",
    ">=2 blue(1) pixels",
    "each blue pixel has bg in its 4 cardinal neighbors",
    "blue pixels are >=3 cells apart (Chebyshev) so compass writes don't overlap",
]

POSITION_BIASES = ("scattered", "row_aligned", "col_aligned", "diagonal",
                   "corners", "centered")
DEGENERATE_TEXTURES = ("single_blue", "adjacent_blues", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "n_blues":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "min_separation": {"type": "int", "default": "3", "valid": "3..6"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_blues = int(overrides.get("n_blues",
                                ctx.draw_int("n_blues", 2, 4)))
    n_blues = max(2, min(6, n_blues))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    min_sep = int(overrides.get("min_separation", 3))
    min_sep = max(3, min(6, min_sep))
    g = full_grid(h, w, 0)
    placed = []
    candidates = _candidate_positions(bias, h, w, rng)
    for r, c in candidates:
        if len(placed) >= n_blues:
            break
        # Must be interior (cardinal cells in-bounds)
        if not (1 <= r <= h - 2 and 1 <= c <= w - 2):
            continue
        # Chebyshev distance from existing >= min_sep
        if any(abs(r - pr) < min_sep and abs(c - pc) < min_sep
               for pr, pc in placed):
            continue
        if (g[r - 1][c] != 0 or g[r + 1][c] != 0
                or g[r][c - 1] != 0 or g[r][c + 1] != 0):
            continue
        g[r][c] = 1
        placed.append((r, c))
    if len(placed) < 2:
        for r, c in [(1, 1), (h - 2, w - 2)]:
            if 1 <= r <= h - 2 and 1 <= c <= w - 2 and g[r][c] == 0:
                g[r][c] = 1
    return g


def _candidate_positions(bias, h, w, rng):
    if bias == "row_aligned":
        r = h // 2
        return [(r, c) for c in range(1, w - 1, 4)]
    if bias == "col_aligned":
        c = w // 2
        return [(r, c) for r in range(1, h - 1, 4)]
    if bias == "diagonal":
        return [(i, i) for i in range(1, min(h, w) - 1, 3)]
    if bias == "corners":
        return [(2, 2), (2, w - 3), (h - 3, 2), (h - 3, w - 3)]
    if bias == "centered":
        cr, cc = h // 2, w // 2
        positions = [(cr, cc)]
        for d in (3, 4, 5):
            for dr, dc in [(-d, 0), (d, 0), (0, -d), (0, d)]:
                positions.append((cr + dr, cc + dc))
        return positions
    candidates = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(candidates)
    return candidates


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_blue":
        g[h // 2][w // 2] = 1
        return g
    if name == "adjacent_blues":
        cr, cc = h // 2, w // 2
        g[cr][cc] = 1
        if cc + 1 < w:
            g[cr][cc + 1] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                if (r + c) % 4 == 0:
                    g[r][c] = 1
        return g
    return g
