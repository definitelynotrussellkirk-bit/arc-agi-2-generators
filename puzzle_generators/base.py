"""GenCtx — keyed-draw generator context for puzzle-instance generators.

Every random decision goes through `ctx.draw_*(label, ...)`. The label
is hashed against `(seed, sample_index, version, task_id)` to seed an
independent `random.Random`, so adding/removing/reordering draws cannot
affect other draws and the same arguments always produce the same grid.

Mirrors the rack project's GenCtx pattern (~/Desktop/rack/gen/base.py),
adapted for ARC: instead of math-problem domain helpers we expose
draw_color, draw_grid_size, draw_rect_size, draw_rect_position,
draw_distinct_colors, draw_shape.

Cardinal rules (see docs/PUZZLE_GENERATOR_SPEC.md "Anti-patterns"):
  - Never use bare `random.*` inside a generator. Always go through ctx.
  - Override values from the caller's **overrides dict take precedence
    over the random draw, but pass the same validity gate.
  - draw_choice / draw_color / etc. accept an `exclude` set to filter
    illegal values; the underlying RNG is re-rolled until a valid value
    is drawn (capped at MAX_RETRIES).
"""
from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from typing import Any, Iterable, Optional, Sequence

# Cap re-rolls per draw — protects against impossible exclude sets without
# falling into an infinite loop.
MAX_RETRIES = 256


# ---------------------------------------------------------------------------
# Stable RNG construction
# ---------------------------------------------------------------------------

def stable_rng(seed: int, salt: str, version: str = "0") -> random.Random:
    """Hash-seeded RNG that is stable across Python versions.

    Two calls with identical (seed, salt, version) return RNGs that
    produce identical sequences. Mirrors rack's stable_rng.
    """
    h = hashlib.sha256(f"{seed}|{salt}|{version}".encode()).digest()
    return random.Random(int.from_bytes(h[:16], "big"))


# ---------------------------------------------------------------------------
# GenCtx
# ---------------------------------------------------------------------------

@dataclass
class GenCtx:
    """Per-instance generator context.

    Fields:
      seed:          caller-provided integer; identifies the instance family.
      sample_index:  index within the family (e.g., 0..149 for a 150-batch).
      version:       generator's VERSION string. Bumping invalidates caches.
      task_id:       which puzzle this generator produces variants of.
      difficulty:    "easy" | "medium" | "hard" | None — optional shape hint.
      overrides:     caller-provided kwargs that short-circuit specific draws.
      _drawn:        records what label produced what value (for provenance).
      _override_used: subset of `overrides` that the generator actually consumed.
    """
    seed: int
    sample_index: int
    version: str = "0"
    task_id: str = ""
    difficulty: Optional[str] = None
    overrides: dict = field(default_factory=dict)
    _drawn: dict = field(default_factory=dict)
    _override_used: dict = field(default_factory=dict)

    # ---- core draw mechanics --------------------------------------------

    def draw_rng(self, label: str) -> random.Random:
        """Get a deterministic, label-keyed RNG for ad-hoc draws.

        Use this when none of the higher-level draw_* methods fit. Most
        generator code should prefer the typed methods below."""
        salt = f"{self.task_id}|{self.sample_index}|{label}"
        return stable_rng(self.seed, salt, self.version)

    def _record(self, label: str, value: Any, *, from_override: bool) -> Any:
        if from_override:
            self._override_used[label] = value
        self._drawn[label] = value
        return value

    def _override(self, label: str) -> tuple[bool, Any]:
        """If the caller overrode this label, return (True, value)."""
        if label in self.overrides and self.overrides[label] is not None:
            return True, self.overrides[label]
        return False, None

    # ---- typed draws ----------------------------------------------------

    def draw_int(self, label: str, lo: int, hi: int) -> int:
        """Inclusive integer in [lo, hi]."""
        if hi < lo:
            raise ValueError(f"draw_int({label!r}): hi ({hi}) < lo ({lo})")
        used, ov = self._override(label)
        if used:
            v = int(ov)
            if not (lo <= v <= hi):
                raise ValueError(
                    f"draw_int({label!r}): override {v} outside [{lo}, {hi}]")
            return self._record(label, v, from_override=True)
        rng = self.draw_rng(label)
        return self._record(label, rng.randint(lo, hi), from_override=False)

    def _diff_band(self) -> tuple[float, float]:
        """Map self.difficulty to a (lb, ub) band in [0, 1]. Used by
        draw_int_diff and any caller that wants difficulty-aware sampling."""
        d = self.difficulty
        if isinstance(d, str):
            return {
                "easy": (0.0, 0.33),
                "medium": (0.33, 0.66),
                "hard": (0.66, 1.0),
            }.get(d, (0.0, 1.0))
        if isinstance(d, (int, float)):
            x = max(0.0, min(1.0, float(d)))
            return (max(0.0, x - 0.1), min(1.0, x + 0.1))
        return (0.0, 1.0)

    def draw_int_diff(self, label: str, lo: int, hi: int) -> int:
        """Difficulty-knob int draw in [lo, hi]. With self.difficulty
        unset, behaves like uniform over the full band (close to draw_int
        but slightly different roll cadence). With "easy"/"medium"/"hard"
        or a float in [0, 1], skews toward lo or hi accordingly.

        Mirrors re-arc/utils.py::unifint, ported to our gen_ctx so
        re-arc generators translate cleanly."""
        if hi < lo:
            raise ValueError(f"draw_int_diff({label!r}): hi ({hi}) < lo ({lo})")
        used, ov = self._override(label)
        if used:
            v = int(ov)
            if not (lo <= v <= hi):
                raise ValueError(
                    f"draw_int_diff({label!r}): override {v} outside [{lo}, {hi}]")
            return self._record(label, v, from_override=True)
        rng = self.draw_rng(label)
        diff_lb, diff_ub = self._diff_band()
        d = rng.uniform(diff_lb, diff_ub)
        v = min(max(lo, round(lo + (hi - lo) * d)), hi)
        return self._record(label, v, from_override=False)

    def draw_choice(self, label: str, options: Sequence) -> Any:
        """Pick one element of options."""
        if not options:
            raise ValueError(f"draw_choice({label!r}): empty options")
        used, ov = self._override(label)
        if used:
            if ov not in options:
                raise ValueError(
                    f"draw_choice({label!r}): override {ov!r} not in options")
            return self._record(label, ov, from_override=True)
        rng = self.draw_rng(label)
        return self._record(label, rng.choice(list(options)), from_override=False)

    def draw_color(self, label: str, *, exclude: Iterable[int] = ()) -> int:
        """A color in 0..9, optionally excluding some values."""
        bad = set(int(x) for x in exclude)
        legal = [c for c in range(10) if c not in bad]
        if not legal:
            raise ValueError(f"draw_color({label!r}): exclude={bad} leaves no colors")
        used, ov = self._override(label)
        if used:
            v = int(ov)
            if v in bad or not (0 <= v <= 9):
                raise ValueError(
                    f"draw_color({label!r}): override {v} not in legal colors {legal}")
            return self._record(label, v, from_override=True)
        rng = self.draw_rng(label)
        return self._record(label, rng.choice(legal), from_override=False)

    def draw_distinct_colors(
        self, label: str, *, n: int, exclude: Iterable[int] = ()
    ) -> tuple[int, ...]:
        """n distinct colors in 0..9, none in `exclude`."""
        bad = set(int(x) for x in exclude)
        legal = [c for c in range(10) if c not in bad]
        if n > len(legal):
            raise ValueError(
                f"draw_distinct_colors({label!r}): want {n}, only {len(legal)} legal")
        used, ov = self._override(label)
        if used:
            seq = tuple(int(x) for x in ov)
            if len(seq) != n:
                raise ValueError(
                    f"draw_distinct_colors({label!r}): override length {len(seq)} != {n}")
            if len(set(seq)) != n:
                raise ValueError(
                    f"draw_distinct_colors({label!r}): override has duplicates")
            for c in seq:
                if c in bad or not (0 <= c <= 9):
                    raise ValueError(
                        f"draw_distinct_colors({label!r}): override color {c} illegal")
            return self._record(label, seq, from_override=True)
        rng = self.draw_rng(label)
        seq = tuple(rng.sample(legal, n))
        return self._record(label, seq, from_override=False)

    def draw_grid_size(
        self, label: str, *, lo: tuple[int, int] = (5, 5),
        hi: tuple[int, int] = (20, 20),
    ) -> tuple[int, int]:
        """An (h, w) pair with each dimension in its respective range."""
        used, ov = self._override(label)
        if used:
            h, w = int(ov[0]), int(ov[1])
            if not (lo[0] <= h <= hi[0] and lo[1] <= w <= hi[1]):
                raise ValueError(
                    f"draw_grid_size({label!r}): override ({h},{w}) outside [{lo},{hi}]")
            return self._record(label, (h, w), from_override=True)
        rng = self.draw_rng(label)
        h = rng.randint(lo[0], hi[0])
        w = rng.randint(lo[1], hi[1])
        return self._record(label, (h, w), from_override=False)

    def draw_rect_size(
        self, label: str, *, grid: tuple[int, int],
        margin: int = 1, min_dim: int = 1,
    ) -> tuple[int, int]:
        """An (rh, rw) such that an rh×rw rect fits inside grid with `margin`
        on every side, and each dimension is at least `min_dim`."""
        h, w = grid
        max_rh = h - 2 * margin
        max_rw = w - 2 * margin
        if max_rh < min_dim or max_rw < min_dim:
            raise ValueError(
                f"draw_rect_size({label!r}): grid {grid} too small for "
                f"min_dim={min_dim} and margin={margin}")
        used, ov = self._override(label)
        if used:
            rh, rw = int(ov[0]), int(ov[1])
            if not (min_dim <= rh <= max_rh and min_dim <= rw <= max_rw):
                raise ValueError(
                    f"draw_rect_size({label!r}): override ({rh},{rw}) doesn't fit")
            return self._record(label, (rh, rw), from_override=True)
        rng = self.draw_rng(label)
        rh = rng.randint(min_dim, max_rh)
        rw = rng.randint(min_dim, max_rw)
        return self._record(label, (rh, rw), from_override=False)

    def draw_rect_position(
        self, label: str, *, grid: tuple[int, int],
        size: tuple[int, int], margin: int = 1,
    ) -> tuple[int, int]:
        """An (rr, rc) such that a `size`-shaped rect at (rr, rc) fits in
        grid with `margin` on every side."""
        h, w = grid
        rh, rw = size
        max_rr = h - rh - margin
        max_rc = w - rw - margin
        if max_rr < margin or max_rc < margin:
            raise ValueError(
                f"draw_rect_position({label!r}): no legal position for "
                f"size={size} in grid={grid} with margin={margin}")
        used, ov = self._override(label)
        if used:
            rr, rc = int(ov[0]), int(ov[1])
            if not (margin <= rr <= max_rr and margin <= rc <= max_rc):
                raise ValueError(
                    f"draw_rect_position({label!r}): override ({rr},{rc}) illegal")
            return self._record(label, (rr, rc), from_override=True)
        rng = self.draw_rng(label)
        rr = rng.randint(margin, max_rr)
        rc = rng.randint(margin, max_rc)
        return self._record(label, (rr, rc), from_override=False)


def gen_ctx(
    *, seed: int, sample_index: int, version: str = "0",
    task_id: str = "", difficulty: Optional[str] = None,
    overrides: Optional[dict] = None,
) -> GenCtx:
    """Construct a GenCtx. Use this from generator modules; do not
    instantiate GenCtx directly so we can extend the API without
    breaking call sites."""
    return GenCtx(
        seed=seed, sample_index=sample_index, version=version,
        task_id=task_id, difficulty=difficulty,
        overrides=dict(overrides or {}),
    )
