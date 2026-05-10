"""Generator for ARC task 1a6449f1.

Rule: find the largest rectangular frame; output is its strict interior
(excluding frame border).

Combinatorial axes: grid_h/w, frame_color, frame_h/w, interior_palette,
interior_pattern, decoy_outside_frame.
Degenerates: empty_interior (all bg), interior_one_color, multiple_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "aaabf5b57a80"
VERSION = "1.1.0"
TASK_ID = "aaabf5b57a80"
SUMMARY = "A large rectangular frame surrounds interior content; rule extracts the interior."

INVARIANTS = [
    "≥1 dominant rectangular frame",
    "frame has ≥2 × 2 interior",
    "interior cells contain varied colors so output isn't all-bg",
]

INTERIOR_PATTERNS = ("random", "blob", "stripes", "checker", "diagonal", "border")
DEGENERATE_TEXTURES = ("empty_interior", "interior_one_color", "multiple_frames")
HELPFUL_TEXTURES = INTERIOR_PATTERNS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 12..22", "valid": "8..30"},
    "grid_w":            {"type": "int", "default": "rng 12..22", "valid": "8..30"},
    "frame_color":       {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "interior_palette_size": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "interior_pattern":  {"type": "str", "default": "rng helpful",
                          "valid": "|".join(INTERIOR_PATTERNS)},
    "interior_density":  {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "texture":           {"type": "str", "default": "alias for interior_pattern",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 12, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 22
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("interior")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)
    frame = int(overrides.get("frame_color", ctx.draw_color("frame_color", exclude={0})))
    n_palette = int(overrides.get("interior_palette_size",
                                  ctx.draw_int("interior_palette_size", 2, 4)))
    interior_palette = list(ctx.draw_distinct_colors(
        "interior_palette", n=max(1, n_palette), exclude={0, frame}))
    pattern = (overrides.get("texture") or overrides.get("interior_pattern")
               or ctx.draw_choice("interior_pattern", list(INTERIOR_PATTERNS)))
    density = float(overrides.get("interior_density",
                                  ctx.draw_rng("interior_density").uniform(0.3, 0.6)))
    g = full_grid(h, w, 0)
    r0 = rng.randint(1, 3); c0 = rng.randint(1, 3)
    rh = rng.randint(6, max(7, h - r0 - 2))
    rw = rng.randint(6, max(7, w - c0 - 2))
    draw_rect_outline(g, r0, c0, rh, rw, frame)
    _fill_interior(g, r0 + 1, c0 + 1, rh - 2, rw - 2, pattern,
                   density, interior_palette, rng)
    return g


def _fill_interior(g, rr, rc, sh, sw, pattern, density, palette, rng):
    if pattern == "random":
        for r in range(rr, rr + sh):
            for c in range(rc, rc + sw):
                if rng.random() < density:
                    g[r][c] = rng.choice(palette)
    elif pattern == "blob":
        bh = max(1, int(sh * density)); bw = max(1, int(sw * density))
        r0 = rng.randint(rr, rr + sh - bh)
        c0 = rng.randint(rc, rc + sw - bw)
        color = rng.choice(palette)
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = color
    elif pattern == "stripes":
        for r in range(rr, rr + sh):
            if (r - rr) % 2 == 0:
                color = rng.choice(palette)
                for c in range(rc, rc + sw):
                    g[r][c] = color
    elif pattern == "checker":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        for r in range(rr, rr + sh):
            for c in range(rc, rc + sw):
                g[r][c] = a if (r + c) % 2 == 0 else b
    elif pattern == "diagonal":
        for k in range(min(sh, sw)):
            g[rr + k][rc + k] = palette[k % len(palette)]
    elif pattern == "border":
        c0 = palette[0]
        for c in range(rc, rc + sw):
            g[rr][c] = c0; g[rr + sh - 1][c] = c0
        for r in range(rr, rr + sh):
            g[r][rc] = c0; g[r][rc + sw - 1] = c0


def _draw_from_degenerate(name, h, w, ctx, rng):
    frame = ctx.draw_color("frame_color", exclude={0})
    palette = list(ctx.draw_distinct_colors("interior_palette", n=2, exclude={0, frame}))
    g = full_grid(h, w, 0)
    if name == "empty_interior":
        rh, rw = h - 4, w - 4
        draw_rect_outline(g, 2, 2, rh, rw, frame)
        return g
    if name == "interior_one_color":
        rh, rw = h - 4, w - 4
        draw_rect_outline(g, 2, 2, rh, rw, frame)
        for r in range(3, 3 + rh - 2):
            for c in range(3, 3 + rw - 2):
                if rng.random() < 0.5:
                    g[r][c] = palette[0]
        return g
    if name == "multiple_frames":
        # Two frames; rule picks the largest.
        draw_rect_outline(g, 1, 1, h // 2, w // 2, frame)
        draw_rect_outline(g, 2, w // 2 + 1, h - 4, w - w // 2 - 3, frame)
        return g
    return g
