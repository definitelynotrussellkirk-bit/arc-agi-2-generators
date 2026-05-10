"""Generator for 2a5f8217.

Rule: for each 1-blob, find a non-1 template blob with identical
normalized shape and recolor 1-cells to template's color.

Combinatorial axes (8): grid_h/w, n_templates, n_ones,
template_shape_kind, palette_size, position_bias,
inter_blob_margin, decoy_density.
Degenerates: no_templates, no_ones, single_template.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "51481963f4a3"
VERSION = "1.1.0"
TASK_ID = "51481963f4a3"
SUMMARY = "Templates + same-shape 1-blobs; rule recolors 1s to template color."

INVARIANTS = [
    "background is 0",
    ">=2 distinct non-1 template shapes in distinct colors",
    ">=1 1-blob with shape matching one template",
    "blobs don't touch (4-conn separation)",
]

SHAPE_KINDS = ("U_shape", "L_shape", "T_shape", "block_2x2",
               "diag", "horizontal_pair", "vertical_pair", "plus")
DEGENERATE_TEXTURES = ("no_templates", "no_ones", "single_template")
HELPFUL_TEXTURES = SHAPE_KINDS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 7..14", "valid": "6..18"},
    "grid_w":              {"type": "int", "default": "rng 9..16", "valid": "8..20"},
    "n_templates":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "n_ones":              {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "template_shape_kind": {"type": "str", "default": "rng helpful",
                            "valid": "|".join(SHAPE_KINDS)},
    "palette_size":        {"type": "int", "default": "= n_templates",
                            "valid": "1..7"},
    "position_bias":       {"type": "str", "default": "rng spread|center|edge",
                            "valid": "spread|center|edge"},
    "inter_blob_margin":   {"type": "int", "default": "1", "valid": "1..3"},
    "texture":             {"type": "str", "default": "alias for template_shape_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 9, 8, 11
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 13, 18, 15, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 14, 9, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_templates = int(overrides.get("n_templates",
                                    ctx.draw_int("n_templates", 2, 3)))
    n_ones = int(overrides.get("n_ones",
                               ctx.draw_int("n_ones", 2, 3)))
    n_templates = max(2, min(4, n_templates))
    n_ones = max(1, min(4, n_ones))
    palette = list(ctx.draw_distinct_colors("palette",
                                            n=n_templates, exclude={0, 1}))
    while len(palette) < n_templates:
        palette.append(palette[0])
    margin = int(overrides.get("inter_blob_margin", 1))
    shape_kind_pref = (overrides.get("texture") or
                       overrides.get("template_shape_kind"))
    g = full_grid(h, w, 0)
    template_shapes = []
    for i in range(n_templates):
        kind = shape_kind_pref or rng.choice(list(SHAPE_KINDS))
        cells = _shape_cells(kind, rng)
        # Make distinct: alternate kinds if same chosen
        if i > 0 and shape_kind_pref is None:
            for _ in range(5):
                kind = rng.choice(list(SHAPE_KINDS))
                cells = _shape_cells(kind, rng)
                if cells != template_shapes[i - 1]:
                    break
        if place_no_overlap(rng, g, cells, palette[i], bg=0,
                            margin=margin, max_tries=40):
            template_shapes.append(cells)
    if not template_shapes:
        return _draw_from_degenerate("single_template", h, w, rng)
    ones_placed = 0
    for _ in range(n_ones * 4):
        if ones_placed >= n_ones:
            break
        # Pick a random template's shape to match
        cells = rng.choice(template_shapes)
        if place_no_overlap(rng, g, cells, 1, bg=0,
                            margin=margin, max_tries=20):
            ones_placed += 1
    if ones_placed < 1:
        cells = template_shapes[0]
        place_no_overlap(rng, g, cells, 1, bg=0,
                         margin=margin, max_tries=10)
    return g


def _shape_cells(kind, rng):
    if kind == "U_shape":
        return normalize([(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)])
    if kind == "L_shape":
        return normalize([(0, 0), (1, 0), (1, 1)])
    if kind == "T_shape":
        return normalize([(0, 0), (0, 1), (0, 2), (1, 1)])
    if kind == "block_2x2":
        return normalize([(0, 0), (0, 1), (1, 0), (1, 1)])
    if kind == "diag":
        return normalize([(0, 0), (1, 1), (2, 2)])
    if kind == "horizontal_pair":
        return normalize([(0, 0), (0, 1)])
    if kind == "vertical_pair":
        return normalize([(0, 0), (1, 0)])
    if kind == "plus":
        return normalize([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)])
    return normalize([(0, 0), (0, 1), (1, 0)])


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = [c for c in range(2, 10)]
    rng.shuffle(palette)
    if name == "no_templates":
        cells = normalize([(0, 0), (0, 1), (1, 0)])
        place_no_overlap(rng, g, cells, 1, bg=0, margin=1, max_tries=20)
        place_no_overlap(rng, g, cells, 1, bg=0, margin=1, max_tries=20)
        return g
    if name == "no_ones":
        cells_a = normalize([(0, 0), (0, 1), (1, 0)])
        cells_b = normalize([(0, 0), (1, 0), (2, 0)])
        place_no_overlap(rng, g, cells_a, palette[0], bg=0, margin=1, max_tries=20)
        place_no_overlap(rng, g, cells_b, palette[1], bg=0, margin=1, max_tries=20)
        return g
    if name == "single_template":
        cells = normalize([(0, 0), (0, 1), (1, 0)])
        place_no_overlap(rng, g, cells, palette[0], bg=0, margin=1, max_tries=20)
        place_no_overlap(rng, g, cells, 1, bg=0, margin=1, max_tries=20)
        return g
    return g
