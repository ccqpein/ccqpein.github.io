---
layout: post
title: Set tree-sitter of my emacs
---

I noticed open `Cargo.toml` in my emacs didn't show colors/highlights one day. After check the error messages, I figured out a new word that `tree-sitter`.

## Problem ##

Error message shows it cannot found the `libtree-sitter-xxx.dylib` and it obviously make my `.toml` file openning with issue. 

## Information collection ##

Google is my good friends since 2010, I still believe it today. So, the first is 

> what is tree-sitter

> Tree-sitter is a parser generator tool and an incremental parsing library.

Looks like it is the parser making tool. Then, the second question is: 

> why it screws up my emacs

After some search, the problem came from the `emacs >= 29`. After emacs 29, there is a new feature. Guess what? It is `tree-sitter`. But it isn't the tree-sitter package which already hosted on elpa for a while. It calls `treesit`.

And the error message I got just shows that it cannot find the `dylib` file that should be used by `treesit` in emacs and created through `tree-sitter`. 

## Go fix it ##

Actually, fix this problem does not even need to install `tree-sitter (-cli)` by cargo ~~or homebrew~~ (I need it installed by homebrew when I compile my emacs). Just need do one `batch.sh` from [tree-sitter-module](https://github.com/casouri/tree-sitter-module). 

Then change the `treesit-extra-load-path` in emacs configuration to the folder stores all the result files (`dist/` in the repo root is the default). 

Of course, after dependencies all set, there are some issues in emacs itself. 

Firstly, because I build my emacs with the `treesit` argvs, and every major languages `treesit` has ability to support has their cousins (for example `python-mode` has `python-ts-mode`), so their consins add to `auto-mode-alist` first as native mode. My personal configurations add them later. But when emacs search which mode it gonna use to this file, it searches like stack, find the newest one in `auto-mode-alist`. Which means `rust-mode` before the `rust-ts-mode`. 

I tried to add those `treesit` modes to `auto-mode-alist` again to make them on the top of stack, but it cannot work. I guess the alist cannot accept the duplication entries? So I use a traditional way that add some hook to the languages' modes.

And after all, it works. Now I use the master branch emacs with treesit features and new languages modes.

My `treesit` configuration is [here](https://github.com/ccqpein/ccQ-Emacs-d/blob/master/lisp/init-custom.el)

## See also ##

+ [How to use Emacs 29 Tree-sitter?](https://www.reddit.com/r/emacs/comments/zbpa42/how_to_use_emacs_29_treesitter/)
+ [tree-sitter-module](https://github.com/casouri/tree-sitter-module)
+ [starter guide](https://github.com/emacs-mirror/emacs/blob/master/admin/notes/tree-sitter/starter-guide)
