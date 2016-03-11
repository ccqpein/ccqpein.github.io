---
layout: post
title: 关于 Lisp 的废话
modified: 2016-3-10
tags: study
image:
---

## 起源

Lisp 诞生了至少半个世纪了，至于为什么学这门语言，老实说是收到了Paul Graham 的安利。他在《黑客与画家》这本书里面，对Lisp 的评价非常高。在中文网络上面搜索，对Lisp 最坏的评价也只是停留在「装逼」上，而这是对人的评价，并且是一个中文网络环境中较为无聊的评价，相比PHP 和 Java，针对语言本身的争论并没有这么大。当然也可能是学的人太少，即使已经有几本不错的中文教材和优秀的博文，Lisp 诡异的语法就吓退了不少人。

在2014年底知道了Emacs 这个编辑器，而Emacs 自带一个 Lisp 方言。当在一段时间经常性的看到一个单词，而且伴随「黑魔法」「神的编辑器」这种迷魂汤一起出现，即使是我，恐怕也沦陷了。

## 上车

我先了解了一下 Lisp 的现状，Lisp 有众多的方言，主要还在活跃的是这三个：Scheme，Clojure，和 Common Lisp。第一个 Scheme 是 MIT 自己用来讲课的语言（[SICP](http://www.wikiwand.com/en/Structure_and_Interpretation_of_Computer_Programs)）。Clojure 最近才看了一点，个人感觉是 Lisp 和 Java 的混合体，由于科班出身的大部分在学校都学了 Java，用 Clojure 做项目应该更好上手一点。

前面关于 Scheme，Clojure 的评价都是后话，我最开始是想从 Emacs 开始，根据[这篇](http://blog.csdn.net/redguardtoo/article/details/7222501)教程所讲，最好的开始方法是直接拿高手的配置，尝试了一下，后来由于两个原因，放弃这个方法：

+ 我个人不太喜欢预装一大堆语言的环境，这种赘余不能忍
+ 背景色太丑

于是打算开始看 Emacs 自己的 Elisp 来自己配环境。中文资料太少，后来发现 Emacs 自己的手册写的已经很好了，但是按照之前的经验，看完手册不写东西，和没看没什么两样。几乎是同一时间，看的Common Lisp 教程里面有教如何用 `sbcl`和`Slime` 来把 Emacs 变成一个Ide，类似于`IPython`，而且比较简单。于是就把 Elisp 先放到一边，从Common Lisp 开始。


## 关于CL和其它

之所以选择了 Common Lisp 一个原因是上面讲的，上手相对方便，另一个原因是之前了解了一点 Lisp 方言的情况， Common Lisp 更接近纯 Lisp，想一开始学个比较通用型的。

Lisp 诡异的语法来源 [S-expression](http://www.wikiwand.com/en/S-expression) 至于与 Church 的 lambda 表达式的关系，我没查，只是觉得长得像。


## 难度


## 几本教材的评价

有的没有看完，看完补上