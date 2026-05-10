"""Generator for 9b:hard_60 — select by hole count, scale to marker.

Rule: key cell is value 2 or 3. need = 1 if key==2 else 2. marker is
the color-8 cell. Pick color-4 component with exactly `need` holes.
Scale 2x at marker position.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_marker, no_holed_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "27e12a4be7f6"
VERSION = "1.1.0"
TASK_ID = "27e12a4be7f6"

SUMMARY = "1 key (2 or 3) + 1 marker (8) + 2-3 color-4 shapes with distinct hole counts."

INVARIANTS = [
    "background is 0",
    "exactly one isolated key cell with value 2 or 3",
    "exactly one isolated color-8 marker cell with room for 2x-scaled stamp",
    "2-3 color-4 components with strictly distinct hole counts (one with 1 hole, one with 2 holes)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_marker", "no_holed_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 16..18", "valid": "15..22"},
    "grid_w":         {"type": "int", "default": "rng 17..19", "valid": "16..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "shapes_plus_key_plus_marker",
                       "valid": "shapes_plus_key_plus_marker"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_HOLED_1 = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
]
_HOLED_2 = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
     (1, 0), (1, 2), (1, 4),
     (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
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


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 16, 17)
        w = ctx.draw_int("grid_w", 17, 18)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 18, 21)
        w = ctx.draw_int("grid_w", 19, 22)
    else:
        h = ctx.draw_int("grid_h", 16, 18)
        w = ctx.draw_int("grid_w", 17, 19)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    if not _place(g, rng, rng.choice(_HOLED_1), 4):
        raise ValueError("could not place 1-hole shape")
    if not _place(g, rng, rng.choice(_HOLED_2), 4):
        raise ValueError("could not place 2-hole shape")
    key = rng.choice([2, 3])
    for _ in range(60):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] != 0 or _too_close(g, r, c): continue
        g[r][c] = key; break
    bound = 8
    for _ in range(60):
        r = rng.randint(0, h - bound); c = rng.randint(0, w - bound)
        if g[r][c] != 0 or _too_close(g, r, c): continue
        bad = False
        for rr in range(r, r + bound):
            for cc in range(c, c + bound):
                if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                    bad = True; break
            if bad: break
        if bad: continue
        g[r][c] = 8
        return g
    raise ValueError("could not place marker with stamp clearance")


def _draw_from_degenerate(name, rng):
    h, w = 17, 18
    g = full_grid(h, w, 0)
    if name == "no_key":
        # Shapes + marker but no key — rule has no `need` count to filter by.
        for dr, dc in _HOLED_1[0]: g[1 + dr][1 + dc] = 4
        for dr, dc in _HOLED_2[0]: g[5 + dr][1 + dc] = 4
        g[10][10] = 8
        return g
    if name == "no_marker":
        # Shapes + key but no color-8 marker — rule has no anchor for the stamp.
        for dr, dc in _HOLED_1[0]: g[1 + dr][1 + dc] = 4
        for dr, dc in _HOLED_2[0]: g[5 + dr][1 + dc] = 4
        g[10][10] = 2
        return g
    if name == "no_holed_match":
        # Key=2 (need=1) but no 1-hole shape — rule selects nothing.
        for dr, dc in _HOLED_2[0]: g[1 + dr][1 + dc] = 4
        for dr, dc in _HOLED_2[0]: g[5 + dr][1 + dc] = 4
        g[12][1] = 2
        g[8][10] = 8
        return g
    return g
