"""Generator for puzzle 8e5a5113.

Rule: input is n × (3n+2) with cols n and 2n+1 as 5-separators. Section
0 (cols 0..n-1) is content; sections 1 and 2 are zero (rule fills them
with rotated/reflected copies of section 0).

Combinatorial axes (8): grid_n, palette_size, palette_kind,
section_density, section_pattern, anchor_corner, asymmetry_force,
fill_density.
Degenerates: empty_section, full_section, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "616a5c01a7ea"
VERSION = "1.1.0"
TASK_ID = "616a5c01a7ea"
SUMMARY = "n × (3n+2) grid with section 0 content + 5-cols + zero sections."

INVARIANTS = [
    "n in [3, 7]",
    "width = 3*n + 2",
    "cols n and 2*n+1 are all 5",
    "section 0 has >=2 distinct non-bg colors",
    "sections 1 and 2 are all zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary", "pastel")
SECTION_PATTERNS = ("noise", "stripes", "checker", "diagonal",
                    "blob", "solid_run", "corners")
DEGENERATE_TEXTURES = ("empty_section", "full_section", "monochrome")
HELPFUL_TEXTURES = SECTION_PATTERNS

AXES = {
    "grid_n":           {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "palette_size":     {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "section_pattern":  {"type": "str", "default": "rng helpful",
                         "valid": "|".join(SECTION_PATTERNS)},
    "fill_density":     {"type": "float", "default": "rng 0.5..0.9",
                         "valid": "0.2..1"},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "asymmetry_force":  {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for section_pattern",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_lo, n_hi = 3, 3
    elif difficulty == "hard":
        n_lo, n_hi = 5, 7
    else:
        n_lo, n_hi = 3, 5
    n = ctx.draw_int("grid_n", n_lo, n_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 2, 4)))
    palette_size = max(2, min(6, palette_size))
    pattern = (overrides.get("texture") or
               overrides.get("section_pattern")
               or ctx.draw_choice("section_pattern",
                                  list(SECTION_PATTERNS)))
    density = float(overrides.get("fill_density",
                                  ctx.draw_rng("fill_density")
                                  .uniform(0.5, 0.9)))
    palette = _build_palette(palette_kind, palette_size, rng)
    sec_w = n
    w = 3 * sec_w + 2
    g = full_grid(n, w, 0)
    _fill_section0(g, pattern, n, sec_w, palette, density, rng)
    for r in range(n):
        g[r][sec_w] = 5
        g[r][2 * sec_w + 1] = 5
    if not _has_two_colors(g, n, sec_w):
        g[0][0] = palette[0]
        g[n - 1][sec_w - 1] = palette[1] if len(palette) > 1 else 1
    return g


def _has_two_colors(g, n, sec_w):
    seen = set()
    for r in range(n):
        for c in range(sec_w):
            if g[r][c] != 0:
                seen.add(g[r][c])
    return len(seen) >= 2


def _build_palette(kind, size, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3]
    elif kind == "pastel":
        pool = [3, 4, 6, 7]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    while len(pool) < size:
        for c in [1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= size:
                break
    return pool[:size]


def _fill_section0(g, pattern, n, sec_w, palette, density, rng):
    if pattern == "noise":
        for r in range(n):
            for c in range(sec_w):
                if rng.random() < density:
                    g[r][c] = rng.choice(palette)
    elif pattern == "stripes":
        for r in range(n):
            color = palette[r % len(palette)]
            for c in range(sec_w):
                if rng.random() < density:
                    g[r][c] = color
    elif pattern == "checker":
        for r in range(n):
            for c in range(sec_w):
                if (r + c) % 2 == 0 and rng.random() < density + 0.2:
                    g[r][c] = palette[0]
                elif rng.random() < density - 0.2:
                    g[r][c] = palette[-1]
    elif pattern == "diagonal":
        for i in range(min(n, sec_w)):
            g[i][i] = palette[i % len(palette)]
        for r in range(n):
            for c in range(sec_w):
                if r != c and rng.random() < density / 2:
                    g[r][c] = palette[(r + c) % len(palette)]
    elif pattern == "blob":
        cr, cc = rng.randint(0, n - 1), rng.randint(0, sec_w - 1)
        for r in range(n):
            for c in range(sec_w):
                if abs(r - cr) + abs(c - cc) <= 2 and rng.random() < density:
                    g[r][c] = palette[0 if (r + c) % 2 == 0
                                       else -1 % len(palette)]
    elif pattern == "solid_run":
        for r in range(n):
            color = palette[r % len(palette)]
            for c in range(sec_w):
                g[r][c] = color
    elif pattern == "corners":
        for r, c in [(0, 0), (0, sec_w - 1), (n - 1, 0),
                      (n - 1, sec_w - 1)]:
            g[r][c] = palette[(r + c) % len(palette)]
    else:
        for r in range(n):
            for c in range(sec_w):
                if rng.random() < density:
                    g[r][c] = rng.choice(palette)


def _draw_from_degenerate(name, n, rng):
    sec_w = n
    w = 3 * sec_w + 2
    g = full_grid(n, w, 0)
    for r in range(n):
        g[r][sec_w] = 5
        g[r][2 * sec_w + 1] = 5
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    if name == "empty_section":
        # Section 0 is all zero; the rotations are also zero — output
        # equals input modulo 5-separators. May fail validate if
        # output_equals_input gate is on.
        return g
    if name == "full_section":
        for r in range(n):
            for c in range(sec_w):
                g[r][c] = palette[0]
        return g
    if name == "monochrome":
        for r in range(n):
            for c in range(sec_w):
                g[r][c] = palette[0]
        return g
    return g
