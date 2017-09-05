---
layout: post
title: Haskell data 使用小记
categories:
- blog
---

## 写在前面

这一篇的来由是前段时间看到用 Haskell 实现 Dependent Type 的 Haskell 代码里面有用一个我不知道的 `data` 语法实现，觉得有意思，就抽空看了看。这一篇主要是方便我自己复习，免得过段时间就忘了。

## 正文

我最开始看的书是[Learn You a Haskell for Great Good!](http://learnyouahaskell.com/chapters)，里面的第八章有提到 `data` 关键字的用法。整理了一下，从简单的讲起。

### 枚举
`data` 第一个用法首先是类似于别的语言的枚举的形式：

```haskell
data Weekdays = Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday
```

同时，这种类型可以根据 `deriving` 的类型类的不同，实现不同的特性。

有两个点要注意的，一个是 `data` 后面的类型名要首字母大写，这个很重要，对理解 Haskell 类型判断的逻辑有用，下面会提到。另一个点是，里面的 Monday 等等也是首字母大写的。

### 构造
`data` 的第二个用法是构造一个类型，比如一个矩形需要长和宽：

```haskell
data Rectangle = Rectangle Float Float
let rectangle = Rectangle 1.0 1.0
```

这里有一个混淆的点，`data` 后面和 `=` 后面的 `Rectangle` 虽然都是大写，但意义不同。等于号后面的 Rectangle 是用于构造的，而不是类型，虽然同名，但不是一码事。

这时候可以回过头去看之前的枚举data，完全可以理解成里面的 Monday, Tuesday 等等是一个空的构造。

### 进阶构造
`data` 用于构造类型的时候，可以在构造体内增加信息，方便理解。上面的 Rectangle 的例子里，两个Float 哪一个是长，哪一个是宽，没有明确说明，如果想明确的知道哪个是哪个，可以在构造里面增加详情。

```haskell
data Rectangle = Rectangle {length :: Float
                            , wide :: Float}
let newRectangle = Rectangle {length=1.0, wide=1.0}
```

这时候注意，构造器里面的`length`、`wide` 是小写，而后面的`Float`是大写。这时候要区分个个单词的不同意义了，因为我在这里被坑过。

`data`允许定义一个递归类型，就是`data`定义的类型里面可以包含自己，上面说了`data`里面进行构造的不是类型，那么哪些是类型哪些不是呢？给个例子：

```haskell
data Ccq = None | CcqConstructor Integer Ccq
```
上面的例子里，`data`后面的`Ccq`是定义的类型，`None`是空构造（枚举），`CcqConstructor`是构造，`Integer`是类型，最后一个`Ccq`是类型，也就是自身。构造出来的数据，对应的类型都是`Ccq`。

这里比较绕的原因有两点：

1. 构造**可以**和对应的类型同名，这样虽然方便了不用想类型名，但是会出现混淆。
2. 类型和构造都为首字母大写，且`data`定义类型允许定义递归类型，在写`data`的时候可能会迷惑哪个是类型，哪个是构造。

### 进阶构造（二）
对`data`增加类型标记， 直接给例子：

```haskell
data Rectangle a = Rectangle a a
```

其中的`a`为类型，根据构造的不同来定义不同的类型，比如

```haskell
-- a 是 Num 实例
λ> :t Rectangle 1 1
Rectangle 1 1 :: Num a => Rectangle a

-- a 是 Fractional 实例
λ> :t Rectangle 1.0 1.0
Rectangle 1.0 1.0 :: Fractional a => Rectangle a
```

### GADTs (Generalised Algebraic Datatype)[^GADTs]

[^GADTs]: https://wiki.haskell.org/GADT

这个就是我一开始说，看到的不一样的用法。先给个例子：

```haskell
data Empty
data NonEmpty
data List x y where
     Nil :: List a Empty
     Cons:: a -> List a b ->  List a NonEmpty
     
λ> :t Nil
Nil :: List a Empty
λ> :t Cons 1.0 Nil
Cons 1.0 Nil :: Fractional a => List a NonEmpty
```

在定义阶段，`Nil`和`Cons`均为构造，后面的写法有点像函数的写法，`List x y` 的类型在构造阶段直接写好了，如果不这样写，而是用上面讲的构造来写，`Nil` 返回的类型就是`List x y`，而不是`List a Empty`。这种写法增加了类型定义的灵活性，虽然我现在还没看到更多使用场景，不过感觉还是挺强大的。

## 最后
目前就这些了，感觉`data`在 Haskell 里面还是很重要的，这篇就是整理一下自己曾经迷惑或者不太懂的点，以后如果有机会再更新吧。




