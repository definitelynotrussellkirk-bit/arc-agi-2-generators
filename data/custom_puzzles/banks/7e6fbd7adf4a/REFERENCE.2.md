# New Primitive for Set 16 — `infer_dihedral`

## Signature

```text
infer_dihedral(src, dst, candidates=None)
```

## Purpose

Infer which dihedral transform maps one motif or cropped object to another.

Many ARC-style tasks show a before/after pair without naming the transform explicitly. A solver has to recognize whether the change is a rotation, a mirror, a transpose, an anti-transpose, or no transform at all. `infer_dihedral` makes that recognition step explicit instead of burying it inside a larger rule.

## Arguments

- `src`: the source grid or cropped object
- `dst`: the target grid or cropped object
- `candidates`: optional iterable of transform codes to consider; when omitted, search the full dihedral family

## Semantics

Try each allowed transform in a fixed order and return the first one that maps `src` to `dst` exactly:

```text
for code in candidates or FULL_DIHEDRAL_SET:
    if transform(code, src) == dst:
        return code
return None
```

A solver can then feed the returned code into an ordinary transform table.

## Why this helper matters

Without an explicit helper, analogy-style ARC rules often tangle three separate jobs:

1. extracting the objects that matter,
2. recognizing the transform between examples,
3. applying that transform somewhere else.

`infer_dihedral` isolates the second job cleanly. That supports staged solving: first crop the relevant panels, then infer the transform, then apply it.

## Direct uses in this pack

- **E106** — infer the transform from panel A to panel B, then apply it to panel C
- **M106** — do the same after first removing panel frames
- **H106** — infer two independent analogy axes in a 2×2 panel layout

## Related patterns it supports

The same helper naturally extends to:

- command-free analogy transfer,
- transform-class clustering,
- canonical gallery construction,
- and puzzle families where the output depends on recognizing symmetry class before any painting happens.
