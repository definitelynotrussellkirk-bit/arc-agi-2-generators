"""Generator for ARC task ca8de6ea.

Rule: input is 5 × 5. Output is 3 × 3 reading 9 fixed positions:
  out[0,0]=g[0,0]  out[0,1]=g[1,1]  out[0,2]=g[0,4]
  out[1,0]=g[1,3]  out[1,1]=g[2,2]  out[1,2]=g[3,1]
  out[2,0]=g[4,0]  out[2,1]=g[3,3]  out[2,2]=g[4,4]

Combinatorial axes: texture, palette_size, sampled_kind (controls colors
at the 9 sampled positions), unsampled_density (decoy elsewhere).
Degenerates: monochrome, all_zero_at_sampled, sampled_all_same.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b2f8fcc010d5"
VERSION = "1.1.0"
TASK_ID = "b2f8fcc010d5"
SUMMARY = "A 5 × 5 multicolor grid; rule reads 9 fixed positions into a 3 × 3 output."

INVARIANTS = [
    "input is 5 × 5",
    "the 9 sampled positions determine the output",
    "unsampled positions are decoy",
]

SAMPLED_KINDS = ("all_distinct", "two_colors", "single_color", "diagonal_marker", "noise")
DEGENERATE_TEXTURES = ("monochrome", "all_zero_at_sampled", "sampled_all_same")
HELPFUL_TEXTURES = SAMPLED_KINDS

SAMPLED_POSITIONS = [(0, 0), (1, 1), (0, 4),
                    (1, 3), (2, 2), (3, 1),
                    (4, 0), (3, 3), (4, 4)]

AXES = {
    "palette_size":      {"type": "int", "default": "rng 3..7", "valid": "1..10"},
    "sampled_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(SAMPLED_KINDS)},
    "unsampled_density": {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "texture":           {"type": "str", "default": "alias for sampled_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 3, 7)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(2, n_palette)))
    sampled_kind = (overrides.get("texture") or overrides.get("sampled_kind")
                    or ctx.draw_choice("sampled_kind", list(SAMPLED_KINDS)))
    decoy_d = float(overrides.get("unsampled_density",
                                  ctx.draw_rng("unsampled_density").uniform(0.3, 0.7)))
    g = full_grid(5, 5, palette[0])
    # Decoy fill
    for r in range(5):
        for c in range(5):
            if rng.random() < decoy_d:
                g[r][c] = rng.choice(palette)
    # Place sampled positions
    if sampled_kind == "all_distinct":
        for i, (r, c) in enumerate(SAMPLED_POSITIONS):
            g[r][c] = palette[i % len(palette)]
    elif sampled_kind == "two_colors":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        for i, (r, c) in enumerate(SAMPLED_POSITIONS):
            g[r][c] = a if i % 2 == 0 else b
    elif sampled_kind == "single_color":
        c0 = palette[0]
        for (r, c) in SAMPLED_POSITIONS:
            g[r][c] = c0
    elif sampled_kind == "diagonal_marker":
        for i, (r, c) in enumerate(SAMPLED_POSITIONS):
            g[r][c] = palette[(i // 3) % len(palette)]
    elif sampled_kind == "noise":
        for (r, c) in SAMPLED_POSITIONS:
            g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    palette = list(range(1, 10))
    rng.shuffle(palette)
    g = full_grid(5, 5, palette[0])
    if name == "monochrome":
        c0 = palette[0]
        for r in range(5):
            for c in range(5):
                g[r][c] = c0
        return g
    if name == "all_zero_at_sampled":
        # Sampled positions are 0; output is 3 × 3 all 0.
        for r in range(5):
            for c in range(5):
                g[r][c] = palette[0]
        for (r, c) in SAMPLED_POSITIONS:
            g[r][c] = 0
        return g
    if name == "sampled_all_same":
        c0 = palette[0]
        for r in range(5):
            for c in range(5):
                if rng.random() < 0.5:
                    g[r][c] = palette[1]
        for (r, c) in SAMPLED_POSITIONS:
            g[r][c] = c0
        return g
    return g
