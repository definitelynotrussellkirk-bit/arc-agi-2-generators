"""Generator for 82819916.

Rule: template row + key rows; rule remaps each row using key/template
color correspondence.

Combinatorial axes (8): grid_h/w, n_template_cols, n_keys, palette_kind,
template_position, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_template, no_keys, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "83ca9df09514"
VERSION = "1.1.0"
TASK_ID = "83ca9df09514"
SUMMARY = "Template row + key rows; rule remaps each row."

INVARIANTS = [
    "background is 0",
    "one row (template) has strictly more non-zero cells than any other",
    "key rows have non-zero cells only at columns where template is non-zero",
    "key cells reveal a per-row color permutation",
]

POSITION_BIASES = ("top", "middle", "bottom", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_keys", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "n_template_cols":{"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "n_keys":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "template_position":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
    "texture":        {"type": "str", "default": "alias for template_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 8, 8, 10
        nc_lo, nc_hi = 3, 4
        nk_lo, nk_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 16, 14, 18
        nc_lo, nc_hi = 5, 8
        nk_lo, nk_hi = 3, 4
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 12, 10, 14
        nc_lo, nc_hi = 4, 6
        nk_lo, nk_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 4, rng)
    g = full_grid(h, w, 0)
    n_cols = int(overrides.get("n_template_cols",
                               ctx.draw_int("n_template_cols",
                                            nc_lo, nc_hi)))
    n_cols = max(3, min(w, n_cols))
    cols = rng.sample(range(w), n_cols)
    template_colors = [rng.choice(palette) for _ in cols]
    pos = (overrides.get("texture") or
           overrides.get("template_position")
           or ctx.draw_choice("template_position", list(POSITION_BIASES)))
    if pos == "top":
        template_row = 1
    elif pos == "middle":
        template_row = h // 2
    elif pos == "bottom":
        template_row = h - 2
    else:
        template_row = rng.randint(0, h - 1)
    template_row = max(0, min(template_row, h - 1))
    for col, color in zip(cols, template_colors):
        g[template_row][col] = color
    n_keys = int(overrides.get("n_keys",
                               ctx.draw_int("n_keys", nk_lo, nk_hi)))
    n_keys = max(1, min(4, n_keys))
    used_rows = {template_row}
    for _ in range(n_keys):
        for _try in range(20):
            kr = rng.randint(0, h - 1)
            if kr in used_rows:
                continue
            used_rows.add(kr)
            perm = rng.sample(palette, len(palette))
            mapping = dict(zip(palette, perm))
            n_reveal = rng.randint(1, 2)
            picks = rng.sample(list(zip(cols, template_colors)),
                               min(n_reveal, len(cols)))
            for col, tcolor in picks:
                g[kr][col] = mapping[tcolor]
            break
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_template":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.1:
                    g[r][c] = rng.choice([1, 2, 3, 4])
        return g
    if name == "no_keys":
        for c in range(2, 8):
            g[3][c] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
