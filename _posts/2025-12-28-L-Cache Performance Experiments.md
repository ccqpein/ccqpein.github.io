---
layout: post
title: L-Cache Performance Experiments
---

A few days ago, I read `Thoughts on Performance Hints from Jeff` and wrote a [blog post](https://ccqpein.me/Thoughts-of-Performance-Hints-from-Jeff/) about it.

One specific tip from those hints that I wanted to play around with is L-Cache performance.

I’ve read many articles about L-Cache, but I’ve never actually written any demos or tests for it (weird, right? Especially since I have a lot of demo code on my GitHub). Most of those articles are written in C. If I wanted to test this myself in Go or Lisp, I would likely need to disable the Garbage Collector (GC) to observe "pure" hardware behavior.

Then I realized I could write it in Rust, which is well-suited for this. So, here we go.

## My CPU Details

First, I wanted to find my Mac's CPU details so I could write tests depending on the cache line and cache sizes. 

I can get these details using the following commands:

```shell
sysctl -n hw.l1dcachesize # 65536 => 64KB
sysctl -n hw.cachelinesize # 128
```

I’m not entirely sure if this is the correct answer, because Google provides the following specs:

```
Efficiency (E) Cores:
L1 Instruction Cache (L1i): 128 KB per core.
L1 Data Cache (L1d): 64 KB per core.

Performance (P) Cores:
L1 Instruction Cache (L1i): 192 KB per core, 12-way set-associative.
L1 Data Cache (L1d): 128 KB per core, 8-way set-associative.
```

If Google is right, it looks like `sysctl` is reporting the E-core details. However, based on the tests below, it seems they are running on the P-cores. Why? When I run `taskpolicy -b cargo bench` (which forces the background/E-cores), it is about 400% slower than the default. Therefore, I assume `cargo bench` runs on P-cores by default.

## Test Cases

While writing the tests, I essentially ignored the CPU details I gathered since the answers seemed inconsistent. The only thing I am fairly sure of is that `cargo bench` runs on the P-cores. This shouldn't affect the relative speed differences in cache access. Even if I don't know the exact cache line size, a performance hit from an L-cache miss will still be obvious.

**Sequential Access by Steps**

I created a sequence and accessed the elements using different steps:

```rust
pub fn sequential_access_step4(data: &mut [i32]) {
    for i in (0..data.len()).step_by(4) {
        data[i] = 1;
    }
}

pub fn sequential_access_step16(data: &mut [i32]) {
    for i in (0..data.len()).step_by(16) {
        data[i] = 1;
    }
}
```

I benchmarked these two functions using a 64M `Vec<i32>`. Intuitively, the second one should be four times faster than the first, right? Here are the results:

```
Memory Access/sequential_access_step_by_4
                        time:   [5.2634 ms 5.2797 ms 5.2990 ms]
Memory Access/sequential_access_step_by_16
                        time:   [4.4792 ms 4.4846 ms 4.4915 ms]
```

It is actually not much faster. 

The reason, I believe, is that an `i32` is 4 bytes and the CPU loads a full cache line (128 bytes). Since `128 / 4 = 32`, the CPU loads 32 elements at once. The runtimes of the two functions do not differ much because most of the cost is spent jumping to the next cache line regardless of the step size within that line.

**Memory Access with Increments**

This function accesses memory with a specific step (increment). I ran it with several `count/increment` pairs.

```rust
pub fn cache_line_hit_with_increment(count: usize, increment: usize) {
    let size = count * increment;
    let mut data: Vec<i32> = vec![0; size];

    for j in (0..size).step_by(increment) {
        data[j] += 1;
    }
}
```

Access the memory with specific step. And run it with several `count/step` pairs. The result is:

| count\step |     1     |    16     |    512    |   1024    |
|:----------:|:---------:|:---------:|:---------:|:---------:|
|     1      | 14.623 ns | 20.203 ns | 39.497 ns | 60.158 ns |
|     2      | 14.959 ns | 16.719 ns | 61.666 ns | 117.56 ns |
|     3      | 15.316 ns | 16.682 ns | 86.723 ns | 155.49 ns |
|     4      | 15.523 ns | 17.043 ns | 116.55 ns | 191.88 ns |
|     5      | 18.830 ns | 26.392 ns | 129.64 ns | 233.49 ns |
|     6      | 19.095 ns | 27.074 ns | 156.91 ns | 294.41 ns |
|     7      | 19.339 ns | 27.871 ns | 172.78 ns | 329.69 ns |
|     8      | 19.754 ns | 28.192 ns | 190.90 ns | 432.96 ns |
|     9      | 20.547 ns | 28.936 ns | 240.19 ns | **1327.3 ns** |
|     10     | 20.838 ns | 29.175 ns | 249.96 ns | 1330.2 ns |
|     11     | 21.312 ns | 30.231 ns | 280.66 ns | 1402.7 ns |
|     12     | 21.545 ns | 30.510 ns | 283.95 ns | 1402.9 ns |
|     13     | 20.448 ns | 31.647 ns | 331.33 ns | 1466.5 ns |
|     14     | 20.798 ns | 31.434 ns | 324.00 ns | 1487.9 ns |
|     15     | 21.119 ns | 30.458 ns | 456.47 ns | 1474.7 ns |
|     16     | 21.363 ns | 30.754 ns | 397.97 ns | 1471.9 ns |
|     17     | 21.654 ns | 37.488 ns | **1322.7 ns** | 1589.9 ns |
|     18     | 21.879 ns | 37.473 ns | 1503.8 ns | 1709.9 ns |

The timing increases significantly at `9 * 1024` (1024 * 4 * 9 = 36 KB) and `17 * 512` (512 * 4 * 17 = 34 KB). My assumption is that 32 KB is the effective cache size, and the time increases because the CPU needs to reload the cache. (However, the P-core should have 128 KB per core rather than 32 KB; I still don't know why this discrepancy exists).


**Matrix Hit**

Since I have done a lot of Advent of Code (AOC) this year, this matrix test case was quite fun. I actually found performance issues with matrices [previously](https://ccqpein.me/Why-the-Vec-grid-of-my-tool-is-that-slow-in-Rust/). That post was about memory allocation performance; this time, it's about memory access performance.

```rust
pub fn matrix_iter_row() -> i32 {
    let col_num = 512;
    let row_num = 1024;
    let matrix = vec![vec![0i32; col_num]; row_num];

    let mut sum: i32 = 0;
    for r in 0..row_num {
        for c in 0..col_num {
            sum = sum.wrapping_add(matrix[r][c]);
        }
    }
    sum
}

pub fn matrix_iter_col() -> i32 {
    let col_num = 512;
    let row_num = 1024;
    let matrix = vec![vec![0i32; col_num]; row_num];

    let mut sum: i32 = 0;
    for c in 0..col_num {
        for r in 0..row_num {
            sum = sum.wrapping_add(matrix[r][c]);
        }
    }
    sum
}
```

The performance results are:

```
Matrix Hit/matrix_iter_row => 194.06 µs
Matrix Hit/matrix_iter_col => 437.18 µs
```

## Wrap Up

It was fun revealing these L-cache performance issues. I have to admit that I might never encounter this level of performance optimization in my daily work (at least for now). 

But it's always fun to learn something new, and these results actually support the [experience](https://abseil.io/fast/hints.html#better-memory-representation) shared in Jeff’s article.
