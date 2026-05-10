"""Generator for 8b:hard_50 — frame direction rays.

Rule: each 8-frame contains an emitter (color 6) and a key cell with
value in {1,2,3,4} naming a cardinal direction. The emitter casts a
ray in the key's direction; ray paints color 6 until it hits a 7-block
or the frame's wall.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame (no 8-frame → rule has no chamber);
no_emitter (frame but no color-6 emitter → rule has no source);
no_key (frame + emitter but no direction key → rule has no
direction).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7d09ccad28c8"
VERSION = "1.1.0"
TASK_ID = "7d09ccad28c8"

SUMMARY = "1-2 hollow 8-frames; each contains 1 emitter (color 6) + 1 key (1/2/3/4)."

INVARIANTS = [
    "background is 0",
    "1-2 hollow rectangular 8-frames",
    "each frame contains exactly one isolated color-6 emitter",
    "each frame contains exactly one isolated key cell with value in {1, 2, 3, 4}",
    "emitter and key are separated by ≥1 bg cell, both inside the frame interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_emitter", "no_key")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 16..19", "valid": "15..22"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "frame_with_emitter_and_key",
                          "valid": "frame_with_emitter_and_key"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


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
        w = ctx.draw_int("grid_w", 16, 17)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 18, 19)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 16, 19)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_frames = 1
    placed_frames = 0
    for _ in range(n_frames):
        for _ in range(60):
            fh = rng.randint(6, 8); fw = rng.randint(6, 8)
            if fh > h or fw > w: continue
            r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            for c in range(c0, c0 + fw): g[r0][c] = 8; g[r0 + fh - 1][c] = 8
            for r in range(r0, r0 + fh): g[r][c0] = 8; g[r][c0 + fw - 1] = 8
            er = rng.randint(r0 + 2, r0 + fh - 3)
            ec = rng.randint(c0 + 2, c0 + fw - 3)
            g[er][ec] = 6
            placed_key = False
            for _ in range(40):
                kr = rng.randint(r0 + 1, r0 + fh - 2)
                kc = rng.randint(c0 + 1, c0 + fw - 2)
                if g[kr][kc] != 0 or _too_close(g, kr, kc): continue
                g[kr][kc] = rng.choice([1, 2, 3, 4])
                placed_key = True; break
            if not placed_key: continue
            placed_frames += 1; break
    if placed_frames < n_frames:
        raise ValueError(f"could only place {placed_frames}/{n_frames} frames")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 17
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # No 8-frame — rule has no chamber.
        g[5][8] = 6; g[7][12] = 1
        return g
    if name == "no_emitter":
        # Frame + key but no color-6 emitter.
        for c in range(2, 12): g[2][c] = 8; g[9][c] = 8
        for r in range(2, 10): g[r][2] = 8; g[r][11] = 8
        g[5][7] = 1
        return g
    if name == "no_key":
        # Frame + emitter but no direction key.
        for c in range(2, 12): g[2][c] = 8; g[9][c] = 8
        for r in range(2, 10): g[r][2] = 8; g[r][11] = 8
        g[5][7] = 6
        return g
    return g
