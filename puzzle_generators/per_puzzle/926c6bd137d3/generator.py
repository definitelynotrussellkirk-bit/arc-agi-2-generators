"""Generator for arc_additional_puzzle_bank_volume13:E90 — yellow frame fills with marker color.

Rule: each hollow yellow frame contains exactly one nonzero non-yellow
marker; the rule fills the frame's blank interior with the marker color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_marker, multiple_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "926c6bd137d3"
VERSION = "1.1.0"
TASK_ID = "926c6bd137d3"
SUMMARY = "Hollow yellow frames fill their blank interiors with their marker color."

INVARIANTS = [
    "background is 0",
    "each yellow object is a hollow rectangular frame",
    "each frame contains exactly one nonzero non-yellow marker in its interior",
    "frames are separated and not nested",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_marker", "multiple_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "scattered_yellow_frames",
                       "valid": "scattered_yellow_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n_frames = ctx.draw_int("n_frames", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 18)
        w = ctx.draw_int("grid_w", 14, 18)
        n_frames = ctx.draw_int("n_frames", 2, 4)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
        n_frames = ctx.draw_int("n_frames", 1, 2)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    colors = [1, 2, 3, 5, 6, 7, 8, 9]
    anchors: list[tuple[int, int, int, int]] = []
    for i in range(n_frames):
        for _ in range(120):
            rh = rng.randint(4, min(6, h))
            rw = rng.randint(4, min(6, w))
            r = rng.randint(0, h - rh)
            c = rng.randint(0, w - rw)
            if any(not (r + rh + 1 < ar or ar + ah + 1 < r or c + rw + 1 < ac or ac + aw + 1 < c)
                   for ar, ac, ah, aw in anchors):
                continue
            draw_rect_outline(g, r, c, rh, rw, 4)
            mr = rng.randint(r + 1, r + rh - 2)
            mc = rng.randint(c + 1, c + rw - 2)
            g[mr][mc] = colors[i % len(colors)]
            anchors.append((r, c, rh, rw))
            break
    if not anchors:
        draw_rect_outline(g, 1, 1, 4, 4, 4)
        g[2][2] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Markers but no yellow frames — rule has no frame to fill.
        g[2][3] = 3; g[5][8] = 6
        return g
    if name == "no_marker":
        # Yellow frame present but interior is empty — rule has no
        # color to paint the interior with.
        draw_rect_outline(g, 2, 2, 5, 6, 4)
        return g
    if name == "multiple_markers":
        # Frame with two non-yellow markers in interior — rule's
        # one-marker invariant violated, ambiguous fill color.
        draw_rect_outline(g, 2, 2, 5, 6, 4)
        g[3][3] = 3; g[5][6] = 6
        return g
    return g
