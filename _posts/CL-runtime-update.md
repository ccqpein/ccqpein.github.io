## 写在前面 ##

这几天处理手头新项目的时候，突然想到 Common Lisp 里面好像有一种运行时更新的方法。听说过很多次，但是从来没有用过。一直很好奇，于是前几天试了试。

用英文搜了一圈，不知道这种运行时更新的术语是什么，就只能搜Common Lisp + 更新，运气还不错，最后找到了一个[SOF的答案](https://stackoverflow.com/questions/8874615/how-to-replace-a-running-function-in-common-lisp)。

两个答案加在一起就讲了如何实现这个功能。实现起来一点也不难，正是如此才把我惊到了。

## HOW-TO ##

要测试实现这个功能首先得想好我到底想做什么，既然是一个运行时更新，那么肯定有一个更新前的状态和一个更新后状态，同时两个状态还能随时监测到。

一开始我想的是用一个loop 无限循环，循环体内不停调用一个函数，然后更新这个函数的返回，通过if判断就能知道是不是更新成功了。

这个办法只有一个问题：实现不了。

上文的那个答案里就有讲为什么这个无法实现[^1]

>This will not replace already running calls of previous functions; for example, an infinite event loop can not be changed this way....

那么还有什么办法能简单快速的确定函数是不是更新了呢？而且还不能是一直被调用，也就是说是一种事件调用的方法。于是我想到快速建一个web 服务，然后通过访问服务来查看结果。我直觉上觉得这个可以，一般服务器是一个监听，收到消息后再调用相应的函数来实现，这样就能避免无限循环调用。

然后快速搜到了这个第三包[woo](https://github.com/fukamachi/woo)[^2]


[^1]:递归
[^2]:dddd

