"""Generator for puzzle a934301b.

Rule: multicolor 8-connected objects. Remove (recolor to 0) any object
containing >1 cyan(8) cell; keep objects with <=1 cyan.

Combinatorial axes (8): grid_h/w, n_bad_objects, n_good_objects,
object_size_range, cyan_count_per_bad, position_bias,
inter_object_margin, palette_size.
Degenerates: all_bad, all_good, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "5d630040eb61"
VERSION = "1.1.0"
TASK_ID = "5d630040eb61"
SUMMARY = "Multicolor objects; rule removes those with >1 cyan(8) cell."

INVARIANTS = [
    "background is 0",
    ">=1 multicolor object with >=2 cyan(8) cells (will be removed)",
    ">=1 multicolor object with <=1 cyan cell (will be kept)",
    "objects 8-conn, non-overlapping with margin >= 2",
]

DEGENERATE_TEXTURES = ("all_bad", "all_good", "single_object")
HELPFUL_TEXTURES = ("balanced", "bad_heavy", "good_heavy", "many_objects")

AXES = {
    "grid_h":              {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "grid_w":              {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "n_bad_objects":       {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "n_good_objects":      {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "object_size_range":   {"type": "str", "default": "rng small|medium|large",
                            "valid": "small|medium|large"},
    "cyan_count_per_bad":  {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "inter_object_margin": {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":       {"type": "str", "default": "rng spread|center|edge",
                            "valid": "spread|center|edge"},
    "texture":             {"type": "str", "default": "rng helpful",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 14, 20
    else:
        h_lo, h_hi = 10, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    if texture == "bad_heavy":
        n_bad, n_good = 3, 1
    elif texture == "good_heavy":
        n_bad, n_good = 1, 3
    elif texture == "many_objects":
        n_bad, n_good = 2, 2
    else:
        n_bad = int(overrides.get("n_bad_objects",
                                  ctx.draw_int("n_bad_objects", 1, 2)))
        n_good = int(overrides.get("n_good_objects",
                                   ctx.draw_int("n_good_objects", 1, 2)))
    n_bad = max(1, min(3, n_bad))
    n_good = max(1, min(3, n_good))
    palette = list(ctx.draw_distinct_colors("palette",
                                            n=max(2, n_bad + n_good),
                                            exclude={0, 8}))
    while len(palette) < n_bad + n_good:
        palette.append(palette[0])
    size_range = overrides.get("object_size_range",
                               ctx.draw_choice("object_size_range",
                                               ["small", "medium", "large"]))
    cyan_count = int(overrides.get("cyan_count_per_bad",
                                   ctx.draw_int("cyan_count_per_bad", 2, 4)))
    margin = int(overrides.get("inter_object_margin", 2))
    s_lo, s_hi = {"small": (3, 3), "medium": (3, 4), "large": (4, 5)}[size_range]
    g = full_grid(h, w, 0)
    placed_bad = 0
    for i in range(n_bad):
        for _ in range(20):
            rh, rw = rng.randint(s_lo, s_hi), rng.randint(s_lo, s_hi)
            cells = normalize(rect_cells(rh, rw))
            pos = place_no_overlap(rng, g, cells, palette[i], bg=0,
                                   margin=margin, max_tries=20)
            if pos is not None:
                rr, rc = pos
                local_cells = [(rr + dr, rc + dc)
                               for dr in range(rh) for dc in range(rw)]
                n_cyan = min(cyan_count, len(local_cells) - 1)
                for r, c in rng.sample(local_cells, n_cyan):
                    g[r][c] = 8
                placed_bad += 1
                break
    placed_good = 0
    for i in range(n_good):
        color = palette[n_bad + i] if (n_bad + i) < len(palette) else palette[-1]
        for _ in range(20):
            rh, rw = rng.randint(s_lo, s_hi), rng.randint(s_lo, s_hi)
            cells = normalize(rect_cells(rh, rw))
            pos = place_no_overlap(rng, g, cells, color, bg=0,
                                   margin=margin, max_tries=20)
            if pos is not None:
                rr, rc = pos
                if rng.random() < 0.5:
                    g[rr][rc] = 8
                placed_good += 1
                break
    if placed_bad < 1 or placed_good < 1:
        return _draw_from_degenerate("single_object", h, w, rng)
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = [c for c in range(1, 10) if c != 8]
    rng.shuffle(palette)
    if name == "all_bad":
        # bad object only
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = palette[0]
        for r in range(2, 5):
            for c in range(2, 5):
                if rng.random() < 0.5:
                    g[r][c] = 8
        return g
    if name == "all_good":
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = palette[0]
        return g
    if name == "single_object":
        for r in range(3, 6):
            for c in range(3, 6):
                g[r][c] = palette[0]
        g[3][3] = 8
        return g
    return g
