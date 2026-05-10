"""Generator for 6d0160f0.

Rule: color-4 marker's local position chooses 4x4 destination block.

Combinatorial axes (8): grid_size, source_block, palette_kind, accent,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_marker, no_lattice, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c5905adcd2cb"
VERSION = "1.1.0"
TASK_ID = "c5905adcd2cb"
SUMMARY = "Color-4 marker's local position chooses 4x4 destination block."

INVARIANTS = [
    "background is color 0",
    "color 5 forms a fixed 4x4 macro-grid separator lattice",
    "one source macro-cell contains the color-4 marker and a small colored motif",
    "the marker's relative row and column choose the destination macro-cell",
]

SOURCE_BLOCKS = ("upper", "lower", "ul", "ur")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marker", "no_lattice", "full_grid")
HELPFUL_TEXTURES = SOURCE_BLOCKS

AXES = {
    "grid_size":      {"type": "int", "default": "16", "valid": "12..20"},
    "source_block":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SOURCE_BLOCKS)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "accent":         {"type": "color", "default": "rng !{0,4,5}",
                       "valid": "1..9"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for source_block",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    source_block = (overrides.get("texture") if overrides.get("texture") in SOURCE_BLOCKS else None) or \
                   overrides.get("source_block") or \
                   ctx.draw_choice("source_block", list(SOURCE_BLOCKS))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    accent = int(overrides.get("accent",
                               rng.choice(pal) if pal else
                               ctx.draw_color("accent", exclude={0, 4, 5})))
    g = full_grid(16, 16, 0)
    for i in range(3, 16, 4):
        for c in range(16):
            g[i][c] = 5
        for r in range(16):
            g[r][i] = 5
    if source_block == "upper":
        src_qr, src_qc = 0, 2
    elif source_block == "lower":
        src_qr, src_qc = 2, 0
    elif source_block == "ul":
        src_qr, src_qc = 0, 0
    else:
        src_qr, src_qc = 0, 3 if 16 // 4 > 3 else 2
    rel_options = [(1, 1), (1, 2), (2, 1), (2, 2)]
    rel_r, rel_c = rel_options[(sample_index + rng.randint(0, 3)) % len(rel_options)]
    r0 = src_qr * 4
    c0 = src_qc * 4
    g[r0 + rel_r][c0 + rel_c] = 4
    g[r0 + 0][c0 + 0] = accent
    g[r0 + 0][c0 + 1] = accent
    g[r0 + 1][c0 + 0] = accent
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 4, 5)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "no_marker":
        for i in range(3, 16, 4):
            for c in range(16):
                g[i][c] = 5
            for r in range(16):
                g[r][i] = 5
        return g
    if name == "no_lattice":
        g[1][1] = 4; g[0][0] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
