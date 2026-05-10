"""Generator for puzzle e0fb7511.

Rule: bg = mode (most common color). For each non-bg object: if size > 1,
recolor to 8; else keep. Effect: clustered non-bg objects become cyan,
isolated singletons stay.

Hmm — re-reading: `(for-each-object g (objects g bg) ...)`. So objects
are non-bg. For each non-bg object: if size > 1 → paint 8; else keep.

Combinatorial axes: grid_h/w, bg_color, noise_palette_size, n_clusters,
n_singletons, cluster_kind. Degenerates: only_singletons,
only_clusters, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "57bafcdde8c3"
VERSION = "1.1.0"
TASK_ID = "57bafcdde8c3"
SUMMARY = "Noise + clustered/isolated cells; rule recolors non-bg objects with size > 1 to cyan(8)."

INVARIANTS = [
    "bg = mode color (well-defined)",
    "≥1 non-bg object of size ≥ 2 (becomes 8)",
    "≥1 isolated non-bg pixel (size 1, stays)",
]

CLUSTER_KINDS = ("L_shape", "rect", "line_h", "line_v", "blob", "cross")
DEGENERATE_TEXTURES = ("only_singletons", "only_clusters", "no_objects")
HELPFUL_TEXTURES = CLUSTER_KINDS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":             {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "bg_color":           {"type": "color", "default": "rng (≠8)", "valid": "0..9 (≠8)"},
    "noise_palette_size": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "n_clusters":         {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "n_singletons":       {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "cluster_kind":       {"type": "str", "default": "rng helpful",
                           "valid": "|".join(CLUSTER_KINDS)},
    "texture":            {"type": "str", "default": "alias for cluster_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, c_lo, c_hi, s_lo, s_hi = 7, 9, 1, 1, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, c_lo, c_hi, s_lo, s_hi = 12, 14, 2, 3, 4, 5
    else:
        h_lo, h_hi, c_lo, c_hi, s_lo, s_hi = 7, 14, 1, 3, 2, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)
    bg = int(overrides.get("bg_color", ctx.draw_color("bg_color", exclude={8})))
    n_noise = int(overrides.get("noise_palette_size",
                                ctx.draw_int("noise_palette_size", 2, 3)))
    noise_palette = list(ctx.draw_distinct_colors(
        "noise", n=max(1, n_noise), exclude={bg, 8})) or [1]
    n_clusters = int(overrides.get("n_clusters",
                                   ctx.draw_int("n_clusters", c_lo, c_hi)))
    n_singletons = int(overrides.get("n_singletons",
                                     ctx.draw_int("n_singletons", s_lo, s_hi)))
    cluster_kind = (overrides.get("texture") or overrides.get("cluster_kind")
                    or ctx.draw_choice("cluster_kind", list(CLUSTER_KINDS)))
    g = full_grid(h, w, bg)
    occupied: set[tuple[int, int]] = set()
    # Plant clusters
    for i in range(n_clusters):
        for _try in range(20):
            sh = rng.randint(2, max(2, h // 4))
            sw = rng.randint(2, max(2, w // 4))
            rr = rng.randint(1, max(1, h - sh - 1))
            rc = rng.randint(1, max(1, w - sw - 1))
            cells = _cluster_cells(cluster_kind, sh, sw)
            actual = [(rr + dr, rc + dc) for dr, dc in cells]
            buffer = set()
            for (r, c) in actual:
                for ddr in (-1, 0, 1):
                    for ddc in (-1, 0, 1):
                        buffer.add((r + ddr, c + ddc))
            if any(p in occupied for p in buffer):
                continue
            color = noise_palette[i % len(noise_palette)]
            for (r, c) in actual:
                if 0 <= r < h and 0 <= c < w:
                    g[r][c] = color
                    occupied.add((r, c))
            break
    # Plant singletons
    for i in range(n_singletons):
        for _try in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            # Must not touch existing non-bg
            if any((r + dr, c + dc) in occupied
                   for dr in (-1, 0, 1) for dc in (-1, 0, 1)):
                continue
            color = noise_palette[(i + n_clusters) % len(noise_palette)]
            g[r][c] = color
            occupied.add((r, c))
            break
    return g


def _cluster_cells(kind, sh, sw):
    if kind == "rect":
        return [(dr, dc) for dr in range(sh) for dc in range(sw)]
    if kind == "L_shape":
        out = [(dr, 0) for dr in range(sh)]
        out += [(sh - 1, dc) for dc in range(1, sw)]
        return out
    if kind == "line_h":
        return [(0, dc) for dc in range(sw)]
    if kind == "line_v":
        return [(dr, 0) for dr in range(sh)]
    if kind == "blob":
        return [(0, 0), (0, 1), (1, 0)]
    if kind == "cross":
        mr, mc = sh // 2, sw // 2
        out = [(mr, dc) for dc in range(sw)]
        out += [(dr, mc) for dr in range(sh) if dr != mr]
        return list(set(out))
    return [(0, 0), (0, 1), (1, 0)]


def _draw_from_degenerate(name, h, w, ctx, rng):
    bg = ctx.draw_color("bg_color", exclude={8})
    noise = list(ctx.draw_distinct_colors("noise", n=2, exclude={bg, 8})) or [1]
    g = full_grid(h, w, bg)
    if name == "only_singletons":
        cells = [(r, c) for r in range(0, h, 2) for c in range(0, w, 2)]
        rng.shuffle(cells)
        for r, c in cells[:8]:
            g[r][c] = noise[0]
        return g
    if name == "only_clusters":
        # 3 clusters of size ≥ 2.
        for r in range(1, 3):
            for c in range(1, 3):
                g[r][c] = noise[0]
        for r in range(1, 3):
            for c in range(w - 3, w - 1):
                g[r][c] = noise[1] if len(noise) > 1 else noise[0]
        return g
    if name == "no_objects":
        return g
    return g
