"""Generator for 7b:m44 — stamp rotated source at markers.

Rule: source = largest shape whose color is NOT in {1,2,3,4}. For
each cell with value v in {1,2,3,4}, paste source rotated (v-1) times
CW, recolored to v, with top-left at that cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_markers, marker_invalid_code.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e1f0030b6a1e"
VERSION = "1.1.0"
TASK_ID = "e1f0030b6a1e"

SUMMARY = "1 source shape (color 5-9) + 2-3 marker cells with values in {1,2,3,4}."

INVARIANTS = [
    "background is 0",
    "exactly one source shape in a color from {5,6,7,8,9}, isolated, asymmetric",
    "2-3 isolated marker cells with values in {1, 2, 3, 4}",
    "each marker has space for the source rotated by (v-1)*90° to fit in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_markers", "marker_invalid_code")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "source_plus_markers",
                       "valid": "source_plus_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_ASYM_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _too_close(g, r, c) -> bool:
    h, w = len(g), len(g[0])
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 14, 17)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    source_color = rng.choice([5, 6, 7, 8, 9])
    shape = rng.choice(_ASYM_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    bound = max(sh, sw)
    placed_source = False
    for _ in range(60):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = source_color
        placed_source = True; break
    if not placed_source:
        raise ValueError("could not place source shape")
    n_markers = rng.randint(2, 3)
    used_codes = rng.sample([1, 2, 3, 4], n_markers)
    placed = 0
    attempts = 0
    while placed < n_markers and attempts < 80:
        attempts += 1
        mr = rng.randint(0, h - bound); mc = rng.randint(0, w - bound)
        if g[mr][mc] != 0 or _too_close(g, mr, mc): continue
        bad = False
        for r in range(mr, mr + bound):
            for c in range(mc, mc + bound):
                if 0 <= r < h and 0 <= c < w and g[r][c] != 0:
                    bad = True; break
            if bad: break
        if bad: continue
        g[mr][mc] = used_codes[placed]
        placed += 1
    if placed < n_markers:
        raise ValueError(f"could only place {placed}/{n_markers} markers")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_source":
        # Markers but no source shape — rule has nothing to stamp.
        g[3][3] = 1; g[6][8] = 2
        return g
    if name == "no_markers":
        # Source but no markers — rule has nothing to stamp at.
        for dr, dc in _ASYM_SHAPES[0]: g[1 + dr][1 + dc] = 5
        return g
    if name == "marker_invalid_code":
        # Markers have codes outside {1..4} — rule has no defined rotation.
        for dr, dc in _ASYM_SHAPES[0]: g[1 + dr][1 + dc] = 5
        g[6][6] = 7  # 7 is not a valid marker code
        g[8][3] = 8
        return g
    return g
