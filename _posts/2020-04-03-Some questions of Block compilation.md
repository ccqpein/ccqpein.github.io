---
layout: post
title: Some questions of SBCL block compilation
---

Several weeks ago, SBCL 2.0.2 updated with a "new" feature called `Block Compilation`. This is the first time I hear this term, I go collect some information of this new feature and I found this [article](https://mstmetent.blogspot.com/2020/02/block-compilation-fresh-in-sbcl-202.html). 

# Questions 

After read this article I have several questions:

+ **If I enable this optimization, do I lost the ability of redefine the function**

+ **What are the differences between this optimization and `inline`**

+ **How faster this optimization can achieve**

# Verification

Let me verify them one by one

-------------

> If I enable this optimization, do I lost the ability of redefine the function

The answer is yes I can.

```lisp
(defun foo (x y)
  (bar x y))

(defun bar (x y)
  (+ x y))
```

Then I compile whole file and load it in repl:

```lisp
(compile-file "/Users/BC.lisp" :block-compile t :entry-points nil :output-file "/Users/BC.fasl")

(load "/Users/BC.fasl")

(foo 1 1) ;; => 2
```

Then I redefine `bar` function:

```lisp
(defun bar () (print "a"))

(foo 1 1) ;; => 2
(bar) ;; => "a"
```

So I still have ability to redefine function `bar`, but even `foo` call `bar`, the `foo`'s behavior hasn't been changed because `bar` be redefined.

How about I don't enable `Block compilation`? 

```lisp
(compile-file "/Users/BC.lisp" :block-compile nil :entry-points nil :output-file "/Users/BC.fasl") ;; turn off Block compilation

(load "/Users/BC.fasl")

(foo 1 1) ;; => 2

(defun bar () (print "a")) ;; redefine bar

(foo 1 1) ;; ERROR
; Evaluation aborted on #<SB-INT:SIMPLE-PROGRAM-ERROR "invalid number of arguments: ~S" {1002751533}>.
```

As we can see, if I turn off `Block compilation`, each time I call `foo`, `foo` is gonna to call `bar` inside. So if I redefine `bar`, `foo`'s behavior has been changed by my redefinition.

----------------

> What are the differences between this optimization and `inline`

I asked this question on SO, here is the [post](https://stackoverflow.com/questions/60749799/whats-the-differences-from-inline-and-block-compilation-of-sbcl)

------------------

> How faster this optimization can achieve

I always use some stupid way to test productivity -- `time` function. So, I use it again:

```lisp
;;; new file
(defun foo (x y z)
  (bar x y z))

(defun bar (x y z)
  (max x y z))
```

Same, compile and load it:

```
(compile-file "/Users/BC.lisp" :block-compile nil :entry-points nil :output-file "/Users/BC.fasl") ;; turn off Block compilation

(load "/Users/BC.fasl")

(time (loop repeat 3000000 do (foo 1 2 3))) ;; run 3 millions times
```

Then, I get the result:

```
Evaluation took:
  0.040 seconds of real time
  0.040597 seconds of total run time (0.040512 user, 0.000085 system)
  102.50% CPU
  117,978,902 processor cycles
  0 bytes consed
```

Next, do same thing but turn on Block compilation this time:

```
(compile-file "/Users/BC.lisp" :block-compile t :entry-points nil :output-file "/Users/BC.fasl")

(load "/Users/BC.fasl")

(time (loop repeat 3000000 do (foo 1 2 3)))
```

This time, the answer is

```
Evaluation took:
  0.037 seconds of real time
  0.037057 seconds of total run time (0.036985 user, 0.000072 system)
  100.00% CPU
  107,609,083 processor cycles
  0 bytes consed
```

Well, it just a little bit faster. I guess if my function is more complex, it should be much faster than just `max` function.


