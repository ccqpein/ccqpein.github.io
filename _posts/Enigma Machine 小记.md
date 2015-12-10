---
layout: post
title: Enigma Machine 小记
modified: 2015-11-19
tags: study
image:
---

# Enigma Machine 小记

## 写在前面
前几天，看了一下[知乎上一篇文章](http://www.zhihu.com/question/28397034)讲《模仿游戏》中提到的德军密码机Enigma。然后就想用python 自己写一个enigma机出来。

## 转子问题
过程中，设计转子的类。最开始没有一一对应，导致明文可以变成密文，但是密文缺没办法变成明文。后来用了一个取巧的方法，让a到z随机排列，然后用列表倒叙，变成密匙。由于正好有26个

~~~python
def __init__(self, *args):
    self.originalDict = [i for i in originalKey]
    random.shuffle(self.originalDict)
    self.originalKey = []

    for i in reversed(self.originalDict):
        self.originalKey.append(i)
~~~

这样下来就有一个问题，按照知乎的讲解，反射板的作用让enigma机得到了两个特性：

>性质一：反射器使得恩格玛机的加密过程是自反的。也就是说，如果输入字母A得到字母G，那么在机器配置不变的情况下，输入字母G一定会得到字母A。

>性质二：一个字母加密后的输出结果绝不会是它自身。

首先性质一的前提就是之前讲的，一一对应关系，其实有没有反射板，只要能做到a得到z，同时输入z一定能得到a就可以了。这并不是反射板的作用。

我觉得反射板的作用是第二点，按照enigma的设定，每一次输入结束后，转子都移动一格，字母表就往后一格，那么，说明有一种情况可能存在：第一个转子输入A，输出也是A。反射板杜绝了这个可能性。

假设上面这种情况不存在，每一个转子的输出都不等于输入，在偶数个转子共同作用的情况下，是存在明文等于密文的情况（我这个偷懒的转子就是这样），所以反射板在我的实现里就是一个转子，只不过它调整偶数为奇数，就杜绝了偶数个转子可能出现的明文等于密文的情况。而德军是不是这样想的，就不知道了。