# Samples

Hand-picked input → output pairs from the corpus, rendered with the standard ARC color palette.

Each pair is one `(input, output)` instance the generator produced; the rule was applied via the Racket runner. Re-running `python3 scripts/build_samples.py` re-rolls them with the same seeds.

## `ecc04b33119c`

**Rule:** Tile 3×3 alternating original / LR-mirror by row block

![ecc04b33119c train 0](samples/ecc04b33119c/train_0.png)

![ecc04b33119c train 1](samples/ecc04b33119c/train_1.png)

*test instance:*

![ecc04b33119c test 0](samples/ecc04b33119c/test_0.png)

---

## `c4ab07496ad4`

**Rule:** Small shape determines big shape's color: plus→2, bottom-full→3, top-full→7

![c4ab07496ad4 train 0](samples/c4ab07496ad4/train_0.png)

![c4ab07496ad4 train 1](samples/c4ab07496ad4/train_1.png)

*test instance:*

![c4ab07496ad4 test 0](samples/c4ab07496ad4/test_0.png)

---

## `ad5998ad11d6`

**Rule:** Fill all enclosed regions with yellow(4)

![ad5998ad11d6 train 0](samples/ad5998ad11d6/train_0.png)

![ad5998ad11d6 train 1](samples/ad5998ad11d6/train_1.png)

*test instance:*

![ad5998ad11d6 test 0](samples/ad5998ad11d6/test_0.png)

---

## `a9f315ca9cc7`

**Rule:** Self-tile 3×3: each cell of the input determines whether that tile-position copies the input or stays blank

![a9f315ca9cc7 train 0](samples/a9f315ca9cc7/train_0.png)

![a9f315ca9cc7 train 1](samples/a9f315ca9cc7/train_1.png)

*test instance:*

![a9f315ca9cc7 test 0](samples/a9f315ca9cc7/test_0.png)

---

## `c739fcbc6cbd`

**Rule:** Repeat a vertical color marker across all columns at the same spacing

![c739fcbc6cbd train 0](samples/c739fcbc6cbd/train_0.png)

![c739fcbc6cbd train 1](samples/c739fcbc6cbd/train_1.png)

*test instance:*

![c739fcbc6cbd test 0](samples/c739fcbc6cbd/test_0.png)

---


To regenerate: `python3 scripts/build_samples.py`