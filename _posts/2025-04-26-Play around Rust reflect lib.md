---
layout: post
title: Playing around with the Rust reflect lib
---

Days ago, I noticed an interesting lib called [reflect](https://github.com/dtolnay/reflect). It looks like it's a sort of macro writing helper lib. Macros are cool, especially in Common Lisp. Rust macros can also bring some fun, but to be honest, they aren't easy to write. (This is the [repo](https://github.com/ccqpein/cl-format-rs) of a macro I wrote in Rust).

So, I'm curious how to use this repo.

## Run some demos ##

I have to be honest that I don't really understand the README of the repo. So I found the [tests/debug](https://github.com/dtolnay/reflect/tree/master/tests/debug) directory and tried to study from there.

My first question was, what is `reflect::library!`? I used `cargo expand` on it, but that was actually a bit misleading. Eventually, I went back to the literal meaning and realized that [`extern crate`](https://github.com/dtolnay/reflect/blob/e962d3cbafdabb5b89204aa329f97f5a480a6945/tests/debug/mod.rs#L11) seems to provide a fake interface for future usage.

In `mod.rs`, I found that [`derive`](https://github.com/dtolnay/reflect/blob/e962d3cbafdabb5b89204aa329f97f5a480a6945/tests/debug/mod.rs#L33C8-L33C14) is used in the test files by checking the expanded result.

So, I did the same thing, changing `Debug` to [`MyDebug`](https://github.com/ccqpein/garage/blob/69f8ad278f1418ab1b5c0ee9231a1b91c1b3dfe0/rusty/reflect-demo/macro-demo/src/lib.rs#L288).

After copying the result from the repo's test file, [it](https://github.com/ccqpein/garage/blob/69f8ad278f1418ab1b5c0ee9231a1b91c1b3dfe0/rusty/reflect-demo/macro-demo/src/main.rs#L48) returned the failed result, as I expected:

```
assertion `left == right` failed
  left: "impl :: std :: fmt :: MyDebug for Point { fn fmt (& self , __arg0 : & mut :: std :: fmt :: Formatter) -> :: std :: fmt :: Result { let __v0 = self ; let __v1 = __arg0 ; let __v3 = & __v0 . x ; let __v4 = & __v0 . y ; let mut __v5 = :: std :: fmt :: Formatter :: debug_struct (__v1 , \"Point\") ; let __v6 = & mut __v5 ; let _ = :: std :: fmt :: DebugStruct :: field (__v6 , \"x\" , __v3) ; let _ = :: std :: fmt :: DebugStruct :: field (__v6 , \"y\" , __v4) ; let __v11 = :: std :: fmt :: DebugStruct :: finish (__v6) ; __v11 } }"
 right: "impl :: std :: fmt :: Debug for Point { fn fmt (& self , __arg0 : & mut :: std :: fmt :: Formatter) -> :: std :: fmt :: Result { let __v0 = self ; let __v1 = __arg0 ; let __v3 = & __v0 . x ; let __v4 = & __v0 . y ; let mut __v5 = :: std :: fmt :: Formatter :: debug_struct (__v1 , \"Point\") ; let __v6 = & mut __v5 ; let _ = :: std :: fmt :: DebugStruct :: field (__v6 , \"x\" , __v3) ; let _ = :: std :: fmt :: DebugStruct :: field (__v6 , \"y\" , __v4) ; let __v11 = :: std :: fmt :: DebugStruct :: finish (__v6) ; __v11 } }"
```

This means that `MyDebug` truly affects `derive`.

## Make it derivable ##

Now that I understand what it's doing, I'm going to try to make it derivable.

First, I uncommented this [block](https://github.com/ccqpein/garage/blob/095b54ef68c4a71ad50413ecc2c6023d0d1bf987/rusty/reflect-demo/macro-demo/src/lib.rs#L355) and needed to comment out the `derive` function above.

Then, I used it [here](https://github.com/ccqpein/garage/blob/095b54ef68c4a71ad50413ecc2c6023d0d1bf987/rusty/reflect-demo/usage-demo/src/main.rs#L3). The compiler gave me the error that it couldn't find `MyDebug` in `std::fmt`.

Then, I commented out `MyDebug` and put back the real `Debug` in `extern crate` [here](https://github.com/ccqpein/garage/blob/095b54ef68c4a71ad50413ecc2c6023d0d1bf987/rusty/reflect-demo/macro-demo/src/lib.rs#L288-L294). And it works now.

## Next Step ##

I am thinking of re-writing the [cl-format-macro](https://github.com/ccqpein/cl-format-rs/blob/90e3f5dd26cfeaa697f2c81fecccf8b1c576d0ee/cl-format-macros/src/lib.rs#L90) with this reflect lib.

## Conclusion ##

First, the biggest question was what `reflect::library!` does. After understanding that it's some kind of header file/golang interface, everything is much cleaner.

Second, proc macros are always fun to me because they require a higher level of thinking about the language. But I prefer Common Lisp macros.
