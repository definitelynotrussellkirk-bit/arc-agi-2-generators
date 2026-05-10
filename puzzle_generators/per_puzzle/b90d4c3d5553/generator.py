"""Generator for arc_puzzle_bank_21_set22_s:S22_H5.

Two local coordinate frames are marked by colors 2/3/4 and 5/6/7. The
source frame has an 8-motif around it; only points with a reflected partner
across the local vertical axis are copied into the target frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b90d4c3d5553"
VERSION = "1.1.0"
TASK_ID = "b90d4c3d5553"
SUMMARY = "Copy only source-frame 8 cells whose local mirror partner exists."

INVARIANTS = [
    "one source frame is marked by colors 2, 3, and 4",
    "one target frame is marked by colors 5, 6, and 7",
    "source motif cells are color 8 and lie within local radius 3",
    "at least one mirrored local pair copies into empty target-frame cells",
]

AXES = {
    "extra_pair": {"type": "int", "default": "rng 0..2", "valid": "0..2"},
}

_BASE_PAIRS = [
    ((-2, -1), (2, -1)),
    ((-1, 2), (1, 2)),
]
_OPTIONAL_PAIRS = [
    ((-3, 0), (3, 0)),
    ((-2, 3), (2, 3)),
    ((-1, -3), (1, -3)),
]
_NOISE = [(3, 1), (-2, 2), (1, -2)]


def _put_frame(g, origin, colors):
    r, c = origin
    g[r][c] = colors[0]
    g[r][c + 1] = colors[1]
    g[r + 1][c] = colors[2]


def _global(origin, u, v):
    r, c = origin
    return r + v, c + u


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    extra_pair = ctx.draw_int("extra_pair", 0, 2)
    rng = ctx.draw_rng("layout")

    src = (6 + rng.randint(-1, 1), 4)
    tgt = (6 + rng.randint(-1, 1), 13)
    g = full_grid(12, 18, 0)
    _put_frame(g, src, (2, 3, 4))
    _put_frame(g, tgt, (5, 6, 7))

    motif = []
    for pair in _BASE_PAIRS:
        motif.extend(pair)
    motif.extend(_OPTIONAL_PAIRS[extra_pair])
    motif.extend(rng.sample(_NOISE, 2))

    blocked = {(0, 0), (1, 0), (0, 1)}
    for u, v in motif:
        if (u, v) in blocked:
            continue
        r, c = _global(src, u, v)
        g[r][c] = 8
    return g
