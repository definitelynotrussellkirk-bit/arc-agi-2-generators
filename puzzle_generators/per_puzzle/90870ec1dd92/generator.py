"""Generator for puzzle e50d258f.

Rule: multicolor 8-connected rectangles. Output extracts bbox of the
rectangle with most red(2) cells.

Combinatorial axes (8): grid_h/w, n_clusters, rect_h_min, rect_h_max,
rect_w_min, rect_w_max, palette_kind, position_bias.
Degenerates: tied_red, no_red, single_cluster.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "90870ec1dd92"
VERSION = "1.1.0"
TASK_ID = "90870ec1dd92"
SUMMARY = "Multicolor clusters w/ varying red counts; rule outputs max-red cluster's bbox."

INVARIANTS = [
    "background is 0",
    ">=2 multicolor 8-connected clusters",
    "each has >=1 red(2) cell",
    "clusters have distinct red counts (winner unique)",
    "clusters separated by margin >=2",
]

POSITION_BIASES = ("scattered", "stacked", "row_aligned", "diagonal",
                   "corners")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tied_red", "no_red", "single_cluster")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..20", "valid": "12..24"},
    "grid_w":         {"type": "int", "default": "rng 14..20", "valid": "12..24"},
    "n_clusters":     {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "rect_h_min":     {"type": "int", "default": "3", "valid": "3..5"},
    "rect_h_max":     {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "rect_w_min":     {"type": "int", "default": "3", "valid": "3..5"},
    "rect_w_max":     {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 12, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 24
    else:
        h_lo, h_hi = 14, 20
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_clusters = int(overrides.get("n_clusters",
                                   ctx.draw_int("n_clusters", 2, 3)))
    n_clusters = max(2, min(4, n_clusters))
    rh_min = int(overrides.get("rect_h_min", 3))
    rh_max = int(overrides.get("rect_h_max",
                               ctx.draw_int("rect_h_max", 4, 5)))
    rw_min = int(overrides.get("rect_w_min", 3))
    rw_max = int(overrides.get("rect_w_max",
                               ctx.draw_int("rect_w_max", 4, 5)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_clusters, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    red_counts = sorted(rng.sample(range(1, 7), n_clusters))
    g = full_grid(h, w, 0)
    placed = 0
    for i, n_red in enumerate(red_counts):
        rh = rng.randint(rh_min, rh_max)
        rw = rng.randint(rw_min, rw_max)
        cells = normalize(rect_cells(rh, rw))
        pos = place_no_overlap(rng, g, cells, palette[i], bg=0,
                               margin=2, max_tries=30)
        if pos is None:
            continue
        rr, rc = pos
        local_cells = [(rr + dr, rc + dc)
                       for dr in range(rh) for dc in range(rw)]
        rng.shuffle(local_cells)
        for r, c in local_cells[:n_red]:
            g[r][c] = 2
        placed += 1
    if placed < 2:
        return _draw_from_degenerate("single_cluster", h, w, rng)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 3, 4]
    else:
        pool = [1, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "tied_red":
        for r0, c0 in [(2, 2), (2, w - 6)]:
            for dr in range(3):
                for dc in range(3):
                    g[r0 + dr][c0 + dc] = 5
            g[r0][c0] = 2
            g[r0][c0 + 1] = 2
        return g
    if name == "no_red":
        for r0, c0 in [(2, 2), (2, w - 6)]:
            for dr in range(3):
                for dc in range(3):
                    g[r0 + dr][c0 + dc] = 5
        return g
    if name == "single_cluster":
        for dr in range(3):
            for dc in range(3):
                g[2 + dr][2 + dc] = 5
        g[2][2] = 2
        return g
    return g
