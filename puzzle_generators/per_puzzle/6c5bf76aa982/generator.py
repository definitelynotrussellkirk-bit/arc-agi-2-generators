"""Generator for `arc_additional_puzzle_bank_volume14:E96` — orange(7)
connected components touching exactly ONE grid border get recolored
(rule body uses touch_count == 1 specifically).

Concept membership: 2 puzzles share this rule.

Note: same behavior as `arc_additional_puzzle_bank_volume21:E144`
(which is already covered) but a different syntactic shape, so a
different concept_hash.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_one_side (no orange touches exactly 1 border → rule
has no cells to recolor; output = input), no_interior (every orange
touches at least 1 border → rule recolors them all gray; no kept-orange
contrast), no_orange (grid is all bg → rule's selector finds nothing).

Invariants:
  - background is 0
  - >=1 orange(7) component touching exactly 1 border
  - >=1 orange component strictly interior
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "6c5bf76aa982"
VERSION = "1.1.0"
TASK_ID = "6c5bf76aa982"
SUMMARY = "Orange components, one touching exactly one border (rule recolors those)."

INVARIANTS = [
    "background is 0",
    ">=1 orange(7) component touching exactly 1 border",
    ">=1 orange component strictly interior",
    "components 4-connected, non-overlapping with margin >= 1",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_one_side", "no_interior", "no_orange")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":            {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 1..1", "valid": "1..1"},
    "position_bias":     {"type": "str", "default": "border_and_interior_orange",
                          "valid": "border_and_interior_orange"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..1", "valid": "1..1"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 17, 18)
        w = ctx.draw_int("grid_w", 17, 18)
    else:
        h = ctx.draw_int("grid_h", 14, 18)
        w = ctx.draw_int("grid_w", 14, 18)
    rng = ctx.draw_rng("placement")

    g = full_grid(h, w, 0)
    placed_one = 0
    placed_boxes: list[tuple[int, int, int, int]] = []
    for _ in range(8):
        if placed_one >= 2: break
        rh = rng.randint(2, 4); rw = rng.randint(2, 4)
        side = rng.choice(["top", "bottom", "left", "right"])
        if side == "top":     rr, rc = 0, rng.randint(2, w - rw - 2)
        elif side == "bottom":rr, rc = h - rh, rng.randint(2, w - rw - 2)
        elif side == "left":  rr, rc = rng.randint(2, h - rh - 2), 0
        else:                 rr, rc = rng.randint(2, h - rh - 2), w - rw
        ok = all(not (rr - 1 <= or2 and rr + rh >= or1
                       and rc - 1 <= oc2 and rc + rw >= oc1)
                  for (or1, oc1, or2, oc2) in placed_boxes)
        if not ok: continue
        for dr in range(rh):
            for dc in range(rw):
                g[rr + dr][rc + dc] = 7
        placed_boxes.append((rr, rc, rr + rh - 1, rc + rw - 1))
        placed_one += 1

    placed_int = 0
    for _ in range(8):
        if placed_int >= 2: break
        rh = rng.randint(2, 3); rw = rng.randint(2, 3)
        cells = normalize(rect_cells(rh, rw))
        if place_no_overlap(rng, g, cells, 7, bg=0, margin=1, max_tries=30):
            placed_int += 1

    if placed_one < 1 or placed_int < 1:
        return [[0]]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "no_one_side":
        # All components are interior — rule has no 1-side cells to
        # recolor; output equals input.
        for r in range(3, 6):
            for c in range(3, 6): g[r][c] = 7
        for r in range(8, 10):
            for c in range(9, 12): g[r][c] = 7
        return g
    if name == "no_interior":
        # Every orange touches a border — rule recolors them all gray;
        # no kept-orange contrast.
        for r in range(0, 3):
            for c in range(3, 6): g[r][c] = 7
        for r in range(13, 16):
            for c in range(8, 11): g[r][c] = 7
        return g
    if name == "no_orange":
        # No orange anywhere — rule's selector finds nothing.
        return g
    return g
