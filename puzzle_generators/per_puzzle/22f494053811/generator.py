"""Generator for 8b:m56 — mark each frame's center with majority color.

Rule: each rect-frame has interior with cells of various colors.
Output: replace frame's center cell with the most common interior color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_majority, empty_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "22f494053811"
VERSION = "1.1.0"
TASK_ID = "22f494053811"
SUMMARY = "1-2 5-frames each with multiple interior colored cells (majority unique)."

INVARIANTS = [
    "background is 0",
    "≥1 5-rect-frame ≥5×5 with ≥3 interior cells of one color (majority)",
    "interior also has 1-2 distractor cells of other colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_majority", "empty_interior")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "frames_with_majority_interior",
                       "valid": "frames_with_majority_interior"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(1, 2)
    for _ in range(n):
        for _ in range(40):
            fh = 5; fw = 5
            r1 = rng.randint(0, h - fh)
            c1 = rng.randint(0, w - fw)
            r2 = r1 + fh - 1; c2 = c1 + fw - 1
            if _free(g, r1, c1, r2, c2):
                for c in range(c1, c2 + 1):
                    g[r1][c] = 5; g[r2][c] = 5
                for r in range(r1, r2 + 1):
                    g[r][c1] = 5; g[r][c2] = 5
                interior = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
                pal = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
                majority, distractor = pal
                rng.shuffle(interior)
                for cell in interior[:max(3, len(interior) // 2)]:
                    g[cell[0]][cell[1]] = majority
                for cell in interior[max(3, len(interior) // 2):max(3, len(interior) // 2) + 1]:
                    g[cell[0]][cell[1]] = distractor
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 13
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Loose colored cells but no 5-frames — rule's "frame
        # interior majority" lookup has no scope.
        g[3][3] = 4; g[5][8] = 6
        return g
    if name == "no_majority":
        # Frame with interior split evenly between two colors —
        # rule's "strict majority" filter fails; center cell
        # selection ambiguous.
        for c in range(2, 7): g[1][c] = 5; g[5][c] = 5
        for r in range(1, 6): g[r][2] = 5; g[r][6] = 5
        interior = [(r, c) for r in range(2, 5) for c in range(3, 6)]
        for i, (r, c) in enumerate(interior):
            g[r][c] = 4 if i < 4 else 6
        return g
    if name == "empty_interior":
        # Frame with empty interior — rule has no cells to compute
        # majority from; center marker undefined.
        for c in range(2, 7): g[1][c] = 5; g[5][c] = 5
        for r in range(1, 6): g[r][2] = 5; g[r][6] = 5
        return g
    return g
