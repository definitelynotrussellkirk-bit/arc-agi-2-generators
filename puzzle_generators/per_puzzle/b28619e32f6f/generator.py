"""Generator for 00dbd492.

Rule: closed red(2) frames enclose zero regions; rule fills each
enclosed region by area bucket (≤8 → 8, ≤24 → 4, else → 3).

Combinatorial axes (8): grid_h/w, n_frames, frame_size_kind,
frame_position_bias, palette_size, decoy_density, anchor_corner,
inter_frame_margin.
Degenerates: no_frame, full_grid_frame, single_cell_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "b28619e32f6f"
VERSION = "1.1.0"
TASK_ID = "b28619e32f6f"
SUMMARY = "Closed red frames enclose zero regions; rule fills by area bucket."

INVARIANTS = [
    "background is 0",
    ">=1 closed red(2) frame (rectangular outline)",
    "interior of each frame is connected zero region",
    "frames don't overlap",
    "exterior bg remains 0",
]

FRAME_SIZES = ("tiny", "small", "medium", "large")
DEGENERATE_TEXTURES = ("no_frame", "full_grid_frame", "single_cell_interior")
HELPFUL_TEXTURES = FRAME_SIZES

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":            {"type": "int", "default": "rng 9..16", "valid": "6..20"},
    "n_frames":          {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "frame_size_kind":   {"type": "str", "default": "rng helpful",
                          "valid": "|".join(FRAME_SIZES)},
    "frame_position_bias": {"type": "str", "default": "rng spread|center",
                            "valid": "spread|center"},
    "include_decoy_pixel": {"type": "bool", "default": "false",
                            "valid": "true|false"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "inter_frame_margin": {"type": "int", "default": "1", "valid": "1..3"},
    "texture":           {"type": "str", "default": "alias for frame_size_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 5, 8, 6, 9, 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 12, 18, 14, 20, 2, 4
    else:
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 7, 14, 9, 16, 1, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_frames = int(overrides.get("n_frames",
                                 ctx.draw_int("n_frames", n_lo, n_hi)))
    n_frames = max(1, min(4, n_frames))
    size_kind = (overrides.get("texture") or
                 overrides.get("frame_size_kind")
                 or ctx.draw_choice("frame_size_kind",
                                    list(FRAME_SIZES)))
    g = full_grid(h, w, 0)
    placed = 0
    used = []
    margin = int(overrides.get("inter_frame_margin", 1))
    for _ in range(n_frames * 5):
        if placed >= n_frames:
            break
        ih, iw = _pick_inner_size(size_kind, rng)
        outer_h = ih + 2; outer_w = iw + 2
        if outer_h + 2 >= h or outer_w + 2 >= w:
            continue
        for _try in range(20):
            r0 = rng.randint(1, h - outer_h - 1)
            c0 = rng.randint(1, w - outer_w - 1)
            if any(_overlap(r0, c0, outer_h, outer_w,
                            ur, uc, uh, uw, margin)
                   for ur, uc, uh, uw in used):
                continue
            draw_rect_outline(g, r0, c0, outer_h, outer_w, 2)
            used.append((r0, c0, outer_h, outer_w))
            placed += 1
            break
    if placed < 1:
        # fallback: place a small frame
        if h >= 4 and w >= 5:
            draw_rect_outline(g, 1, 1, 3, 4, 2)
    if bool(overrides.get("include_decoy_pixel", False)) and used:
        ur, uc, uh, uw = used[0]
        if uh >= 4 and uw >= 4:
            g[ur + 2][uc + 2] = 2
    return g


def _pick_inner_size(kind, rng):
    if kind == "tiny":
        return 2, 2
    if kind == "small":
        return rng.randint(2, 3), rng.randint(2, 3)
    if kind == "medium":
        return rng.randint(3, 4), rng.randint(3, 4)
    if kind == "large":
        return rng.randint(4, 6), rng.randint(4, 6)
    return rng.randint(2, 4), rng.randint(2, 4)


def _overlap(r1, c1, h1, w1, r2, c2, h2, w2, margin):
    return not (r1 + h1 + margin <= r2 or r2 + h2 + margin <= r1
                or c1 + w1 + margin <= c2 or c2 + w2 + margin <= c1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_frame":
        return g
    if name == "full_grid_frame":
        draw_rect_outline(g, 0, 0, h, w, 2)
        return g
    if name == "single_cell_interior":
        if h >= 4 and w >= 4:
            draw_rect_outline(g, 1, 1, 3, 3, 2)
        return g
    return g
