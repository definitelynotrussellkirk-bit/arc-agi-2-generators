"""Generator for 5614dbcf.

Rule: 3*bh × 3*bw grid divided into 3×3 sub-blocks; for each block
output the most common value into a 3×3 result grid.

Combinatorial axes (8): block_h, block_w, n_filled_blocks,
palette_size, stray_density, fill_layout, position_distribution,
stray_color.
Degenerates: empty_grid, all_filled, single_block.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "bbcc617baafb"
VERSION = "1.1.0"
TASK_ID = "bbcc617baafb"
SUMMARY = "9×9 grid; rule emits 3×3 of mode-per-3×3-block."

INVARIANTS = [
    "h % 3 == 0 and w % 3 == 0",
    ">=2 sub-blocks have a STRICTLY dominant non-bg color",
    ">=1 sub-block has mode = 0 (or stray-color minority)",
    "stray cells count is < block-cell-count / 2 (so they don't outvote dominant color)",
]

FILL_LAYOUTS = ("solid", "majority", "ring", "frame")
DEGENERATE_TEXTURES = ("empty_grid", "all_filled", "single_block")
HELPFUL_TEXTURES = FILL_LAYOUTS

AXES = {
    "block_h":            {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "block_w":            {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "n_filled_blocks":    {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "palette_size":       {"type": "int", "default": "= n_filled",
                           "valid": "1..7"},
    "stray_density":      {"type": "float", "default": "rng 0.05..0.15",
                           "valid": "0..0.3"},
    "fill_layout":        {"type": "str", "default": "rng helpful",
                           "valid": "|".join(FILL_LAYOUTS)},
    "stray_color":        {"type": "color", "default": "5", "valid": "1..9"},
    "position_distribution": {"type": "str", "default": "rng spread|corner|diag",
                              "valid": "spread|corner|diag"},
    "texture":            {"type": "str", "default": "alias for fill_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        bh_lo, bh_hi = 2, 2
    elif difficulty == "hard":
        bh_lo, bh_hi = 4, 6
    else:
        bh_lo, bh_hi = 2, 4
    bh = ctx.draw_int("block_h", bh_lo, bh_hi)
    bw = ctx.draw_int("block_w", bh_lo, bh_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], bh, bw, rng)
    h = 3 * bh
    w = 3 * bw
    n_filled = int(overrides.get("n_filled_blocks",
                                 ctx.draw_int("n_filled_blocks", 3, 6)))
    n_filled = max(1, min(9, n_filled))
    pool = [c for c in range(1, 10) if c not in (0, 5)]
    rng.shuffle(pool)
    pal = pool[:max(1, n_filled)]
    layout = (overrides.get("texture") or overrides.get("fill_layout")
              or ctx.draw_choice("fill_layout", list(FILL_LAYOUTS)))
    stray_density = float(overrides.get("stray_density",
                                        ctx.draw_rng("stray_density")
                                        .uniform(0.05, 0.15)))
    stray_color = int(overrides.get("stray_color", 5))
    pos_dist = overrides.get("position_distribution",
                             ctx.draw_choice("position_distribution",
                                             ["spread", "corner", "diag"]))
    g = full_grid(h, w, 0)
    blocks = [(r0, c0) for r0 in range(0, h, bh) for c0 in range(0, w, bw)]
    chosen = _pick_blocks(pos_dist, blocks, n_filled, rng)
    for i, (r0, c0) in enumerate(chosen):
        color = pal[i % len(pal)]
        _fill_block(g, layout, r0, c0, bh, bw, color, rng)
    n_strays = max(1, int(stray_density * h * w))
    placed = 0
    tries = 0
    while placed < n_strays and tries < 30:
        tries += 1
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = stray_color
            placed += 1
    return g


def _pick_blocks(dist, blocks, n, rng):
    if dist == "corner":
        # corners first
        bh, bw = blocks[-1]
        corners = [(0, 0), (0, bw), (bh, 0), (bh, bw)]
        chosen = [b for b in corners if b in blocks][:n]
        rest = [b for b in blocks if b not in chosen]
        rng.shuffle(rest)
        return chosen + rest[:n - len(chosen)]
    if dist == "diag":
        sz = int(len(blocks) ** 0.5)
        diag = [blocks[i * sz + i] for i in range(sz) if i * sz + i < len(blocks)]
        rest = [b for b in blocks if b not in diag]
        rng.shuffle(rest)
        return (diag + rest)[:n]
    rng.shuffle(blocks)
    return blocks[:n]


def _fill_block(g, layout, r0, c0, bh, bw, color, rng):
    if layout == "solid":
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = color
        return
    if layout == "majority":
        cells = [(r, c) for r in range(r0, r0 + bh) for c in range(c0, c0 + bw)]
        n_fill = max(1, len(cells) // 2 + 1)
        rng.shuffle(cells)
        for r, c in cells[:n_fill]:
            g[r][c] = color
        return
    if layout == "ring":
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                if r == r0 or r == r0 + bh - 1 or c == c0 or c == c0 + bw - 1:
                    g[r][c] = color
        return
    if layout == "frame":
        for r in range(r0, r0 + bh):
            g[r][c0] = color
            g[r][c0 + bw - 1] = color
        for c in range(c0, c0 + bw):
            g[r0][c] = color
            g[r0 + bh - 1][c] = color
        return
    for r in range(r0, r0 + bh):
        for c in range(c0, c0 + bw):
            g[r][c] = color


def _draw_from_degenerate(name, bh, bw, rng):
    h, w = 3 * bh, 3 * bw
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    if name == "empty_grid":
        return g
    if name == "all_filled":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "single_block":
        for r in range(bh):
            for c in range(bw):
                g[r][c] = color
        return g
    return g
