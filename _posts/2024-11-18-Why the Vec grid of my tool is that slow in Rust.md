---
layout: post
title: Why the Vec grid of my tool is that slow in Rust
---

Time flows and now it is November. The AOC is coming in just one month. I was checking the first year of AOC I completed back in 2017. When I was working on day 3, I was going to use the AOC map that I had made in the AOC tools I worked on during the last several AOCs.

I just skipped the quiz part because it doesn't have major issues. The problem is I used a `Vec<Vec<T>>` to create the 2D grid map, and I need a huge map this time. After checking the code, I found this line:

```rust
let mut m: Map<Option<i32>> = Map::new(200000, 200000, None);
```

It is extremely slow. It's very interesting—how can just initializing a Vector be so slow?

## What does Google say? ##

Google shows me that this isn't a new question; Reddit and StackOverflow have some general answers as to why the `Vec<Vec<T>>` is slow:

From Reddit [post](https://www.reddit.com/r/rust/comments/z26wm5/comment/ixfpm8t):

> This structure is probably good enough for most use cases, but has some issues.
>
> Firstly, note that CPUs load data from memory in chunks and store them in cache, which is much faster (L1 cache is ~100x faster than main memory). Because it's so much faster, the CPU often loads more than it needs, under the assumption that if you're loading data from some address, you likely want other data near it.
>
> A Vec is a pointer to a heap allocation. All the memory in a single vec is contiguous, but if you create lots, it's not guaranteed. So a Vec<Vec> will have suboptimal cache performance, sincethe top-level Vec is only storing pointers. Loading the memory for that pointer will likely not load the data it points to. And because every Vec might be pointing to totally different heap locations, you're likely going to go to main memory every time you pick a different Vec.
>
> Arrays are good if you know lengths at compile time. They pack all their elements inline, so a [[T; N]; M] will be closely packed. But if your dataset is very sparse, there are more efficient ways to represent it.

From StackOverflow [post](https://stackoverflow.com/questions/60583618/performance-of-rust-vector-vect-versus-array-t-n):

> Vector of vectors uses N+1 separate allocations. One of the oldest tricks in programming is to replace an array of same-size arrays with a single flat array of size W*H, and index elements with X*H+Y (or Y*W+X).

I understand the heap allocation and the CPU cache mismatching of `Vec`. But I’m still confused as to why initializing costs so much time. From my understanding, I thought it just allocates memory and writes `None` inside one by one. And the answers above are all about reading data.

## What does the source code say? ##

So I tried to check the source code of `vec!` that I used in the `Map::new()`. After running `cargo expand` and digging a bit, I found it calls `extend_with(&mut self, n: usize, value: T)` in `alloc/src/vec/mod.rs`.

```rust
    fn extend_with(&mut self, n: usize, value: T) {
        self.reserve(n);

        unsafe {
            let mut ptr = self.as_mut_ptr().add(self.len());
            // Use SetLenOnDrop to work around bug where compiler
            // might not realize the store through `ptr` through self.set_len()
            // doesn't alias.
       let mut local_len = SetLenOnDrop::new(&mut self.len);

            // Write all elements except the last one
            for _ in 1..n {
                ptr::write(ptr, value.clone());
                ptr = ptr.add(1);
                // Increment the length in every step in case clone() panics
                local_len.increment_len(1);
            }

            if n > 0 {
                // We can write the last element directly without cloning needlessly
                ptr::write(ptr, value);
                local_len.increment_len(1);
            }

            // len set by scope guard
        }
    }
```

In this function, I’m thinking that the `clone()` in `ptr::write(ptr, value.clone());` costs a lot of time, and it's the "reading" operation, which might trigger the heap memory issue. 

## What does ChatGPT say? ##

So, I activated my ChatGPT buffer in Emacs and sent all the information I had and the guesses I made to it. I let it explain it to me.

> You're correct that the performance issue in your code occurs during initialization when you're working with a `Vec<Vec<T>>`, specifically in this line of `extend_with`:
>
> ptr::write(ptr, value.clone());
>
> ### Main Issue: **Cloning Deeply Nested Structures**
>
> One major source of the performance problem is deep cloning of Vectors, especially with a `Vec<Vec<T>>` structure. Since `Vec` involves heap allocations, every time you clone a `Vec<T>`, the entire structure (including its heap allocation) has to be copied. In the context of nested vectors (`Vec<Vec<T>>`), this can be an expensive operation because:
>
> - **`Vec::clone()` behavior**: `Vec<T>` implements the `Clone` trait. When you clone a `Vec`, Rust doesn't just copy the raw memory, because the vector's elements can be non-trivially large. Instead, `Vec::clone()` does a *deep copy*. This means it allocates the same amount of memory as the original vector and then clones each of the elements in the vector. For a `Vec<Vec<T>>`, each inner vector in your outer vector has to be individually cloned.
>
> - **Heap allocations**: Each `Vec` manages its own heap allocation. When you clone an inner `Vec`, it's copying its data to a new allocated section of heap memory. So, if you have an outer `Vec` containing many inner `Vec`s, cloning them results in N allocations, each of which may individually involve moving memory around. This becomes an expensive process once the size of the vectors grows.
>
> When you call `extend_with(n, value)` with `value` being a `Vec<T>`, you can imagine it is slow because:
>
> 1. **Memory Allocations for the Inner Vectors:** Every call to `clone()` for a `Vec<T>` creates a new heap allocation for that inner vector.
> 2. **Copying the Data in the inner `Vec<T>`:** The elements of the inner `Vec` must be cloned (deep copied) as part of the cloning process.
> 3. **Multiple Allocations:** Since each inner `Vec` might reside in a different heap location, initializing many inner vectors means many separate heap allocations and copying operations, which can be a performance bottleneck.


(I wish I had ChatGPT years ago when I was full of curiosity—it definitely would have helped me with learning.)

## What do the test codes say? ##

Okay, now I think the `clone` in the `vec!` has some performance issues. Speaking of `clone`, I remember that `Cow` is a tricky struct that only truly clones the `T` when it is mutable. So if `clone` is the real problem, I should see a lot of performance improvement if I use `Vec<Cow<Vec<Option>>>`.

Original version:

```rust
fn test1() {
    let now = Instant::now();
    let a: Vec<Vec<Option<i32>>> = vec![vec![None; 50000]; 50000];
    println!("time cost: {:?}", Instant::now().duration_since(now)); // 1.857321917s
    dbg!(a
        .into_iter()
        .map(|aa| aa.into_iter().map(|aaa| aaa.unwrap_or(0)).sum::<i32>())
        .sum::<i32>());
    println!("time cost: {:?}", Instant::now().duration_since(now)); // 24.437415167s
}
```

On my machine, it takes `1.857321917s` to generate the init vector (the `dbg!` part is just to let the compiler know I need to use it, in case the compiler notices there's no usage of `a` and just ignores it).

Now, the `Cow` version:

```rust
fn test2() {
    let now = Instant::now();
    let seed: Vec<Option<i32>> = vec![None; 50000];
    let c = Cow::from(&seed);
    dbg!(c.is_owned());
    let a: Vec<Cow<[Option<i32>]>> = vec![c; 50000];
    println!("time cost: {:?}", Instant::now().duration_since(now)); // 390.583µs
    dbg!(a
        .into_iter()
        .map(|aa| aa.into_iter().map(|aaa| aaa.unwrap_or(0)).sum::<i32>())
        .sum::<i32>());
    println!("time cost: {:?}", Instant::now().duration_since(now)); // 15.478458542s
}

```

Well, I guess the `390.583µs` is much faster than `1.857321917s`.

Then I got a bit curious about how the `clone()` is implemented in `Cow`.

```rust
impl<B: ?Sized + ToOwned> Clone for Cow<'_, B> {
    fn clone(&self) -> Self {
        match *self {
            Borrowed(b) => Borrowed(b),
            Owned(ref o) => {
                let b: &B = o.borrow();
                Owned(b.to_owned())
            }
        }
    }
}
```

Then I started wondering if an owned `Cow` has the same performance issue as the original code because the `b.to_owned()` looks like just a normal `clone`.

And Rust's source code shows that it truly is:

```rust
impl<T> ToOwned for T
where
    T: Clone,
{
    type Owned = T;
    fn to_owned(&self) -> T {
        self.clone()
    }

}
```

So, I wrote `test3`:

```rust
// Cow from owned
fn test3() {
    let now = Instant::now();
    let seed: Vec<Option<i32>> = vec![None; 50000];
    let c = Cow::from(seed); // <------------------------ this is owned
    dbg!(c.is_owned());
    let a: Vec<Cow<[Option<i32>]>> = vec![c; 50000];
    println!("time cost: {:?}", Instant::now().duration_since(now)); // 1.761242292s
    dbg!(a
        .into_iter()
        .map(|aa| aa.into_iter().map(|aaa| aaa.unwrap_or(0)).sum::<i32>())
        .sum::<i32>());
    println!("time cost: {:?}", Instant::now().duration_since(now)); // 19.014466209s
}
```

And the result was just as I expected: `Cow::from(seed)` makes the data inside owned. The init processing becomes just like the original version, ~1.7s.

## Wrap-up ##

It was fun discovering how expensive `Vec<Vec<T>>` can be and understanding why. I know about heap memory performance issues but hadn’t come across it until this situation. I also found a use case for `Cow`. Overall, it was a pretty nice journey.
