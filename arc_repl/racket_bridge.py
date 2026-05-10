"""
RacketBridge — persistent Racket subprocess for evaluating S-expressions.

Replaces the Python-based evaluator with real Racket (Chez Scheme backend).
Communicates via stdin/stdout with JSON-encoded results.
"""

import subprocess
import json
import os
import threading
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_PRELUDE_PATH = os.path.join(_HERE, "racket_prelude", "arc-prelude.rkt")
_RACKET = os.environ.get("RACKET_PATH", "racket")

# Boot script: load prelude, then enter a read-eval-write-json loop.
# Protocol: one S-expression per line in, one JSON line out.
_BOOT_SCRIPT = r"""
(require json racket/list racket/string racket/match racket/dict
         racket/set racket/vector racket/format racket/port)

;; Load the ARC prelude with all grid primitives
;; Prelude path is passed as first line of stdin
(define prelude-path (read-line))

;; Set up a namespace with full Racket + prelude bindings
(define ns (make-base-namespace))
(eval '(require racket) ns)
(eval '(require json) ns)
(eval `(require (file ,prelude-path)) ns)
;; Also load heightmap into the namespace
;; Load additional prelude modules into the namespace
(define prelude-dir (path->string (simplify-path
  (build-path (string->path prelude-path) 'up))))
(for-each (lambda (mod)
  (define mod-path (string-append prelude-dir "/" mod))
  (when (file-exists? mod-path)
    (eval `(require (file ,mod-path)) ns)))
  '("heightmap.rkt" "layers.rkt"))
(current-namespace ns)

;; Override operators for ARC compatibility
;; All overrides defined as Racket code eval'd in the namespace
;; Override operators — each eval'd sequentially so earlier defs are visible
(eval '(begin
  (define = arc=)
  (define != arc!=)
  (define / arc/)
  (define range safe-range)

  ;; Safe arithmetic: treat #f as 0
  (define (safe-num x) (if (eq? x #f) 0 x))
  (define orig-+ +) (define orig-- -) (define orig-* *)
  (define orig-< <) (define orig-> >) (define orig-<= <=) (define orig->= >=)
  (define (+ . args) (apply orig-+ (map safe-num args)))
  (define (- . args) (apply orig-- (map safe-num args)))
  (define (* . args) (apply orig-* (map safe-num args)))
  (define (< . args) (apply orig-< (map safe-num args)))
  (define (> . args) (apply orig-> (map safe-num args)))
  (define (<= . args) (apply orig-<= (map safe-num args)))
  (define (>= . args) (apply orig->= (map safe-num args)))

  ;; Safe list accessors: handle #f and short lists
  (define orig-list-ref list-ref)
  (define (safe-idx? idx) (and (integer? idx) (orig->= idx 0)))
  (define (list-ref lst idx)
    (cond [(not (safe-idx? idx)) #f]
          [(orig->= idx (length lst)) #f]
          [else (orig-list-ref lst idx)]))
  (define (nth lst idx) (list-ref lst idx))
  (define (first x) (if (and (list? x) (not (empty? x))) (car x) #f))
  (define (second x) (if (and (list? x) (orig->= (length x) 2)) (list-ref x 1) #f))
  (define (third x) (if (and (list? x) (orig->= (length x) 3)) (list-ref x 2) #f))
  (define (fourth x) (if (and (list? x) (orig->= (length x) 4)) (list-ref x 3) #f))
  (define (last x) (if (and (list? x) (not (empty? x)))
    (orig-list-ref x (sub1 (length x))) #f))
) ns)

;; Load generated puzzle-bank helpers after the ARC compatibility overrides.
;; These are plain top-level forms, not a module, so helper references bind to
;; the same namespace as compacted bank rule bodies.
(define bank-helpers-path (string-append prelude-dir "/bank-helpers.rkt"))
(when (file-exists? bank-helpers-path)
  (call-with-input-file bank-helpers-path
    (lambda (in)
      (let loop ()
        (define form (read in))
        (unless (eof-object? form)
          (eval form ns)
          (loop))))))

;; Serialize a Racket value to a JSON-friendly structure
(define (serialize v)
  (cond
    [(void? v) 'null]
    [(boolean? v) v]
    [(exact-integer? v) v]
    [(number? v) (inexact->exact (round (* v 1000000.0)))]  ;; float as scaled int
    [(string? v) v]
    [(null? v) '()]
    [(pair? v)
     (if (list? v)
         (map serialize v)
         (list (serialize (car v)) (serialize (cdr v))))]
    [(hash? v)
     (for/hasheq ([(k val) (in-hash v)])
       (values (if (number? k) (~a k) k)
               (serialize val)))]
    [(procedure? v) (hasheq 'type "procedure" 'name (~a v))]
    [(vector? v) (map serialize (vector->list v))]
    [else (~a v)]))

;; Main REPL loop: read line, eval, write JSON, repeat
(let loop ()
  (define line (read-line))
  (unless (eof-object? line)
    (define trimmed (string-trim line))
    (cond
      [(string=? trimmed "") (write-json 'null) (newline) (flush-output)]
      [else
       (with-handlers ([exn:fail? (lambda (e)
                          (write-json (hasheq 'error (exn-message e)))
                          (newline) (flush-output))])
         (define expr (read (open-input-string trimmed)))
         (define result (eval expr))
         (write-json (serialize result))
         (newline)
         (flush-output))])
    (loop)))
"""


class RacketBridgeError(Exception):
    pass


class RacketBridge:
    """Manages a persistent Racket subprocess for S-expression evaluation."""

    def __init__(self, prelude_path=None, timeout=10.0):
        self.prelude_path = prelude_path or _PRELUDE_PATH
        self.timeout = timeout
        self._proc = None
        self._start()

    def _start(self):
        """Spawn the Racket subprocess."""
        # Write boot script to temp file (can't use #lang with -e)
        import tempfile
        self._boot_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.rkt', delete=False, prefix='arc_boot_')
        self._boot_file.write('#lang racket\n')
        self._boot_file.write(_BOOT_SCRIPT)
        self._boot_file.flush()
        self._boot_file.close()

        self._proc = subprocess.Popen(
            [_RACKET, self._boot_file.name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # line-buffered
        )
        # Send prelude path as first line
        self._proc.stdin.write(self.prelude_path + "\n")
        self._proc.stdin.flush()
        # Wait a moment for prelude to load
        import time
        time.sleep(0.5)

    def alive(self):
        return self._proc is not None and self._proc.poll() is None

    def eval_text(self, sexpr: str) -> any:
        """Send an S-expression string to Racket, return the parsed result.

        Raises RacketBridgeError on timeout, subprocess crash, or Racket error.
        """
        if not self.alive():
            raise RacketBridgeError("Racket process is not running")

        # Flatten to single line (Racket reads one line at a time)
        line = sexpr.replace("\n", " ").strip()
        if not line:
            return None

        try:
            self._proc.stdin.write(line + "\n")
            self._proc.stdin.flush()
        except (BrokenPipeError, OSError) as e:
            stderr = self._proc.stderr.read() if self._proc.stderr else ""
            raise RacketBridgeError(f"Failed to send to Racket: {e}\nstderr: {stderr}")

        # Read response with timeout
        result_line = self._read_line_timeout()
        if result_line is None:
            raise RacketBridgeError(f"Racket timed out ({self.timeout}s) evaluating: {line[:200]}")

        # Parse JSON response
        try:
            result = json.loads(result_line)
        except json.JSONDecodeError:
            raise RacketBridgeError(f"Invalid JSON from Racket: {result_line[:500]}")

        # Check for error
        if isinstance(result, dict) and "error" in result:
            raise RacketBridgeError(f"Racket error: {result['error']}")

        return result

    def _read_line_timeout(self):
        """Read one line from stdout with timeout."""
        result = [None]

        def reader():
            try:
                result[0] = self._proc.stdout.readline()
            except Exception:
                pass

        t = threading.Thread(target=reader, daemon=True)
        t.start()
        t.join(timeout=self.timeout)

        if t.is_alive():
            # Timeout — kill and restart
            self._proc.kill()
            self._proc = None
            return None

        line = result[0]
        if line is None or line == "":
            # Process died
            stderr = ""
            try:
                stderr = self._proc.stderr.read()
            except Exception:
                pass
            self._proc = None
            raise RacketBridgeError(f"Racket process died. stderr: {stderr[:1000]}")

        return line.strip()

    def define_grid(self, name: str, grid_data: list):
        """Define a grid variable in Racket's namespace."""
        # Serialize grid as a Racket literal: '((1 0 2) (3 4 5))
        rows = " ".join(
            "(" + " ".join(str(v) for v in row) + ")"
            for row in grid_data
        )
        self.eval_text(f"(define {name} '({rows}))")

    def define_value(self, name: str, value):
        """Define a simple value in Racket's namespace."""
        if isinstance(value, bool):
            rkt = "#t" if value else "#f"
        elif isinstance(value, int):
            rkt = str(value)
        elif isinstance(value, float):
            rkt = str(value)
        elif isinstance(value, str):
            rkt = f'"{value}"'
        elif isinstance(value, list):
            rkt = "'" + self._serialize_list(value)
        elif value is None:
            rkt = "'()"
        else:
            rkt = f"'{value}"
        self.eval_text(f"(define {name} {rkt})")

    def _serialize_list(self, lst):
        """Serialize a Python list as a Racket list literal."""
        parts = []
        for item in lst:
            if isinstance(item, list):
                parts.append(self._serialize_list(item))
            elif isinstance(item, bool):
                parts.append("#t" if item else "#f")
            elif isinstance(item, (int, float)):
                parts.append(str(item))
            elif isinstance(item, str):
                parts.append(f'"{item}"')
            else:
                parts.append(str(item))
        return "(" + " ".join(parts) + ")"

    def shutdown(self):
        """Cleanly shut down the Racket subprocess."""
        if self._proc is not None:
            try:
                self._proc.stdin.close()
                self._proc.wait(timeout=2)
            except Exception:
                self._proc.kill()
            self._proc = None

    def __del__(self):
        self.shutdown()
