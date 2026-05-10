"""Generator for arc_additional_puzzle_bank_volume17:M119 — Count components and output an alternating bar.

Rule counts red(2) connected components and emits a 1×N row of
alternating 8/4 (8 first), where N is the count.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_red,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_red, all_red_one_blob, red_touching_distractors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ef7a83e008ab"
VERSION = "1.1.0"
TASK_ID = "ef7a83e008ab"
SUMMARY = "Several red blobs in a small grid; output is alternating 8/4 bar of length N=count."

INVARIANTS = [
    "between 1 and 6 red(2) components, separated (orthogonally non-touching)",
    "0..2 distractor blobs of other non-bg colors",
    "grid 7..12 wide and tall",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_red", "all_red_one_blob", "red_touching_distractors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "6..15"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "6..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_red":          {"type": "int", "default": "rng 1..6", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _has_neighbor(p, used, ignore=frozenset()):
    r, c = p
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r+dr, c+dc
        if (nr, nc) in ignore: continue
        if (nr, nc) in used: return True
    return False


def _grow_blob(rng, h, w, used, target_size):
    for _ in range(50):
        seed = (rng.randint(0, h-1), rng.randint(0, w-1))
        if seed in used or _has_neighbor(seed, used): continue
        cells = {seed}
        frontier = [seed]
        while frontier and len(cells) < target_size:
            r, c = frontier.pop(rng.randint(0, len(frontier)-1))
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r+dr, c+dc
                if not (0 <= nr < h and 0 <= nc < w): continue
                cand = (nr, nc)
                if cand in cells or cand in used: continue
                if _has_neighbor(cand, used, ignore=cells): continue
                cells.add(cand)
                frontier.append(cand)
                if len(cells) == target_size: break
        if len(cells) == target_size:
            return cells
    return None


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
        n_red = ctx.draw_int("n_red", 1, 3)
        n_distractor = ctx.draw_int("n_distractor", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
        n_red = ctx.draw_int("n_red", 4, 6)
        n_distractor = ctx.draw_int("n_distractor", 1, 2)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_red = ctx.draw_int("n_red", 1, 6)
        n_distractor = ctx.draw_int("n_distractor", 0, 2)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used: set[tuple[int,int]] = set()

    for _ in range(n_red):
        size = rng.randint(2, 4)
        blob = _grow_blob(rng, h, w, used, size)
        if blob is None: continue
        used |= blob
        for r, c in blob: g[r][c] = 2

    distract_colors = [3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(distract_colors)
    for i in range(n_distractor):
        if i >= len(distract_colors): break
        size = rng.randint(1, 3)
        blob = _grow_blob(rng, h, w, used, size)
        if blob is None: continue
        used |= blob
        for r, c in blob: g[r][c] = distract_colors[i]

    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_red":
        # no red blobs → count is 0, output bar has length 0 (ambiguous shape)
        for r, c, v in [(2, 2, 4), (5, 6, 5), (7, 3, 6)]:
            g[r][c] = v
        return g
    if name == "all_red_one_blob":
        # red cells touching → 1 component regardless of cell count
        for r in range(2, 7):
            for c in range(3, 7):
                g[r][c] = 2
        return g
    if name == "red_touching_distractors":
        # red cells orthogonally adjacent to distractors create ambiguous component boundaries
        for r, c in [(2, 2), (2, 3), (3, 2)]:
            g[r][c] = 2
        for r, c in [(2, 4), (3, 4)]:
            g[r][c] = 5
        for r, c in [(5, 5), (5, 6)]:
            g[r][c] = 2
        for r, c in [(5, 7), (6, 6)]:
            g[r][c] = 7
        return g
    return g
