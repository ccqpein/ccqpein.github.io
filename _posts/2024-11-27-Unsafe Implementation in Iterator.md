---
layout: post
title: Unsafe Implementation in Iterator
---

A few days ago, I encountered a [performance issue with `Vec<Vec<T>>`](https://ccqpein.me/Why-the-Vec-grid-of-my-tool-is-that-slow-in-Rust/). After resolving that problem, I stumbled upon another challenge, and I think it's worth writing down because I couldn't find a direct answer on Google.

## IterMut for My Map ##

I tried to generate the `std::slice::IterMut` for my `Map<T>` so that I could loop through the map and modify the values inside it.

Here's the struct I came up with:

```rust
pub struct MapIterMut<'a, T>
where
    T: 'a,
{
    /// offsets are where is this map during iter
    r_offset: usize,
    c_offset: usize,

    map: &'a mut Map<T>,
}
```

The next step was implementing the `Iterator` trait for `MapIterMut`. I had implemented this years ago:

```rust
impl<'a, T: Clone> Iterator for MapIterMut<'a, T> {
    type Item = ((usize, usize), &'a mut T);

    fn next(&mut self) -> Option<Self::Item> {
        if self.c_offset == self.map.c_len {
            self.c_offset = 0;
            self.r_offset += 1;
        }

        if self.r_offset == self.map.r_len {
            return None;
        }

        // Unsafe code here
        let result = match unsafe {
            let a = &mut self.map.inner;
            let r = a
                .as_mut_ptr()
                .add(Map::<T>::coop_cal(self.r_offset, self.c_offset))
                .as_mut();
            r
        } {
            Some(a) => Some(((self.r_offset, self.c_offset), a)),
            None => {
                panic!()
            }
        };

        self.c_offset += 1;
        result
    }
}
```

I honestly forgot why I had to use `unsafe` here (specifically the `.as_mut_ptr()` part). But this time, I decided to rethink the design of `Map`. Now `Map` includes this method:

```rust
pub fn get_mut(&mut self, r: usize, c: usize) -> Option<&mut T> {
    let x = self.coop_cal(r, c);
    self.inner.get_mut(x)
}
```

So it seems like I should just be able to call `get_mut`. Right?

## Lifetime Trick ##

The answer is no. I still had to use `unsafe`.

Let’s analyze the lifetimes. `T: 'a`, and the `type Item = ((usize, usize), &'a mut T);`, so everything with `T`'s lifetime should be fine.

As long as `&mut self` lives longer than `&T`, it should be okay. For example:

```rust
struct Some<'a, T>
where
    T: 'a,
{
    v: &'a mut T,
}

impl<'s: 'a, 'a, T> Some<'a, T> {
    fn some(&'s mut self) -> &'a mut T {
        self.v
    }
}
```

The problem is that I cannot give `&mut self` a lifetime like `'s` because the `Iterator` trait doesn’t allow it. That means the `Option<Self::Item>` cannot have a lifetime different from `&mut self`. This creates a conflict between the anonymous lifetime of `&mut self` and `'a`. For example:

```rust
impl<'s: 'a, 'a, T> Some<'a, T> {
    fn some(&mut self) -> &'a mut T { // --> 's removed
        self.v
    }
}
```

This gives the common lifetime error:

```text
error: lifetime may not live long enough
  --> src/main.rs:11:9
   |
9  | impl<'s: 'a, 'a, T> Some<'a, T> {
   |              -- lifetime `'a` defined here
10 |     fn some(&mut self) -> &'a mut T {
   |             - let's call the lifetime of this reference `'1`
11 |         self.v
   |         ^^^^^^ method was supposed to return data with lifetime `'a` but it is returning data with lifetime `'1`
```

## New Unsafe ##

To solve this problem, I decided it makes sense to use `unsafe`. Essentially, I needed to "lie" to the compiler about lifetimes.

Here’s the new unsafe code I wrote:

```rust
impl<'a, T: Clone + Debug> Iterator for MapIterMut<'a, T> {
    type Item = ((usize, usize), &'a mut T);

    fn next(&mut self) -> Option<Self::Item> {
        if self.c_offset == self.map.c_len {
            self.c_offset = 0;
            self.r_offset += 1;
        }

        if self.r_offset == self.map.r_len {
            return None;
        }

        // Unsafe block here
        let result = match unsafe {
            let a = self.map as *mut Map<T>;
            let a = a.as_mut()?; // Convert `a`'s lifetime
            a.get_mut(self.r_offset, self.c_offset)
        } {
            Some(a) => Some(((self.r_offset, self.c_offset), a)),
            None => {
                panic!()
            }
        };

        self.c_offset += 1;
        result
    }
}
```

Let’s break down what’s happening here:

1. `let a = self.map as *mut Map<T>;`  
   This converts `self.map` into a raw pointer.

2. `let a = a.as_mut()?; // Convert a's lifetime`  
   Here, I tell the compiler that `a` (the mutable raw pointer) can safely become a mutable reference with the `'a` lifetime.

As a result, the unsafe block returns `Option<Item>`, where `Item` has the `'a` lifetime.

## Wrap-Up ##

After making this change, I found an article published on Reddit that resonated with this issue. The ideas in it about `unsafe` reminded me of this code change. Although it's labeled as "unsafe," what I’m doing here is essentially just lifetime switching. So, I don’t think this code is entirely *unsafe* in the sense of being error-prone.

Here’s the [article](https://oida.dev/unsafe-for-work/), in case you’re curious.
