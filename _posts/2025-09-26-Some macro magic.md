---
layout: post
title: Some macro magic
---

Days ago, my friend sent me a [question](https://leetcode.com/problems/find-the-k-th-character-in-string-game-i/description/) from LeetCode. Her solution is pretty tricky; it generates the string during compile time and directly retrieves the answer from it.

I was impressed by how tricky it is. This is because LeetCode only counts the runtime of the puzzle solution, not the compile time. So, for some languages (she used C++), it can brute-force the result, making the runtime extremely fast.

Because I don't know C++, but I know some other languages can do this too. For example, Rust (proc macro) and Common Lisp (macro).

## Rust version

I have worked with macros before in [cl-format-rs](https://github.com/ccqpein/cl-format-rs), so this wasn't too difficult for me.

```rust
extern crate proc_macro;

use proc_macro::TokenStream;
use syn::{Expr, ExprLit, ExprTuple, Lit, parse_macro_input};

#[proc_macro]
pub fn make_answer(item: TokenStream) -> TokenStream {
    let expr: Expr = parse_macro_input!(item as Expr);

    let mut string_value: Option<String> = None;
    let mut int_value: Option<i64> = None;

    let Expr::Tuple(ExprTuple { elems, .. }) = expr else {
        panic!()
    };

    for elem in elems {
        match elem {
            Expr::Lit(ExprLit { lit, .. }) => {
                match lit {
                    Lit::Str(lit_str) => {
                        if string_value.is_none() {
                            string_value = Some(lit_str.value());
                        } else {
                        }
                    }
                    Lit::Int(lit_int) => {
                        if int_value.is_none() {
                            match lit_int.base10_parse::<i64>() {
                                Ok(val) => int_value = Some(val),
                                Err(e) => {
                                    return syn::Error::new_spanned(
                                        lit_int,
                                        format!("failed to parse integer literal: {}", e),
                                    )
                                    .to_compile_error()
                                    .into();
                                }
                            }
                        } else {
                        }
                    }
                    _ => {}
                }
            }
            _ => {}
        }
    }

    //println!("{:?}, {:?}", string_value, int_value);
    let mut ss = string_value.unwrap();
    let intt = int_value.unwrap() as usize;
    for _ in 0..intt {
        ss = one_round(ss);
        if ss.len() >= intt {
            return format!("const all: &str = \"{}\";", ss).parse().unwrap();
        }
    }

    r#"const all: &str = "";"#.parse().unwrap()
}

fn one_round(s: String) -> String {
    let mut res = vec![];
    for c in s.chars() {
        res.push(c);
        res.push(match c {
            'a'..='y' => (c as u8 + 1) as char,
            'z' => 'a',
            _ => unreachable!(),
        })
    }
    String::from_iter(res)
}
```

It basically just brute-forces the string and assigns it to a constant variable.

Then, in `main.rs`:

```rust
make_answer!(("a", 50000000));

fn main() {
    //make_answer!(("a", 0));
    //println!("{}", answer());
    println!("{}", all.get(49999999..50000000).unwrap());
}
```


## Lisp version

The Lisp version is even simpler:

```lisp
(defmacro alphab (c)
  (let* ((x (concatenate 'list "abcdefghijklmnopqrstuvwxyz"))
         (y (append (subseq x 1) (list (first x)))))
    `(case ,c
       ,@(loop for xx in x
               for yy in y
               collect (list xx yy)))))

(eval-when (:execute :load-toplevel :compile-toplevel)
  (defun one-round (s)
    (loop for c in (concatenate 'list s)
          collect c into res
          collect (alphab c) into res
          finally (return (concatenate 'string res)))))

(defmacro all (k)
  (loop with res = "a"
        for i from 1 to k
        do (setf res (one-round res))
        finally (return res)))

(defun main ()
  (assert (char= (nth 5 (all 5)) #\b))
  (assert (char= (nth 10 (all 10)) #\c))
  (assert (char= (nth 10 (all 30)) #\c))
  ;;(assert (char= (nth 500 (all 500)) #\h))
  ;;(assert (char= (nth 5000 (all 1000)) #\h))
  )
```

The only thing to worry about is the `eval-when` block. It needs to compile at the top-level so that the `all` macro can call the function defined within it.

## Performance

This is the fun part I wanted to test. Because almost all the work is done during compile time, the compile time should increase with the number of arguments.

**rust:**

| compile time | arguments number |
|--------------|------------------|
| 0.21s        | 500000           |
| 0.55s        | 5000000          |
| 3.18s        | 50000000         |



0.21s 500000
0.55s 5000000
3.18s 50000000

**lisp:**

`(all 10)`

```
; compilation finished in 0:00:00.020
Evaluation took:
  0.020 seconds of real time
  0.018004 seconds of total run time (0.015299 user, 0.002705 system)
  90.00% CPU
  34 forms interpreted
  91 lambdas converted
  5 page faults
  4,886,592 bytes consed
```

`(all 500)`

`memory failed`

`(all 100)`

`memory failed`

`(all 20)`

```
; compilation finished in 0:00:00.101
Evaluation took:
  0.101 seconds of real time
  0.101081 seconds of total run time (0.091436 user, 0.009645 system)
  100.00% CPU
  34 forms interpreted
  91 lambdas converted
  5 page faults
  181,083,424 bytes consed
```
