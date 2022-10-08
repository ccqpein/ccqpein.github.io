---
layout: post
title: A tiny compare and optimize of my tiny project
---

I am trying to learn OCaml several weeks ago. My personal hobbits is writing a tiny project for fun with new language which I am learning. So, for OCaml, I wanna to rewrite my old code-it-later project. At beginning, I just want to practice, then I get some experiments. 

## What is code-it-later

code-it-later is the project I had used to practice my Clojure skill in 2017. I use it almost everyday. Especially when I restart a project after a period of time, code-it-later help me back to where I stopped. 

# Other version

## OCaml version

### Why

My friend recommend me that ocaml, he said it is fast, high expression, and not hard to learn for me because I had learned Haskell before. After read language specialts, I start to find some toy project to write. Then I notice my code-it-later looks a bit slow (actually, it is not, let's talk it after), I want re-write it with ocaml.

### How is going on ###

I use same design and same logic to rewrite code-it-later, and everything is going well. it is not very hard and truly neat to write it, except need to handle some `opam` issues. 

I test with my test cases and my other source code, it is really fast. 

## Haskell version ##

### Why

After OCaml version, I notice I can use concurrency to make it runs faster. I searched, and found ocaml is not very convenient to concurrency or parallel. Even I use third part package to make it concurrency, but I still need mutil-core version ocaml to start mutil-cpu-core use.

Then I think about Haskell, I remember I have read articles talk about STM in Haskell, that's means Haskell should have ability to concurrency. Then I did some research about how-to use concurrency/parallel/mutil-cpu in Haskell. It is a lot read for my poor english but it is worth. Then I rewrite code-it-later in Haskell, and try to make it concurrency.

### How is going on

Generally, it is ok. I finally choice `threads` package. Because I need main thread block until all threads done their jobs. And this package make it easier to use.

#### Concurrency ####

Haskell give a neat way to active mutil-core mode. But first, I need change my code. I play a trick in this requirements. Generally, code-it-later do a lot IO operations. It need read files, and parse them line by line. 

At first, I want to let reading lines function be concurrent. But looks like granularity is too fine. Beside, reading lines function already handle IO monad inside. Depend on my poor design, there should be a lot work have be done if I want they become concurrent.

So I roughly separate all files list to 4 parts. Each of them be sent to one thread handler. 

```haskell
(_,wait1) <- Thread.forkIO $ format_print_out (iter_all_files a1 func)
(_,wait2) <- Thread.forkIO $ format_print_out (iter_all_files a2 func)
(_,wait3) <- Thread.forkIO $ format_print_out (iter_all_files b1 func)
(_,wait4) <- Thread.forkIO $ format_print_out (iter_all_files b2 func)
_ <- wait1
_ <- wait2
_ <- wait3
_ <- wait4
	
return ()
```

#### Mutil-core use ####

There are another things I need to do. If a haskell application need mutil-core running, I need give additional options arguments for compiling and running. Fortunately, I just need to add `ghc-options: -threaded -rtsopts` at the end of `.cabal` file. 

These two options tell ghc I need mutil-threads support, `-threaded` active mutil-threads and `-rtsopts` active **runtime system** options support. Then, I need run with `+RTS -N2 -RTS` to let my code-it-later run exactly on two cores (the number after N). 

#### Parallel ####

Add threads support with running with mutil-cores, code-it-later is concurrent now. In this case, four threads running on 2 cores, managed by runtime and system. Then, I want to try parallel too. 

I tried, after several readings, I make data deriving `Generic`. Change ruler of evaluation, and all other detail operations. Finally, I do not use parallel version, because after all operations, program even slower (sarcastic right?).

Looks like haskell manage threads on different cores are much better than me. 

# Compare different versions

After these three versions, I try to compare different versions efficiency.

## Without concurrency ##

Firstly, I compare one thread version. It is not totally "one thread" because clojure (standalone jar) running on two core automatically. 

For small input, clojure version is slowest, and not matter how small the input is, clojure still need at least 2 seconds (I guess because JVM need time to startup). Haskell and ocaml looks like as fast as each other.

For big input, clojure always fastest version, and ocaml version is a bit slower than haskell version.

## Optimize haskell version ##

After change haskell version to concurrency version, for small input, haskell version still fast. The major part I wanna improve is for large input. For large input, haskell sort of as fast as clojure, with less CPU and memory use. 

for special test case, I get these results:

```
clojure version: cost 2.2 second, ~200% cpu cost.
ocaml version: cost 2.2 second, 100% cpu cost.
this haskell version: cost 0.6 seconds, 140% cpu cost.
```


