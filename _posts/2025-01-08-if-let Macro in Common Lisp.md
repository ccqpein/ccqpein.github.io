---
layout: post
title: if-let Macro in Common Lisp
---

I recently came across someone using the macro `if-let`. I was guessing its purpose is similar to the `if let` construct in Rust:

```rust
let a: Option<_>;
if let Some(x) = a {
    ...
}
```

I actually really need something like this. Especially when working on this year's Advent of Code (AOC), where you often encounter situations like this:

```lisp
(if (gethash a table) 
    (setf something (gethash a table)) 
    (print b))
```

Here, I kind of need to introduce a `let` to avoid calling `gethash` twice:

```lisp
(let ((v (gethash a table)))
  (if v
      (setf something v)
      (print b)))
```

I did a bit of searching and found thatone of the most popular Common Lisp libraries, `alexandria`, already has this feature. So I decided to run some tests with this macro and its sibling, `when-let*`.

---

## Playing Around ##

**Basic example:**

```lisp
(ql:quickload "alexandria")

(defun provide-value ()
  (if (zerop (mod (random 2) 2))
      t
      nil))

(defun test0 ()
  (alexandria:if-let (x (provide-value))
    (format t "x has value")
    (format t "x has no value")))
```

**Multiple bindings:**

```lisp
(defun test1 ()
  (alexandria:if-let
      ((x (provide-value))
       (y (provide-value)))
    (format t "x and y have values")
    (format t "x = ~a, y = ~a" x y)))
```

This requires *all* bindings to have values; otherwise, it won’t execute the `then` statement.

---

## How About `when-let`? ##

```lisp
(defun test2 ()
  (alexandria:when-let (x (provide-value))
    (format t "x has a value~%")
    (format t "Running code with x having a value")))
```

---

## What About `let*`? ##

Common Lisp already has `let*`, which allows you to define values that depend on previously defined ones. I couldn’t find`if-let*`, but I did discover `when-let*`.

```lisp
;; (defun test3 ()
;;   (alexandria:if-let* ;; This won't work; there is no `if-let*`
;;       ((x (provide-value))
;;        (y (provide-value))
;;        (yy y))
;;     (format t "x and y have values")
;;     (format t "x = ~a, y = ~a" x y)))

(defun test4 ()
  (alexandria:when-let*
      ((x (provide-value))
       (y (provide-value))
       (yy y))
    (format t "x has value ~a~%" x)
    (format t "y has value ~a~%" y)
    (format t "Running with all values present, yy = ~a~%" yy)))
```

---

## Wrapping Up ##

Back to the initial example, I can now write:

```lisp
(if-let ((v (gethash a table)))
  (setf something v)
  (print b))
```

Pretty nice, right?
