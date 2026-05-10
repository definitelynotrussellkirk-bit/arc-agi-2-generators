"""Generator for 33997447.

Rule: each cyan(8) frame's bbox interior contains N bg-region holes.
Recolor the object to: 1→1, 2→2, 3→3, 4→7. Else keep cyan.

Combinatorial axes (8): grid_h/w, n_objects, hole_count_distribution,
frame_padding, vertical_alignment, decoy_palette_size, decoy_density,
inter_frame_spacing.
Degenerates: single_frame, all_same_holes, no_holes_solid_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import has_neighbor

GENERATOR_ID = "fa3e0c305476"
VERSION = "1.1.0"
TASK_ID = "fa3e0c305476"
SUMMARY = "Several cyan frames with varied hole counts (1..4); recolor by count."

INVARIANTS = [
    "background is 0",
    ">=2 cyan-8 frames placed left-to-right",
    "frames don't touch each other (4-conn separation)",
    "frame hole counts come from {1, 2, 3, 4}",
]

HOLE_DISTRIBUTIONS = ("ascending", "random_subset", "all_kinds")
DEGENERATE_TEXTURES = ("single_frame", "all_same_holes", "no_holes_solid_blocks")
HELPFUL_TEXTURES = HOLE_DISTRIBUTIONS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":             {"type": "int", "default": "rng 13..20", "valid": "12..24"},
    "n_objects":          {"type": "int", "default": "rng 2..4",  "valid": "1..4"},
    "hole_count_distribution": {"type": "str", "default": "rng helpful",
                                "valid": "|".join(HOLE_DISTRIBUTIONS)},
    "vertical_alignment": {"type": "str", "default": "rng top|center|bottom|random",
                           "valid": "top|center|bottom|random"},
    "inter_frame_spacing": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "decoy_palette_size": {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "decoy_density":      {"type": "float", "default": "rng 0..0.05", "valid": "0..0.2"},
    "texture":            {"type": "str", "default": "alias for hole_count_distribution",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _frame_with_n_holes(n_holes):
    if n_holes == 1:
        cells = set()
        for r in range(3):
            for c in range(3):
                if r in (0, 2) or c in (0, 2):
                    cells.add((r, c))
        return cells, 3, 3
    if n_holes == 2:
        cells = set()
        for c in range(5):
            cells.add((0, c)); cells.add((2, c))
        for r in range(3):
            cells.add((r, 0)); cells.add((r, 2)); cells.add((r, 4))
        return cells, 3, 5
    if n_holes == 3:
        cells = set()
        for c in range(7):
            cells.add((0, c)); cells.add((2, c))
        for r in range(3):
            cells.add((r, 0)); cells.add((r, 2)); cells.add((r, 4)); cells.add((r, 6))
        return cells, 3, 7
    cells = set()
    for r in range(5):
        cells.add((r, 0)); cells.add((r, 2)); cells.add((r, 4))
    for c in range(5):
        cells.add((0, c)); cells.add((2, c)); cells.add((4, c))
    return cells, 5, 5


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 5, 7, 12, 15, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 9, 12, 18, 24, 3, 4
    else:
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 6, 10, 13, 20, 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_obj = int(overrides.get("n_objects", ctx.draw_int("n_objects", n_lo, n_hi)))
    n_obj = max(1, min(4, n_obj))
    distribution = (overrides.get("texture") or overrides.get("hole_count_distribution")
                    or ctx.draw_choice("hole_count_distribution",
                                       list(HOLE_DISTRIBUTIONS)))
    valign = overrides.get("vertical_alignment",
                           ctx.draw_choice("vertical_alignment",
                                           ["top", "center", "bottom", "random"]))
    spacing = int(overrides.get("inter_frame_spacing",
                                ctx.draw_int("inter_frame_spacing", 2, 3)))
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 2)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.05)))
    plan = _draw_hole_plan(distribution, n_obj, rng)
    g = full_grid(h, w, 0)
    cur_c = 1
    used = set()
    for n_holes in plan:
        cells, fh, fw = _frame_with_n_holes(n_holes)
        if cur_c + fw + 1 >= w:
            break
        if fh > h:
            continue
        if valign == "top":
            rr = 0
        elif valign == "bottom":
            rr = h - fh
        elif valign == "center":
            rr = max(0, (h - fh) // 2)
        else:
            rr = rng.randint(0, h - fh)
        rc = cur_c
        placed = {(rr + r, rc + c) for r, c in cells}
        if any(p in used or has_neighbor(p, used, ignore=placed) for p in placed):
            cur_c += fw + spacing
            continue
        used |= placed
        for r, c in placed:
            g[r][c] = 8
        cur_c += fw + spacing
    decoy_palette = [c for c in range(1, 10) if c not in (0, 8)]
    rng.shuffle(decoy_palette)
    decoy_palette = decoy_palette[:max(0, n_decoy)]
    if decoy_palette and decoy_d > 0:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0 and rng.random() < decoy_d:
                    g[r][c] = rng.choice(decoy_palette)
    return g


def _draw_hole_plan(distribution, n_obj, rng):
    if distribution == "ascending":
        start = rng.randint(1, max(1, 4 - n_obj + 1))
        return [start + i for i in range(n_obj) if start + i <= 4]
    if distribution == "all_kinds":
        all_kinds = [1, 2, 3, 4]
        rng.shuffle(all_kinds)
        return all_kinds[:n_obj]
    return rng.sample([1, 2, 3, 4], k=min(n_obj, 4))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_frame":
        n_holes = rng.choice([1, 2, 3, 4])
        cells, fh, fw = _frame_with_n_holes(n_holes)
        rr = max(0, (h - fh) // 2)
        rc = max(0, (w - fw) // 2)
        for r, c in cells:
            if rr + r < h and rc + c < w:
                g[rr + r][rc + c] = 8
        return g
    if name == "all_same_holes":
        n_holes = rng.choice([1, 2, 3])
        cur_c = 1
        for _ in range(2):
            cells, fh, fw = _frame_with_n_holes(n_holes)
            if cur_c + fw + 1 >= w:
                break
            for r, c in cells:
                if r < h and cur_c + c < w:
                    g[r][cur_c + c] = 8
            cur_c += fw + 2
        return g
    if name == "no_holes_solid_blocks":
        for cur_c in (1, 5, 9):
            for r in range(2):
                for c in range(3):
                    if r < h and cur_c + c < w:
                        g[r][cur_c + c] = 8
        return g
    return g
