"""Generator for 7b:m48 — crop fullest frame interior.

Rule: 2-3 hollow rectangular 1-frames each contain a sparse pattern.
Output is the interior of the frame with the highest non-bg density,
cropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, equal_densities, no_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "75be7448827f"
VERSION = "1.1.0"
TASK_ID = "75be7448827f"
SUMMARY = "2-3 1-frames with different interior densities; one strictly highest."

INVARIANTS = [
    "background is 0",
    "2-3 hollow rectangular 1-frames",
    "each frame has 2-5 non-bg interior cells (different colors per frame)",
    "exactly one frame has strictly the highest interior density (cells / interior_area)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "equal_densities", "no_interior")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..16", "valid": "12..20"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "13..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "scattered_frames",
                       "valid": "scattered_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 16, 19)
        w = ctx.draw_int("grid_w", 18, 22)
    else:
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 14, 18)
    rng = ctx.draw_rng("layout")
    for _ in range(40):
        g = full_grid(h, w, 0)
        n = rng.randint(2, 3)
        sizes = []
        used_size_keys = set()
        for _ in range(n):
            for _ in range(20):
                ih = rng.randint(3, 5); iw = rng.randint(3, 5)
                if (ih, iw) not in used_size_keys:
                    used_size_keys.add((ih, iw)); sizes.append((ih, iw)); break
        if len(sizes) < n: continue
        palette = rng.sample([2, 3, 4, 6, 7, 8, 9], n)
        densities = []
        placed_frames = []
        ok = True
        for (ih, iw), color in zip(sizes, palette):
            fh, fw = ih + 2, iw + 2
            placed = False
            for _ in range(50):
                r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
                if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
                for c in range(c0, c0 + fw): g[r0][c] = 1; g[r0 + fh - 1][c] = 1
                for r in range(r0, r0 + fh): g[r][c0] = 1; g[r][c0 + fw - 1] = 1
                interior = [(r, c) for r in range(r0 + 1, r0 + fh - 1)
                            for c in range(c0 + 1, c0 + fw - 1)]
                n_cells = rng.randint(2, min(5, len(interior) - 1))
                for r, c in rng.sample(interior, n_cells):
                    g[r][c] = color
                densities.append(n_cells / (ih * iw))
                placed_frames.append((r0, c0, ih, iw, color, n_cells))
                placed = True; break
            if not placed: ok = False; break
        if not ok: continue
        max_d = max(densities)
        if densities.count(max_d) != 1: continue
        return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 16
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No 1-frames — rule has no candidates.
        g[3][3] = 4; g[7][9] = 5
        return g
    if name == "equal_densities":
        # Two frames with same density — rule's selection is ambiguous.
        for c in range(1, 5): g[1][c] = 1; g[4][c] = 1
        for r in range(1, 5): g[r][1] = 1; g[r][4] = 1
        g[2][2] = 4; g[3][3] = 4
        for c in range(7, 11): g[1][c] = 1; g[4][c] = 1
        for r in range(1, 5): g[r][7] = 1; g[r][10] = 1
        g[2][8] = 5; g[3][9] = 5
        return g
    if name == "no_interior":
        # Frames present but interiors empty — densities all 0.
        for c in range(1, 5): g[1][c] = 1; g[4][c] = 1
        for r in range(1, 5): g[r][1] = 1; g[r][4] = 1
        for c in range(7, 11): g[1][c] = 1; g[4][c] = 1
        for r in range(1, 5): g[r][7] = 1; g[r][10] = 1
        return g
    return g
