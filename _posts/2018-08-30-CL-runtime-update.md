---
layout:     post
title:      "Common Lisp 运行时更新"
modified:   2018-08-30
tag: study
---

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

然后快速搜到了这个第三方包[woo](https://github.com/fukamachi/woo)[^2]，开了一个 server demo 然后里面调用一个`test` 函数。我的目的就是修改`test` 函数，这样就在网页里看到不同的结果了。

**源码**

```lisp
(ql:quickload "swank")
(ql:quickload "woo")

(defun test ()
  "1")

(defun main ()
  (swank:create-server :port 4007  :dont-close t)
  (woo:run
  (lambda (env)
    (declare (ignore env))
    `(200 (:content-type "text/plain") (,(test)))))
  (loop))

```

接下来解决如何链接的问题，我最初的想法是可能要开一个端口，然后这个端口监听到命令后就开始重新载入`test` 函数。然而第二个答案给了一个更神的办法，直接用`slime` 链接到运行中的Lisp image，然后直接在里面改。

我在[这篇文章](http://ccqpein.me/2016/03/10/关于-Lisp-的废话.html)中提到过`slime`，可以把它想像成一个lisp 环境的REPL，类似于Lisp 中的`ipython`，`slime` 会用一个叫`swank` 的服务去链接Lisp runtime，所以我感觉理论上，`slime` 做的事一直都是在运行时更新（一个Lisp 环境），只是从来没有注意到就是了。这个办法真的神了，因为平时写CL 的时候就是打开`slime` 进行调试和测试，这个办法没有引入任何其它的操作，完全就是用日常要用的东西，稍微改一点点设置就能用。

如果要在Lisp image 里面用就需要在主程序中使用`swank`，我是直接使用`quicklisp` 进行安装，最后用`sbcl` 编译成可执行文件就行了。

只有一个坑，就是`(swank:create-server :port 4007  :dont-close t)`这行要写在main 里面，写在外面的话sbcl load 的时候就已经开了4007 端口，再编译会出错。

一切就绪后，运行编译后的binary 文件，然后在Emacs 里面用`slime-connect`，输入`host` 和`port`，就可以连接到正在运行的二进制文件中，这时候可以重新载入`lisp` 文件，`fasl` 文件，甚至直接重新写一遍`test` 函数，只要能把`test` 这个符号替换掉，就行了。


[^1]:这个答案说如果用递归，而不用loop，可能能实现运行时更新，我没有测试，但是loop 无限循环确实是不行。
[^2]:看上去很快的一个服务器包，能和Golang 打一下，但是不知道怎么测试的，实际使用会不会有问题。看了一下源码，用了很多CL 的优化技巧，特别适合学习。

