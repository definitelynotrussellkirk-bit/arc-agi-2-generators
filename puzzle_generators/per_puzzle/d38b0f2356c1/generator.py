"""Generator for puzzle 09629e4f.

Rule: 11x11 grid is a 3x3 lattice of 3x3 blocks separated by gray
rows/cols. Exactly one block is "clean" (no cyan(8) cells); that
block is the template. Output: replace every block with the template,
preserve gray separators.

Combinatorial axes (8): clean_block, palette_kind, template_density,
sep_color, distractor_density, n_cyan_per_block, anchor_corner,
asymmetry_force.
Degenerates: all_blocks_clean, monochrome_template, max_distractors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d38b0f2356c1"
VERSION = "1.1.0"
TASK_ID = "d38b0f2356c1"
SUMMARY = "11x11 lattice; clean (no-cyan) block is template, replicated everywhere."

INVARIANTS = [
    "11x11 lattice with rows/cols 3 and 7 as gray(5) separators",
    "exactly one of the 9 blocks contains no cyan(8) cells",
    "the other 8 blocks each contain >=1 cyan(8) cell",
    "template block has >=1 non-bg cell (so output isn't all 0)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "pastel", "minimal")
TEMPLATE_KINDS = ("sparse", "dense", "symmetric", "asymmetric",
                  "diagonal", "centered", "corners")
DEGENERATE_TEXTURES = ("all_blocks_clean", "monochrome_template",
                       "max_distractors")
HELPFUL_TEXTURES = TEMPLATE_KINDS

AXES = {
    "clean_block":      {"type": "int", "default": "rng 0..8", "valid": "0..8"},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "template_kind":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(TEMPLATE_KINDS)},
    "template_density": {"type": "float", "default": "rng 0.3..0.7",
                         "valid": "0.1..1"},
    "distractor_density":{"type": "float", "default": "rng 0.4..0.7",
                          "valid": "0.1..1"},
    "sep_color":        {"type": "color", "default": "5", "valid": "5"},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for template_kind",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    clean = int(overrides.get("clean_block",
                              ctx.draw_int("clean_block", 0, 8)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    template_kind = (overrides.get("texture") or
                     overrides.get("template_kind")
                     or ctx.draw_choice("template_kind",
                                        list(TEMPLATE_KINDS)))
    t_density = float(overrides.get("template_density",
                                    ctx.draw_rng("template_density")
                                    .uniform(0.3, 0.7)))
    d_density = float(overrides.get("distractor_density",
                                    ctx.draw_rng("distractor_density")
                                    .uniform(0.4, 0.7)))
    palette = _build_palette(palette_kind, rng)
    g = full_grid(11, 11, 0)
    for i in (3, 7):
        for k in range(11):
            g[i][k] = 5
            g[k][i] = 5
    template = _build_template(template_kind, t_density, palette, rng)
    if not any(v != 0 for row in template for v in row):
        template[1][1] = palette[0] if palette else 2
    for bi in range(9):
        br = (bi // 3) * 4
        bc = (bi % 3) * 4
        if bi == clean:
            for r in range(3):
                for c in range(3):
                    g[br + r][bc + c] = template[r][c]
        else:
            for r in range(3):
                for c in range(3):
                    if rng.random() < d_density:
                        g[br + r][bc + c] = rng.choice(palette)
                    else:
                        g[br + r][bc + c] = 0
            rr = rng.randint(0, 2)
            cc = rng.randint(0, 2)
            g[br + rr][bc + cc] = 8
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 9]
    elif kind == "pastel":
        pool = [3, 4, 6, 7]
    elif kind == "minimal":
        pool = [2, 3]
    else:
        pool = [0, 2, 3, 4, 6, 7, 9]
    rng.shuffle(pool)
    return [c for c in pool if c != 8]


def _build_template(kind, density, palette, rng):
    grid = [[0] * 3 for _ in range(3)]
    if kind == "sparse":
        for r in range(3):
            for c in range(3):
                if rng.random() < min(density, 0.4):
                    grid[r][c] = rng.choice(palette)
    elif kind == "dense":
        for r in range(3):
            for c in range(3):
                if rng.random() < max(density, 0.7):
                    grid[r][c] = rng.choice(palette)
    elif kind == "symmetric":
        for r in range(3):
            for c in range(2):
                if rng.random() < density:
                    v = rng.choice(palette)
                    grid[r][c] = v
                    grid[r][2 - c] = v
    elif kind == "asymmetric":
        cells = [(r, c) for r in range(3) for c in range(3)]
        rng.shuffle(cells)
        for (r, c) in cells[:max(2, int(density * 9))]:
            grid[r][c] = rng.choice(palette)
    elif kind == "diagonal":
        for i in range(3):
            grid[i][i] = rng.choice(palette)
        if density > 0.5:
            for i in range(3):
                grid[i][2 - i] = rng.choice(palette)
    elif kind == "centered":
        grid[1][1] = rng.choice(palette)
        if density > 0.4:
            for r, c in [(0, 1), (1, 0), (1, 2), (2, 1)]:
                if rng.random() < density:
                    grid[r][c] = rng.choice(palette)
    elif kind == "corners":
        for r, c in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            if rng.random() < density + 0.2:
                grid[r][c] = rng.choice(palette)
    return grid


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    for i in (3, 7):
        for k in range(11):
            g[i][k] = 5
            g[k][i] = 5
    palette = [2, 3, 4, 6, 7, 9]
    rng.shuffle(palette)
    if name == "all_blocks_clean":
        for bi in range(9):
            br = (bi // 3) * 4
            bc = (bi % 3) * 4
            for r in range(3):
                for c in range(3):
                    if rng.random() < 0.5:
                        g[br + r][bc + c] = rng.choice(palette)
        return g
    if name == "monochrome_template":
        c = palette[0]
        for bi in range(9):
            br = (bi // 3) * 4
            bc = (bi % 3) * 4
            if bi != 4:
                g[br][bc] = 8
                g[br + 1][bc + 1] = c
            else:
                for r in range(3):
                    for cc in range(3):
                        g[br + r][bc + cc] = c
        return g
    if name == "max_distractors":
        for bi in range(9):
            br = (bi // 3) * 4
            bc = (bi % 3) * 4
            for r in range(3):
                for cc in range(3):
                    g[br + r][bc + cc] = rng.choice(palette)
            if bi != 0:
                rr = rng.randint(0, 2)
                cc = rng.randint(0, 2)
                g[br + rr][bc + cc] = 8
        return g
    return g
