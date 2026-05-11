;; ARC Additional Puzzle Bank -- solver-style companion
;;
;; This file is deliberately mixed-mode:
;; - Some rules are close to the minimal local style your current system already uses.
;; - Some rules are helper-dependent sketches for object-heavy tasks.
;;
;; Assumed helper vocabulary for sketches: connected-components, rect-frames,
;; component-size, component-bbox, frame-contains-color?, fill-frame-interiors,
;; crop-to-bbox, find-singleton, cells-of-color, translate-cells, paint-cells,
;; draw-horizontal-run, draw-bars-with-gaps, etc.

;; E1 -- Diagonal Corner Completion
(define rule-e1
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (letrec ((hole?
                   (lambda (r c)
                     (or
                       ;; current cell is NW hole
                       (and (= (safe-at g r c 0) 0)
                            (= (safe-at g r (+ c 1) 0) 3)
                            (= (safe-at g (+ r 1) c 0) 3)
                            (= (safe-at g (+ r 1) (+ c 1) 0) 0))
                       ;; current cell is NE hole
                       (and (= (safe-at g r c 0) 0)
                            (= (safe-at g r (- c 1) 0) 3)
                            (= (safe-at g (+ r 1) c 0) 3)
                            (= (safe-at g (+ r 1) (- c 1) 0) 0))
                       ;; current cell is SW hole
                       (and (= (safe-at g r c 0) 0)
                            (= (safe-at g (- r 1) c 0) 3)
                            (= (safe-at g r (+ c 1) 0) 3)
                            (= (safe-at g (- r 1) (+ c 1) 0) 0))
                       ;; current cell is SE hole
                       (and (= (safe-at g r c 0) 0)
                            (= (safe-at g (- r 1) c 0) 3)
                            (= (safe-at g r (- c 1) 0) 3)
                            (= (safe-at g (- r 1) (- c 1) 0) 0))))))
          (grid-from-fn h w
            (lambda (r c)
              (let ((v (cell-at g r c)))
                (if (and (= v 0) (hole? r c)) 7 v)))))))))

;; E2 -- Diagonal Halo
(define rule-e2
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 0)
                       (or (= (safe-at g (- r 1) (- c 1) 0) 3)
                           (= (safe-at g (- r 1) (+ c 1) 0) 3)
                           (= (safe-at g (+ r 1) (- c 1) 0) 3)
                           (= (safe-at g (+ r 1) (+ c 1) 0) 3)))
                  7
                  v))))))))

;; E3 -- One-Gap Completion
(define rule-e3
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 0)
                       (or (and (= (safe-at g r (- c 1) 0) 4)
                                (= (safe-at g r (+ c 1) 0) 4))
                           (and (= (safe-at g (- r 1) c 0) 4)
                                (= (safe-at g (+ r 1) c 0) 4))))
                  4
                  v))))))))

;; E4 -- Bar Caps
(define rule-e4
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 0)
                       (or
                         ;; left endcap of a run to the right
                         (and (not (= (safe-at g r (- c 1) 0) 6))
                              (= (safe-at g r (+ c 1) 0) 6)
                              (= (safe-at g r (+ c 2) 0) 6))
                         ;; right endcap of a run to the left
                         (and (not (= (safe-at g r (+ c 1) 0) 6))
                              (= (safe-at g r (- c 1) 0) 6)
                              (= (safe-at g r (- c 2) 0) 6))))
                  8
                  v))))))))

;; E5 -- Solid Square Recolor
(define rule-e5
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 5)
                       (or
                         ;; current is NW corner
                         (and (= (safe-at g (+ r 1) c 0) 5)
                              (= (safe-at g r (+ c 1) 0) 5)
                              (= (safe-at g (+ r 1) (+ c 1) 0) 5))
                         ;; current is NE corner
                         (and (= (safe-at g (+ r 1) c 0) 5)
                              (= (safe-at g r (- c 1) 0) 5)
                              (= (safe-at g (+ r 1) (- c 1) 0) 5))
                         ;; current is SW corner
                         (and (= (safe-at g (- r 1) c 0) 5)
                              (= (safe-at g r (+ c 1) 0) 5)
                              (= (safe-at g (- r 1) (+ c 1) 0) 5))
                         ;; current is SE corner
                         (and (= (safe-at g (- r 1) c 0) 5)
                              (= (safe-at g r (- c 1) 0) 5)
                              (= (safe-at g (- r 1) (- c 1) 0) 5))))
                  1
                  v))))))))

;; E6 -- Down-Right Shadow
(define rule-e6
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 0)
                       (= (safe-at g (- r 1) (- c 1) 0) 2))
                  5
                  v))))))))

;; E7 -- Vertical Middle Highlight
(define rule-e7
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 4)
                       (= (safe-at g (- r 1) c 0) 4)
                       (= (safe-at g (+ r 1) c 0) 4))
                  9
                  v))))))))

;; M1 -- Seeded Frame Fill
(define rule-m1
  (rule!
    (lambda (g)
      (let* ((frames (rect-frames g 1))
             (seeded (filter (lambda (fr) (frame-contains-color? g fr 2))
                             frames)))
        (fill-frame-interiors g seeded 4)))))

;; M2 -- Largest 3-Component
(define rule-m2
  (rule!
    (lambda (g)
      (let* ((comps (connected-components g 3))
             (best (largest-component comps)))
        (paint-component g best 8)))))

;; M3 -- Straight Bridge
(define rule-m3
  (rule!
    (lambda (g)
      (let* ((pairs (colors-with-exactly-two-cells g))
             (usable (filter (lambda (entry)
                               (let ((cells (cdr entry)))
                                 (and (aligned-pair? cells)
                                      (clear-corridor? g cells))))
                             pairs)))
        (paint-bridges g usable)))))

;; M4 -- Frame Stripe from External Marker
(define rule-m4
  (rule!
    (lambda (g)
      (let* ((frames (rect-frames g 5))
             (stripes (flatten
                        (map (lambda (fr)
                               (markers->interior-stripes g fr 7))
                             frames))))
        (paint-cells g stripes 3)))))

;; M5 -- Vertical Mirror Divider
(define rule-m5
  (rule!
    (lambda (g)
      (let* ((h (rows g))
             (w (cols g))
             (axis (first-full-col g 9)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (not (= v 0))
                  v
                  (let ((src-c (- (* 2 axis) c))
                        (src (safe-at g r (- (* 2 axis) c) 0)))
                    (if (and (< c w)
                             (>= c 0)
                             (not (= src 0))
                             (not (= src 9)))
                        src
                        0))))))))))

;; M6 -- L-Triomino Filter
(define rule-m6
  (rule!
    (lambda (g)
      (let* ((comps (connected-components g 6))
             (ells  (filter (lambda (comp)
                              (and (= (component-size comp) 3)
                                   (let* ((bb (component-bbox comp))
                                          (bh (bbox-height bb))
                                          (bw (bbox-width bb)))
                                     (and (= bh 2) (= bw 2)))))
                            comps)))
        (paint-components g ells 1)))))

;; M7 -- Crop the Largest Object
(define rule-m7
  (rule!
    (lambda (g)
      (let* ((objs (nonzero-components-anycolor g))
             (best (largest-component objs))
             (bb   (component-bbox best)))
        (crop-to-bbox g bb)))))

;; H1 -- Translate by Anchor Vector
(define rule-h1
  (rule!
    (lambda (g)
      (let* ((p1  (find-singleton g 1))
             (p2  (find-singleton g 2))
             (obj (cells-of-color g 3))
             (dr  (- (car p2) (car p1)))
             (dc  (- (cdr p2) (cdr p1)))
             (dst (translate-cells obj dr dc)))
        (paint-cells g dst 8)))))

;; H2 -- Prototype Stamp from Framed Template
(define rule-h2
  (rule!
    (lambda (g)
      (let* ((frames   (rect-frames g 1))
             (source   (first (filter (lambda (fr) (frame-contains-color? g fr 4))
                                      frames)))
             (pattern  (frame-interior-bitmap g source 4))
             (seeds    (cells-of-color g 7)))
        (stamp-patterns g pattern seeds 8)))))

;; H3 -- Axis-Chooser Reflection
(define rule-h3
  (rule!
    (lambda (g)
      (let* ((h (rows g))
             (w (cols g))
             (axis-r (first-full-row g 9))
             (axis-c (first-full-col g 9)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (not (= v 0))
                  v
                  (cond
                    ((not (false? axis-r))
                     (let ((src (safe-at g (- (* 2 axis-r) r) c 0)))
                       (if (and (not (= src 0)) (not (= src 9))) src 0)))
                    ((not (false? axis-c))
                     (let ((src (safe-at g r (- (* 2 axis-c) c) 0)))
                       (if (and (not (= src 0)) (not (= src 9))) src 0)))
                    (else 0))))))))))

;; H4 -- Component Count Bar
(define rule-h4
  (rule!
    (lambda (g)
      (let* ((n  (length (connected-components g 6)))
             (p2 (find-singleton g 2)))
        (draw-horizontal-run g (car p2) (+ (cdr p2) 1) n 3)))))

;; H5 -- Smallest and Largest Frame Fill
(define rule-h5
  (rule!
    (lambda (g)
      (let* ((frames (rect-frames g 4))
             (small  (smallest-frame-by-interior-area frames))
             (large  (largest-frame-by-interior-area frames)))
        (fill-frame-interiors
          (fill-frame-interiors g (list small) 2)
          (list large)
          8)))))

;; H6 -- Deepest Seeded Frame
(define rule-h6
  (rule!
    (lambda (g)
      (let* ((frames  (rect-frames g 1))
             (seeded  (filter (lambda (fr) (frame-contains-color? g fr 2)) frames))
             (deepest (filter (lambda (fr)
                                (not (ormap (lambda (other)
                                              (and (not (equal? fr other))
                                                   (interior-contains? fr other)))
                                            seeded)))
                              seeded)))
        (fill-frame-interiors g deepest 3)))))

;; H7 -- Sorted Component-Size Bars
(define rule-h7
  (rule!
    (lambda (g)
      (let* ((sizes (sort-desc (map component-size (connected-components g 6))))
             (p2    (find-singleton g 2)))
        (draw-bars-with-gaps g (car p2) (+ (cdr p2) 1) sizes 3)))))

