"""Generator for arc_puzzle_bank_21_set12_bundle:medium_l14 — stamp transformed template at each cmd marker.

Rule: a full-5 row splits the grid. The top section's non-zero cells
are the template (cropped to bbox). The bottom section has cmd
markers in {1,2,3,4} (1=identity, 2=rot-cw, 3=rot-180, 4=transpose).
Each marker stamps the (transformed) template centered on the marker.
Output is the bottom region only.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers (no cmd markers → rule's per-marker stamp
loop is empty, output is bottom region unchanged), no_template (top
empty → rule's stamp has no shape), all_identity_markers (all cmds = 1
→ all stamps are identical, no per-marker transform contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "9adaf46a8128"
VERSION = "1.1.0"
TASK_ID = "9adaf46a8128"
SUMMARY = "Top template (color 2 cells) + full-5 row separator + bottom canvas with 1-3 transform-cmd markers."

INVARIANTS = [
    "background is 0",
    "rows 0..sep-1 hold a small 2-color template (cells in color 2)",
    "row `sep` is entirely 5",
    "rows sep+1..end-1 hold 1-3 cmd markers in {1, 2, 3, 4}",
    "markers are spaced enough that their centered stamps don't crowd each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_template", "all_identity_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "n_markers":      {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "template_separator_markers",
                       "valid": "template_separator_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 1), (0, 3), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        n_markers = ctx.draw_int("n_markers", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 16)
        n_markers = ctx.draw_int("n_markers", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_markers = ctx.draw_int("n_markers", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_TEMPLATES)
    th = max(c[0] for c in template) + 1
    tw = max(c[1] for c in template) + 1
    sep = th + 1
    if sep >= h - 2:
        sep = h - 4
    fill_box(g, sep, 0, sep, w - 1, 5)
    tr0 = rng.randint(0, max(0, sep - th))
    tc0 = rng.randint(0, w - tw)
    for dr, dc in template:
        g[tr0 + dr][tc0 + dc] = 2
    placed: list[tuple[int, int]] = []
    lo_r = sep + 1
    hi_r = h - 1
    lo_c = 0
    hi_c = w - 1
    if hi_r < lo_r or hi_c < lo_c:
        return g
    for _ in range(80):
        if len(placed) >= n_markers: break
        mr = rng.randint(lo_r, hi_r)
        mc = rng.randint(lo_c, hi_c)
        if any(abs(mr - pr) < 2 and abs(mc - pc) < 2 for pr, pc in placed):
            continue
        if g[mr][mc] != 0: continue
        g[mr][mc] = rng.choice([1, 2, 3, 4])
        placed.append((mr, mc))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    sep = 4
    fill_box(g, sep, 0, sep, w - 1, 5)
    if name == "no_markers":
        # No cmd markers — rule's stamp loop is empty; output is
        # bottom region unchanged.
        for dr, dc in _TEMPLATES[0]:
            g[1 + dr][2 + dc] = 2
        return g
    if name == "no_template":
        # Top empty — rule's template extractor finds nothing;
        # markers have no shape to stamp.
        g[6][3] = 1
        g[7][8] = 2
        return g
    if name == "all_identity_markers":
        # All cmds = 1 (identity) — all stamps identical; no
        # per-marker transform contrast.
        for dr, dc in _TEMPLATES[1]:
            g[1 + dr][2 + dc] = 2
        g[6][3] = 1
        g[7][8] = 1
        return g
    return g
