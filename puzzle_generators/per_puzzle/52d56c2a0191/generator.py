"""Generator for arc_additional_puzzle_bank_volume13:M87 — Output the sorted sizes of the red components.

Rule: `(rule! (list (sort (map obj-size (filter (lambda (o) (= (obj-color o) 2)) (objects g 0))) <)))`
  Find all red(2) connected components, take their sizes, sort, output as one row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_red,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_red, single_red_blob, equal_red_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "52d56c2a0191"
VERSION = "1.1.0"
TASK_ID = "52d56c2a0191"
SUMMARY = "Several red blobs of distinct sizes; output is sorted size list as a row."

INVARIANTS = [
    "between 3 and 5 red(2) connected components, all with distinct cell counts",
    "blobs don't touch each other (orthogonally)",
    "1..2 non-red distractor objects of other colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_red", "single_red_blob", "equal_red_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_red":          {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _grow_blob(rng, h, w, used, target_size):
    for _ in range(50):
        seed = (rng.randint(0, h - 1), rng.randint(0, w - 1))
        if seed in used or _has_neighbor(seed, used, h, w):
            continue
        cells = {seed}
        frontier = [seed]
        while frontier and len(cells) < target_size:
            cur_idx = rng.randint(0, len(frontier) - 1)
            r, c = frontier.pop(cur_idx)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if not (0 <= nr < h and 0 <= nc < w): continue
                cand = (nr, nc)
                if cand in cells or cand in used: continue
                if _has_neighbor(cand, used, h, w, ignore=cells): continue
                cells.add(cand)
                frontier.append(cand)
                if len(cells) == target_size:
                    break
        if len(cells) == target_size:
            return cells
    return None


def _has_neighbor(p, used, h, w, ignore=frozenset()):
    r, c = p
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if not (0 <= nr < h and 0 <= nc < w): continue
        if (nr, nc) in ignore: continue
        if (nr, nc) in used: return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
        n_red = ctx.draw_int("n_red", 3, 3)
        n_distractor = ctx.draw_int("n_distractor", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
        n_red = ctx.draw_int("n_red", 4, 5)
        n_distractor = ctx.draw_int("n_distractor", 1, 2)
    else:
        h = ctx.draw_int("grid_h", 9, 14)
        w = ctx.draw_int("grid_w", 9, 14)
        n_red = ctx.draw_int("n_red", 3, 5)
        n_distractor = ctx.draw_int("n_distractor", 1, 2)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")

    sizes = list(range(1, 7))
    rng.shuffle(sizes)
    red_sizes = sorted(sizes[:n_red])

    used: set[tuple[int, int]] = set()

    for size in red_sizes:
        blob = _grow_blob(rng, h, w, used, size)
        if blob is None:
            continue
        used |= blob
        for r, c in blob:
            g[r][c] = 2

    distract_colors = [c for c in (3, 4, 5, 6, 7, 8, 9) if True]
    rng.shuffle(distract_colors)
    for i in range(n_distractor):
        if i >= len(distract_colors): break
        color = distract_colors[i]
        size = rng.randint(1, 4)
        blob = _grow_blob(rng, h, w, used, size)
        if blob is None: continue
        used |= blob
        for r, c in blob:
            g[r][c] = color

    return g


def _draw_from_degenerate(name, rng):
    import random
    rng = random.Random(0)
    h, w = 11, 11
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    if name == "no_red":
        # no red blobs → output is empty list, rule has no signal
        for color in (3, 4, 5):
            blob = _grow_blob(rng, h, w, used, 3)
            if blob is None: continue
            used |= blob
            for r, c in blob:
                g[r][c] = color
        return g
    if name == "single_red_blob":
        # one red blob → output is single-element list, sort is trivial
        blob = _grow_blob(rng, h, w, used, 4)
        if blob:
            for r, c in blob:
                g[r][c] = 2
        return g
    if name == "equal_red_sizes":
        # multiple red blobs all same size → sort is ambiguous (any order satisfies)
        for _ in range(3):
            blob = _grow_blob(rng, h, w, used, 3)
            if blob is None: continue
            used |= blob
            for r, c in blob:
                g[r][c] = 2
        return g
    return g
