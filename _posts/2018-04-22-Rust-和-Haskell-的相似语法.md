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

## Pattern match


```haskell
data Test1 = Lalala Int | Hahaha Int

patternMatchTest :: Test1 -> Int
patternMatchTest (Lalala a) = a
patternMatchTest (Hahaha a) = a + 1

λ> let a = Lalala 11
λ> patternMatchTest a
11
```

```rust
fn main() {
    let a = Test1::Lalala(1);

	match a {
        Test1::Lalala(i) => println!("a, {}", i),
        Test1::Hahaha(i) => println!("b, {}", i+1),
        _ => println!("wrong"),
    }

=> a, 1
```

这个例子可以看到两个语言模式匹配的一点点不同，Haskell 在函数声明的时候，就可以对参数进行模式匹配，Rust 得必须用match 关键字去匹配。语法上我觉得长得很像，但是rust 必须声明`Test1::`，在匹配的时候都能进行对参数进行赋值`a`和`i`。我觉得在语法设计上，Haskell 对类型匹配的优先级还是很高的，而Rust 这个操作有点像Clojure 的解构，但是Rust 的所有权设计让这个使用并不如Clojure 方便，但是至少比没有强。

