"""Generator for arc_puzzle_bank_seventh_21_bundle:hard_46_local_symmetry_completion_by_frame_key.

Rule: 2 hollow color-5 frames; each has a small key marker above its top-left
and partial pattern inside. Rule completes symmetry inside each frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no color-5 frames → rule has no chambers);
no_keys (frames present but no key markers above → rule has no
symmetry-axis hint); no_partial (frames + keys but interiors empty
→ rule has nothing to complete).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5558f27397c3"
VERSION = "1.1.0"
TASK_ID = "5558f27397c3"

SUMMARY = "2 hollow 5-frames with key markers above and partial interior patterns."

INVARIANTS = [
    "background is 0",
    "exactly 2 hollow color-5 rectangular frames",
    "each frame has a small key color marker just above and a partial pattern inside",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_keys", "no_partial")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "grid_w":            {"type": "int", "default": "rng 18..22", "valid": "16..26"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "two_frames_with_keys_and_partials",
                          "valid": "two_frames_with_keys_and_partials"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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
        h = ctx.draw_int("grid_h", 14, 14)
        w = ctx.draw_int("grid_w", 18, 19)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 20, 22)
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
        # No color-5 frames — rule has no chambers.
        g[3][3] = 4; g[5][5] = 4
        g[3][12] = 6; g[5][14] = 6
        return g
    if name == "no_keys":
        # Frames + interior but no key markers above.
        for r0, c0 in [(2, 2), (2, 11)]:
            for c in range(c0, c0 + 8):
                g[r0][c] = 5; g[r0 + 7][c] = 5
            for r in range(r0, r0 + 8):
                g[r][c0] = 5; g[r][c0 + 7] = 5
            g[r0 + 2][c0 + 2] = 4; g[r0 + 4][c0 + 5] = 4
        return g
    if name == "no_partial":
        # Frames + keys but interiors empty — nothing to complete.
        for r0, c0 in [(2, 2), (2, 11)]:
            for c in range(c0, c0 + 8):
                g[r0][c] = 5; g[r0 + 7][c] = 5
            for r in range(r0, r0 + 8):
                g[r][c0] = 5; g[r][c0 + 7] = 5
            g[r0 - 1][c0 + 1] = 4
        return g
    return g
