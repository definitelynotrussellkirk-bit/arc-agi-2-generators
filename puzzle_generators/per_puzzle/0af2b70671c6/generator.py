"""Generator for arc_puzzle_bank_sixth_21_bundle:hard_39_local_object_gravity_in_frames.

Rule: 2 hollow color-5 frames; each has a small key marker above its top-left
and partial pattern inside. Rule completes symmetry inside each frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_keys, no_interior_pattern.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0af2b70671c6"
VERSION = "1.1.0"
TASK_ID = "0af2b70671c6"

SUMMARY = "2 hollow 5-frames with key markers above and partial interior patterns."

INVARIANTS = [
    "background is 0",
    "exactly 2 hollow color-5 rectangular frames",
    "each frame has a small key color marker just above and a partial pattern inside",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_keys", "no_interior_pattern")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "grid_w":         {"type": "int", "default": "rng 18..22", "valid": "16..26"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "two_frames_keys_above",
                       "valid": "two_frames_keys_above"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "3..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 18, 20)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 16, 18)
        w = ctx.draw_int("grid_w", 22, 25)
    else:
        h = ctx.draw_int("grid_h", 14, 16)
        w = ctx.draw_int("grid_w", 18, 22)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        positions = [(2, 2), (2, w // 2 + 1)]
        placed = 0
        for r0, c0 in positions:
            fh, fw = 8, 8
            if r0 + fh > h or c0 + fw > w: continue
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            for c in range(c0, c0 + fw):
                g[r0][c] = 5
                g[r0 + fh - 1][c] = 5
            for r in range(r0, r0 + fh):
                g[r][c0] = 5
                g[r][c0 + fw - 1] = 5
            if r0 - 1 >= 0:
                g[r0 - 1][c0 + 1] = rng.choice([2, 3, 4, 6, 7, 8, 9])
            inner_color = rng.choice([2, 3, 4, 6, 7, 8, 9])
            n_cells = rng.randint(2, 4)
            for _ in range(n_cells):
                for _t in range(20):
                    ir = rng.randint(r0 + 1, r0 + fh - 2)
                    ic = rng.randint(c0 + 1, c0 + fw - 2)
                    if g[ir][ic] == 0:
                        g[ir][ic] = inner_color
                        break
            placed += 1
        if placed == 2:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 15, 20
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No frames — rule has no chambers to fill.
        g[5][5] = 4; g[5][6] = 4
        return g
    if name == "no_keys":
        # Frames present but no key markers above — rule has no priority signal.
        for r0, c0 in [(2, 2), (2, w // 2 + 1)]:
            for c in range(c0, c0 + 8):
                g[r0][c] = 5; g[r0 + 7][c] = 5
            for r in range(r0, r0 + 8):
                g[r][c0] = 5; g[r][c0 + 7] = 5
            g[r0 + 3][c0 + 3] = 4
        return g
    if name == "no_interior_pattern":
        # Frames + keys but empty interiors — rule has no pattern to complete.
        for r0, c0 in [(2, 2), (2, w // 2 + 1)]:
            for c in range(c0, c0 + 8):
                g[r0][c] = 5; g[r0 + 7][c] = 5
            for r in range(r0, r0 + 8):
                g[r][c0] = 5; g[r][c0 + 7] = 5
            if r0 - 1 >= 0:
                g[r0 - 1][c0 + 1] = 4
        return g
    return g
