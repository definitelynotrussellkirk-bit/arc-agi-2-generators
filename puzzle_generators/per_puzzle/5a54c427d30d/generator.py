"""Generator for puzzle 54db823b.

Rule: among multi-color 8-connected components, erase the one with the
FEWEST 9-cells (replace with 0).

Combinatorial axes (8): grid_h/w, n_objs, object_shape_kind,
nine_count_distribution, palette_size, object_size_range,
inter_object_margin, decoy_density.
Degenerates: single_object, ties_for_min, no_nines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "5a54c427d30d"
VERSION = "1.1.0"
TASK_ID = "5a54c427d30d"
SUMMARY = "Multi-color components with varying 9-counts; rule erases the one with fewest 9s."

INVARIANTS = [
    "background is 0",
    ">=2 multi-color 8-connected components (so the choice is real)",
    "each component has >=1 cell of color 9",
    "components have a UNIQUE minimum 9-cell count (no tie at min)",
    "components separated by margin >= 1",
]

OBJECT_SHAPE_KINDS = ("rect", "block_3x3", "block_4x4", "mixed")
NINE_DISTRIBUTIONS = ("ascending", "wide_spread", "tight_spread")
DEGENERATE_TEXTURES = ("single_object", "ties_for_min", "no_nines")
HELPFUL_TEXTURES = OBJECT_SHAPE_KINDS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":              {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "n_objs":              {"type": "int", "default": "rng 2..4",   "valid": "2..5"},
    "object_shape_kind":   {"type": "str", "default": "rng helpful",
                            "valid": "|".join(OBJECT_SHAPE_KINDS)},
    "nine_count_distribution": {"type": "str", "default": "rng helpful",
                                "valid": "|".join(NINE_DISTRIBUTIONS)},
    "palette_size":        {"type": "int", "default": "= n_objs",   "valid": "2..7"},
    "object_size_range":   {"type": "str", "default": "rng small|medium|large",
                            "valid": "small|medium|large"},
    "inter_object_margin": {"type": "int", "default": "2",          "valid": "1..3"},
    "texture":             {"type": "str", "default": "alias for object_shape_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 12, 14, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 18, 22, 3, 4
    else:
        h_lo, h_hi, n_lo, n_hi = 14, 18, 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_objs = int(overrides.get("n_objs", ctx.draw_int("n_objs", n_lo, n_hi)))
    n_objs = max(2, min(4, n_objs))
    palette = list(ctx.draw_distinct_colors("palette", n=n_objs, exclude={0, 9}))
    shape_kind = (overrides.get("texture") or overrides.get("object_shape_kind")
                  or ctx.draw_choice("object_shape_kind", list(OBJECT_SHAPE_KINDS)))
    nine_dist = (overrides.get("nine_count_distribution")
                 or ctx.draw_choice("nine_count_distribution", list(NINE_DISTRIBUTIONS)))
    size_range = overrides.get("object_size_range",
                               ctx.draw_choice("object_size_range",
                                               ["small", "medium", "large"]))
    margin = int(overrides.get("inter_object_margin", 2))
    margin = max(1, min(3, margin))
    s_lo, s_hi = {"small": (3, 3), "medium": (3, 4), "large": (4, 5)}[size_range]
    nine_counts = _draw_nine_counts(nine_dist, n_objs, rng)
    g = full_grid(h, w, 0)
    placed = 0
    for i, n9 in enumerate(nine_counts):
        rh, rw = _draw_shape(shape_kind, s_lo, s_hi, rng)
        cells = normalize(rect_cells(rh, rw))
        pos = place_no_overlap(rng, g, cells, palette[i], bg=0,
                               margin=margin, max_tries=60)
        if pos is None:
            continue
        rr, rc = pos
        local_cells = [(rr + dr, rc + dc) for dr in range(rh) for dc in range(rw)]
        rng.shuffle(local_cells)
        for r, c in local_cells[:min(n9, len(local_cells))]:
            g[r][c] = 9
        placed += 1
    if placed < 2:
        return [[0, 9], [9, 0]]
    return g


def _draw_shape(kind, s_lo, s_hi, rng):
    if kind == "block_3x3":
        return 3, 3
    if kind == "block_4x4":
        return 4, 4
    if kind == "rect":
        return rng.randint(s_lo, s_hi), rng.randint(s_lo, s_hi)
    return rng.randint(s_lo, s_hi), rng.randint(s_lo, s_hi)


def _draw_nine_counts(dist, n_objs, rng):
    if dist == "ascending":
        start = rng.randint(1, 3)
        return [start + i for i in range(n_objs)]
    if dist == "tight_spread":
        base = rng.randint(2, 4)
        return sorted(rng.sample(range(base, base + n_objs + 2), n_objs))
    # wide_spread
    return sorted(rng.sample(range(1, 1 + n_objs * 3), n_objs))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_object":
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        for r in range(3, 6):
            for c in range(3, 6):
                g[r][c] = color
        g[4][4] = 9
        return g
    if name == "ties_for_min":
        color1 = rng.choice([1, 2, 3, 4])
        color2 = rng.choice([5, 6, 7, 8])
        for r in range(3, 6):
            for c in range(3, 6):
                g[r][c] = color1
        g[3][3] = 9; g[3][5] = 9
        for r in range(8, 11):
            for c in range(8, 11):
                g[r][c] = color2
        g[8][8] = 9; g[8][10] = 9
        return g
    if name == "no_nines":
        color1, color2 = rng.choice([1, 2, 3]), rng.choice([4, 5, 6])
        for r in range(3, 6):
            for c in range(3, 6):
                g[r][c] = color1
        for r in range(8, 11):
            for c in range(8, 11):
                g[r][c] = color2
        return g
    return g
