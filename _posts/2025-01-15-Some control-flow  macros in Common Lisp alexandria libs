---
layout: post
title: Some control-flow  macros in Common Lisp alexandria libs
---

[Previous post](https://ccqpein.me/if-let-Macro-in-Common-Lisp/) recorded my curiosity about the `if-let` macro in `alexandria`.

Recently, I stumbled upon another file, `control-flow.lisp`, and became curious about what’s inside. Once again, I played around with it a bit to explore its potential for future use.

## `nth-value-or`

```lisp
(alexandria:nth-value-or 1
    (values 0 nil 2)
    (values 0 1 3)
    (values 0 1 4))
```

This code will return `(values 0 1 3)` because `(nth 1 (multiple-value-list (values 0 1 3)))` is not `nil`.

## `xor`

This one is a bit weird:

```lisp
(assert (equal '(nil nil) (multiple-value-list (alexandria:xor 1 2))))
(assert (equal '(2 t) (multiple-value-list (alexandria:xor nil 2))))
(assert (equal '(1 t) (multiple-value-list (alexandria:xor 1 nil nil))))
(assert (equal '(nil nil) (multiple-value-list (alexandria:xor 1 2 3))))
(assert (equal '(3 t) (multiple-value-list (alexandria:xor nil nil 3 nil))))
(assert (equal '(nil nil) (multiple-value-list (alexandria:xor nil nil 3 4))))
(assert (equal '(nil nil) (multiple-value-list (alexandria:xor nil 2 3 4))))
```

It looks like it keeps comparing pairs of values until it finds a pair that evaluates to `(t nil)` and then returns the corresponding value.

## `switch`

This one has a couple of siblings: `eswitch` and `cswitch`.

```lisp
(alexandria:switch (10 :test 'equal)
  (1 (format t "1") 2)
  (2 (format t "2") 3)
  (3 (format t "3") 4)
  ((1+ 9) (format t "match") 11))
```

At first, I thought it might behave like Go’s `switch`, but it seems more like a supercharged `cond`.
