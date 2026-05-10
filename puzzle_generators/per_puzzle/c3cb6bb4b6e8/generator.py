"""Generator for 4b:hard_22 — local-key rotate template inside frames.

Rule: template = color-1 component (outside any frame). For each
7-frame: find the key cell inside (color in {2,3,4,5}); transform
template by key; center-place inside the frame, painted key-color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template (no color-1 component → rule has nothing
to rotate); no_frames (template but no 7-frames → no destination);
no_keys (frames but no keys inside → no rotation count).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c3cb6bb4b6e8"
VERSION = "1.1.0"
TASK_ID = "c3cb6bb4b6e8"

SUMMARY = "1 color-1 template (outside) + 1-2 hollow 7-frames each with 1 key (color 2/3/4/5) inside."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 multi-cell template, outside any 7-frame",
    "1-2 hollow rectangular 7-frames",
    "each frame's interior holds exactly one isolated key cell with value in {2, 3, 4, 5}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_frames", "no_keys")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 12..15", "valid": "11..18"},
    "grid_w":            {"type": "int", "default": "rng 13..16", "valid": "12..18"},
    "n_frames":          {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "template_outside_frames_with_keys",
                          "valid": "template_outside_frames_with_keys"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]


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
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
        n_frames = ctx.draw_int("n_frames", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 15, 16)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 12, 15)
        w = ctx.draw_int("grid_w", 13, 16)
        n_frames = ctx.draw_int("n_frames", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_SHAPES)
    th = max(r for r, _ in template) + 1
    tw = max(c for _, c in template) + 1
    placed_t = False
    for _ in range(40):
        r0 = rng.randint(0, h - th); c0 = rng.randint(0, w - tw)
        if not _free(g, r0, c0, r0 + th - 1, c0 + tw - 1): continue
        for dr, dc in template:
            g[r0 + dr][c0 + dc] = 1
        placed_t = True; break
    if not placed_t:
        raise ValueError("could not place template")
    placed_frames = 0
    for _ in range(n_frames):
        for _ in range(60):
            fh = rng.randint(5, 6); fw = rng.randint(5, 6)
            r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            for c in range(c0, c0 + fw): g[r0][c] = 7; g[r0 + fh - 1][c] = 7
            for r in range(r0, r0 + fh): g[r][c0] = 7; g[r][c0 + fw - 1] = 7
            kr = rng.randint(r0 + 1, r0 + fh - 2)
            kc = rng.randint(c0 + 1, c0 + fw - 2)
            g[kr][kc] = rng.choice([2, 3, 4, 5])
            placed_frames += 1; break
    if placed_frames < n_frames:
        raise ValueError(f"could only place {placed_frames}/{n_frames} frames")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 14
    g = full_grid(h, w, 0)
    if name == "no_template":
        # Frames with keys but no color-1 template — rule has nothing to rotate.
        for c in range(2, 7): g[1][c] = 7; g[5][c] = 7
        for r in range(1, 6): g[r][2] = 7; g[r][6] = 7
        g[3][4] = 3
        return g
    if name == "no_frames":
        # Template but no 7-frames — no destination.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 1
        return g
    if name == "no_keys":
        # Template + frames but no key cells inside — no rotation count.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[10 + dr][2 + dc] = 1
        for c in range(2, 7): g[1][c] = 7; g[5][c] = 7
        for r in range(1, 6): g[r][2] = 7; g[r][6] = 7
        return g
    return g
