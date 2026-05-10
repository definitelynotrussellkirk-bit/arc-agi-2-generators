"""Generator for puzzle 7c9b52a0.

Rule: bg = cell at (0,0). >=2 equal-sized multicolor components; rule
overlays them. Each output cell is filled by the first non-bg, non-zero
value from the matching position across all containers.

Combinatorial axes (8): grid_h/w, n_containers, box_h, box_w,
container_density, palette_size, position_bias, anchor_corner.
Degenerates: single_container, identical_containers, empty_containers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ed860c0a9107"
VERSION = "1.1.0"
TASK_ID = "ed860c0a9107"
SUMMARY = "Multiple equal-sized containers; rule overlays them."

INVARIANTS = [
    "bg = cell at (0, 0)",
    ">=2 multicolor 8-connected containers of identical bbox",
    "containers separated by >=1 cell of bg",
    "each container has some non-bg interior pattern",
]

POSITION_BIASES = ("vertical_stack", "horizontal_row", "grid",
                   "diagonal", "scattered")
DEGENERATE_TEXTURES = ("single_container", "identical_containers",
                       "empty_containers")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":           {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":           {"type": "int", "default": "rng 12..18", "valid": "12..22"},
    "n_containers":     {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "box_h":            {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "box_w":            {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "container_density":{"type": "float", "default": "rng 0.3..0.6",
                         "valid": "0.2..0.9"},
    "palette_size":     {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "position_bias":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(POSITION_BIASES)},
    "texture":          {"type": "str", "default": "alias for position_bias",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_containers = int(overrides.get("n_containers",
                                     ctx.draw_int("n_containers", 2, 3)))
    n_containers = max(2, min(4, n_containers))
    box_h = int(overrides.get("box_h",
                              ctx.draw_int("box_h", 3, 5)))
    box_w = int(overrides.get("box_w",
                              ctx.draw_int("box_w", 3, 5)))
    box_h = max(2, min(min(h - 2, 6), box_h))
    box_w = max(2, min(min(w - 2, 6), box_w))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 3, 5)))
    palette = ctx.draw_distinct_colors("palette",
                                       n=max(palette_size, 2),
                                       exclude=set())
    bg = palette[0]
    density = float(overrides.get("container_density",
                                  ctx.draw_rng("container_density")
                                  .uniform(0.3, 0.6)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, bg)
    positions = _layout_positions(bias, n_containers, h, w, box_h, box_w,
                                   rng)
    for (rr, rc) in positions:
        for dr in range(box_h):
            for dc in range(box_w):
                if rng.random() < density:
                    g[rr + dr][rc + dc] = rng.choice(palette[1:])
        # Ensure each container has at least one non-bg cell
        if not any(g[rr + dr][rc + dc] != bg
                    for dr in range(box_h) for dc in range(box_w)):
            g[rr][rc] = palette[1] if len(palette) > 1 else bg
    return g


def _layout_positions(bias, n, h, w, box_h, box_w, rng):
    positions = []
    if bias == "vertical_stack":
        for i in range(n):
            rr = 1 + i * (box_h + 2)
            rc = 1
            if rr + box_h > h - 1 or rc + box_w > w - 1:
                rr = h - box_h - 1
            positions.append((rr, rc))
    elif bias == "horizontal_row":
        for i in range(n):
            rr = 1
            rc = 1 + i * (box_w + 2)
            if rc + box_w > w - 1:
                rc = w - box_w - 1
            positions.append((rr, rc))
    elif bias == "grid":
        cols = max(1, int(n ** 0.5 + 0.5))
        for i in range(n):
            ri = i // cols; ci = i % cols
            rr = 1 + ri * (box_h + 2)
            rc = 1 + ci * (box_w + 2)
            if rr + box_h > h - 1: rr = h - box_h - 1
            if rc + box_w > w - 1: rc = w - box_w - 1
            positions.append((rr, rc))
    elif bias == "diagonal":
        for i in range(n):
            rr = 1 + i * (box_h + 1)
            rc = 1 + i * (box_w + 1)
            if rr + box_h > h - 1: rr = h - box_h - 1
            if rc + box_w > w - 1: rc = w - box_w - 1
            positions.append((rr, rc))
    else:
        for _ in range(n):
            rr = rng.randint(1, max(1, h - box_h - 1))
            rc = rng.randint(1, max(1, w - box_w - 1))
            positions.append((rr, rc))
    return positions[:n]


def _draw_from_degenerate(name, h, w, rng):
    bg = 8
    g = full_grid(h, w, bg)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 3)
    if name == "single_container":
        rr, rc = 1, 1
        for dr in range(3):
            for dc in range(3):
                if rng.random() < 0.5:
                    g[rr + dr][rc + dc] = palette[0]
        return g
    if name == "identical_containers":
        # Same pattern in 3 positions → output equals one container
        pattern = [(0, 0, palette[0]), (1, 1, palette[1])]
        for rr, rc in [(1, 1), (1, 6), (h - 4, 1)]:
            if rr + 2 > h - 1 or rc + 2 > w - 1:
                continue
            for dr, dc, color in pattern:
                g[rr + dr][rc + dc] = color
        return g
    if name == "empty_containers":
        # Containers exist but with NO interior fill (rule output = bg)
        return g
    return g
