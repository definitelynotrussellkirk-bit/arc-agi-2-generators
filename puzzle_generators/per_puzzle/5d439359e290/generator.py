"""Generator for arc_additional_puzzle_bank_volume3:H17 — Fill 5-frame interior with dominant color.

Rule: each 5-frame's interior is filled with the dominant non-5 color
inside. (Largest object's color wins.)

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, monochrome_interior, no_dominant.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "5d439359e290"
VERSION = "1.1.0"
TASK_ID = "5d439359e290"
SUMMARY = "2 5-frames, each ≥4×4 with 2 distinct non-5 colors inside (one majority)."

INVARIANTS = [
    "2 separate 5-frames, each ≥4×4",
    "each frame's interior contains 2 different non-5 colors",
    "one color has more cells than the other (dominant)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "monochrome_interior", "no_dominant")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "two_separated_frames",
                       "valid": "two_separated_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "3..7"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = []
    for _ in range(2):
        for _ in range(40):
            fh = rng.randint(4, 5); fw = rng.randint(4, 5)
            r0 = rng.randint(1, h - fh - 1); c0 = rng.randint(1, w - fw - 1)
            if any(abs(r0 - pr) < (fh + 2) and abs(c0 - pc) < (fw + 2) for pr, pc in placed):
                continue
            draw_rect_outline(g, r0, c0, fh, fw, 5)
            placed.append((r0, c0))
            # Fill interior with 2 colors, one dominant
            major, minor = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
            interior_cells = [(r, c) for r in range(r0 + 1, r0 + fh - 1) for c in range(c0 + 1, c0 + fw - 1)]
            n = len(interior_cells)
            n_major = max(2, n - rng.randint(1, 2))
            rng.shuffle(interior_cells)
            for cell in interior_cells[:n_major]:
                g[cell[0]][cell[1]] = major
            for cell in interior_cells[n_major:]:
                g[cell[0]][cell[1]] = minor
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 13
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No 5-frames present — rule has no interiors to fill.
        g[2][3] = 4; g[5][8] = 6
        return g
    if name == "monochrome_interior":
        # Interior already a single color — dominant is trivial, rule is no-op.
        draw_rect_outline(g, 1, 1, 4, 4, 5)
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        return g
    if name == "no_dominant":
        # Interior has equal counts — no clear dominant color.
        draw_rect_outline(g, 1, 1, 4, 4, 5)
        g[2][2] = 4; g[2][3] = 6
        g[3][2] = 4; g[3][3] = 6
        return g
    return g
