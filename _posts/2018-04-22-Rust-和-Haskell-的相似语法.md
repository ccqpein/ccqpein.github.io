---
layout: post
title: Rust 和 Haskell 的相似语法
categories:
- blog
---

## 写在前面

在学习Rust 的过程中遇到了一些和Haskell 语法很相像（或者说是可以类比）的部分，或者是设计相似的部分，这一篇就把我觉得像的部分整理一下。

## Haskell data 

Haskell 里通过data 关键字生成新类型的用法在Rust 里不能说几乎是一样的，但是我觉得很像就是了：

```haskell
λ> data Test1 = Lalala Int | Hahaha Int
λ> let a = Lalala 1
λ> let b = Hahaha 1
λ> a
a :: Test1
λ> b
b :: Test1
```

```rust
enum Test1 {
    Lalala(i32),
    Hahaha(i32),
}
```

## pattern match



