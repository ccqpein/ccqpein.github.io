---
layout: post
title: Common Lisp 语法糖
modified: 2015-11-19
tags: study
image:
---

## 写在前面
自学了一段时间的common lisp，相比python而言，感觉语法反而比python简单。CL 语法的逻辑挺固定，当然不是说别的语言语法就诡异，只是理解了语法逻辑，再复杂的函数也知道是干嘛的。相比之下，一些python包的语法各种类方法的嵌套，看上去就挺吓人的。而lisp 就不一样，lisp 从一开始学的时候就很吓人。

在执行复杂语法的时候，lisp 用语法糖解决。python 在调用装饰器的时候用`@decorater` 完成装饰器的调用，这样可以方便的在定义函数的同时装饰函数，而不用在函数写完后用`fun = decorate(fun)` 来装饰。

这篇就是稍微做一个CL 语法糖的笔记。

## '
这个语法糖非常普遍，这个糖的意思是：

~~~lisp
(quote (a b c d))
>>(a b c d)

'(a b c d)
>>(a b c d)
~~~

`'`就是在这个情景中替代`quote` 这个函数，当这个函数被调用的时候，意思就是后面的表达式不会被求值，按照某本书（我忘了那本书）的解释，这相当于`我＝ccQ`，这时候`我`已经被赋值了，意味着当`我`被引用的时候，这个`我`字作为一个指向，指向`ccQ`。

但是如果我想引用`我`这个字本身，就需要一个指令，告知`我`此时没有指向，这时候就用`quote`这个函数。`(quote (a b c d))`表示，后面的`(a b c d)`不要被求值，则就会返回列表本身。

## \#'
这个语法糖经常用在`map`和`lambda`里面，这个糖的意思是说明，接下来是个函数。有些时候，宏的参数里面需要一个函数，由于语法并没有表明哪些是函数，哪些是需要处理的数据，所以`#'`的出现很有必要。

~~~lisp
(map 'list #'(lambda (x) (+ x x)) '(1 2 3))
>>>(2 4 6)
~~~

## \# 
`#`表示一个数组，例子： `('#(1 2 3 4))`生成的是一个数组，`#(1 2 3 4)`，对于lisp来说，数组的内存占用远小于列表，并且由于数组在内存单元中是连续的，效率也比较高。但是数组也有自己的不足，比如没有列表那么简单的增加一个元素。

~~~lisp
(setf aa '#(1 2 3 4))
>>>#(1 2 3 4)

(type-of aa)
>>>(SIMPLE-VECTOR 4)
~~~

## \#s
`#s` 表示一个结构体。可以直接使用赋值`setf`来创建一个结构体

~~~lisp
(defstruct struc-test a b c)
>>>STRUC-TEST

(setf p '#s(struc-test a 0 b 0 c 0))
>>>#S(STRUC-TEST :A 0 :B 0 :C 0)

(setf (STRUC-TEST-a p) 11)
(p)
>>>#S(STRUC-TEST :A 11 :B 0 :C 0)
~~~

## \`
反引号也是一种防止取值的方法，这点有点像`'`，但是两者的不同在于反引号内可以部分求值。

~~~lisp
(setf name "ccQ")

`(this is ,name blog)
>>>(THIS IS "ccQ" BLOG)
~~~

将需要求值的变量前面加上一个逗号，这个特性让反引号在定义宏中，经常被用到。

~~~lisp
(setf address '(you guess))

`(,name live in ,address)
>>>("ccQ" LIVE IN (YOU GUESS))

`(,name live in ,@address)
>>>("ccQ" LIVE IN YOU GUESS)
~~~
在逗号后面加上一个`@`符号能让后面的值，连接到反引号构造的结果中。

再来一个实在不知道怎么描述的例子：

~~~lisp
(defmacro shower (name)
    `(format t "~&The ~S is ~S" ',name ,name))

(shower name)
>>>The NAME is "ccQ"
>>>NIL
~~~