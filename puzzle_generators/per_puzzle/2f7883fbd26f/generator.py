"""Generator for ARC task 1fad071e.

Rule: count 2 × 2 all-1 blocks; output is encode-bar(n, 5, 1) — a
1 × 5 grid with first n cells = 1, rest = 0.

Combinatorial axes (8): grid_h/w, n_target_blocks, block_layout,
decoy_density, decoy_palette_size, decoy_palette_density, bg_color.
Degenerates: zero_blocks, max_blocks, touching_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2f7883fbd26f"
VERSION = "1.1.0"
TASK_ID = "2f7883fbd26f"
SUMMARY = "Grid with sparse 2 × 2 all-1 blocks; rule outputs 1 × 5 bar of count."

INVARIANTS = [
    "0..5 2×2 all-1 blocks",
    "input dims allow ≥1 2×2 fit (h ≥ 2, w ≥ 2)",
]

BLOCK_LAYOUTS = ("random", "corners", "row", "clustered", "grid", "diagonal")
DEGENERATE_TEXTURES = ("zero_blocks", "max_blocks", "touching_blocks")
HELPFUL_TEXTURES = BLOCK_LAYOUTS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "grid_w":              {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "n_target_blocks":     {"type": "int", "default": "rng 1..5", "valid": "0..8"},
    "block_layout":        {"type": "str", "default": "rng helpful",
                            "valid": "|".join(BLOCK_LAYOUTS)},
    "decoy_density":       {"type": "float", "default": "rng 0..0.15", "valid": "0..0.5"},
    "decoy_palette_size":  {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "decoy_palette_density": {"type": "float", "default": "rng 0..0.2", "valid": "0..0.5"},
    "bg_color":            {"type": "color", "default": "0", "valid": "0..9"},
    "texture":             {"type": "str", "default": "alias for block_layout",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 5, 7, 1, 2
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 12, 14, 4, 5
    else:
        h_lo, h_hi, n_lo, n_hi = 5, 14, 1, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_blocks = max(0, min(5, int(overrides.get("n_target_blocks",
                                               ctx.draw_int("n_target_blocks", n_lo, n_hi)))))
    layout = (overrides.get("texture") or overrides.get("block_layout")
              or ctx.draw_choice("block_layout", list(BLOCK_LAYOUTS)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.15)))
    n_decor = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 3)))
    decor_d = float(overrides.get("decoy_palette_density",
                                  ctx.draw_rng("decoy_palette_density").uniform(0.0, 0.2)))
    g = full_grid(h, w, 0)
    anchors = _block_anchors(layout, h, w, n_blocks, rng)
    for ar, ac in anchors:
        if ar + 1 < h and ac + 1 < w:
            for dr in (0, 1):
                for dc in (0, 1):
                    g[ar + dr][ac + dc] = 1
    if decoy_d > 0:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0 and rng.random() < decoy_d:
                    if not _would_form_block(g, r, c):
                        g[r][c] = 1
    decor_palette = [c for c in range(2, 10)]
    rng.shuffle(decor_palette)
    decor_palette = decor_palette[:max(0, n_decor)]
    if decor_palette:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0 and rng.random() < decor_d:
                    g[r][c] = rng.choice(decor_palette)
    return g


def _block_anchors(layout, h, w, n, rng):
    if n == 0:
        return []
    if layout == "corners":
        return [(0, 0), (0, w - 2), (h - 2, 0), (h - 2, w - 2)][:n]
    if layout == "row":
        r = rng.randint(0, h - 2)
        return [(r, c) for c in range(0, w - 1, 3)][:n]
    if layout == "clustered":
        cr = rng.randint(0, h - 2); cc = rng.randint(0, w - 2)
        cells = [(r, c) for r in range(max(0, cr - 2), min(h - 1, cr + 3))
                 for c in range(max(0, cc - 2), min(w - 1, cc + 3))]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "grid":
        gap = max(2, h // (n + 1))
        return [((i // 3) * gap + 1, (i % 3) * gap + 1) for i in range(n)
                if (i // 3) * gap + 1 < h - 1][:n]
    if layout == "diagonal":
        return [(k * 3 % (h - 1), k * 3 % (w - 1)) for k in range(n)]
    candidates = [(r, c) for r in range(h - 1) for c in range(w - 1)]
    rng.shuffle(candidates)
    chosen: list = []
    for cand in candidates:
        if len(chosen) >= n: break
        if all(abs(cand[0] - cr) > 2 or abs(cand[1] - cc) > 2
               for (cr, cc) in chosen):
            chosen.append(cand)
    return chosen


def _would_form_block(g, r, c):
    h = len(g); w = len(g[0])
    for ar in (r - 1, r):
        for ac in (c - 1, c):
            if 0 <= ar < h - 1 and 0 <= ac < w - 1:
                cells = [g[ar][ac], g[ar][ac + 1], g[ar + 1][ac], g[ar + 1][ac + 1]]
                if cells.count(1) == 3:
                    return True
    return False


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "zero_blocks":
        for r in range(0, h, 3):
            for c in range(0, w, 3):
                g[r][c] = 1
        return g
    if name == "max_blocks":
        anchors = [(0, 0), (0, 4), (3, 0), (3, 4), (3, 8)][:5]
        for ar, ac in anchors:
            if ar + 1 < h and ac + 1 < w:
                for dr in (0, 1):
                    for dc in (0, 1):
                        g[ar + dr][ac + dc] = 1
        return g
    if name == "touching_blocks":
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 1
        return g
    return g
