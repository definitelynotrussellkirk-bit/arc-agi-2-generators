"""Generator for puzzle 834ec97d.

Rule: bg + 1 seed cell. Rule scans for first non-zero cell. Output:
- (cr+1, cc): seed value
- cells where r ≤ cr and c % 2 == (cc % 2): paint 4
- else: 0

Combinatorial axes (8): grid_h/w, fg_color, seed_position,
position_bias, palette_size, decoy_density, parity_force,
edge_avoidance.
Degenerates: no_seed, multiple_seeds, seed_at_bottom_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "033db13a9d37"
VERSION = "1.1.0"
TASK_ID = "033db13a9d37"
SUMMARY = "1 seed cell on bg; rule renders parity-keyed pattern from seed."

INVARIANTS = [
    "background is 0 (rule's bg)",
    "exactly 1 non-bg seed cell",
    "seed at row r where r <= h-2 (so r+1 is in-bounds)",
    "no color 4 in input (rule writes 4 for output)",
]

POSITION_BIAS = ("center", "spread", "edge", "corners")
DEGENERATE_TEXTURES = ("no_seed", "multiple_seeds", "seed_at_bottom_row")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "grid_w":          {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "fg_color":        {"type": "color", "default": "rng (≠0,4)",
                        "valid": "1..9 (≠4)"},
    "seed_row":        {"type": "int", "default": "rng 0..h-2",
                        "valid": "0..h-2"},
    "seed_col":        {"type": "int", "default": "rng 0..w-1",
                        "valid": "0..w-1"},
    "position_bias":   {"type": "str", "default": "rng helpful",
                        "valid": "|".join(POSITION_BIAS)},
    "edge_avoidance":  {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "anchor_corner":   {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "texture":         {"type": "str", "default": "alias for position_bias",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 6
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 5, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fgc = int(overrides.get("fg_color",
                            ctx.draw_color("fg_color", exclude={0, 4})))
    pos_bias = (overrides.get("texture") or
                overrides.get("position_bias")
                or ctx.draw_choice("position_bias",
                                   list(POSITION_BIAS)))
    edge_avoid = bool(overrides.get("edge_avoidance", False))
    inset = 1 if edge_avoid else 0
    rmin = inset
    rmax = h - 2 - inset
    cmin = inset
    cmax = w - 1 - inset
    if rmax < rmin: rmin, rmax = 0, h - 2
    if cmax < cmin: cmin, cmax = 0, w - 1
    if pos_bias == "center":
        loci = (rmin + rmax) // 2
        locj = (cmin + cmax) // 2
    elif pos_bias == "edge":
        loci = rng.choice([rmin, rmax])
        locj = rng.choice([cmin, cmax])
    elif pos_bias == "corners":
        loci, locj = rng.choice([(rmin, cmin), (rmin, cmax),
                                 (rmax, cmin), (rmax, cmax)])
    else:
        loci = rng.randint(rmin, rmax)
        locj = rng.randint(cmin, cmax)
    if "seed_row" in overrides:
        loci = max(0, min(h - 2, int(overrides["seed_row"])))
    if "seed_col" in overrides:
        locj = max(0, min(w - 1, int(overrides["seed_col"])))
    g = full_grid(h, w, 0)
    g[loci][locj] = fgc
    if bool(overrides.get("anchor_corner", False)):
        g[0][0] = fgc
        # ensure only one seed
        for r in range(h):
            for c in range(w):
                if (r, c) != (0, 0) and g[r][c] != 0:
                    g[r][c] = 0
        g[0][0] = fgc
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_seed":
        return g
    if name == "multiple_seeds":
        color = rng.choice([1, 2, 3, 5, 6, 7, 8, 9])
        g[1][1] = color
        g[h - 2][w - 2] = color
        return g
    if name == "seed_at_bottom_row":
        color = rng.choice([1, 2, 3, 5, 6, 7, 8, 9])
        g[h - 1][w // 2] = color
        return g
    return g
