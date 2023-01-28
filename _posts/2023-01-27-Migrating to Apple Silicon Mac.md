---
layout: post
title: Migrating to Apple Silicon Mac
---

After a year's wait, I finally got my M2 aarch64 chip MacBook Pro. And after one day of usage, there are some experiences I should write down about migrating from the old intel macbook pro to this new one. 

Generally, not a lot frustrated. I use the mac migration assistant to transfer data from the old mbp to this one directly. Mostly, everything is just like a copy from the old one to the new one. Even the safari tabs I opened on my old computer are also opening on the new one.

## Mac applications ##

For the Mac application I installed, they are the ones that should be totally the same after the migration assistant did its job. However, some applications need to ask permission again. 

My old laptop still has the touch bar. The best part of the touch bar is it is easy to activate PIP when I watch videos in Safari. So after this upgrade, I need to install a safari extension to active PIP.

Besides, my menu bar is much shorter than before because of the notch. So I am trying Bartender4 to hide some status icons.

## Developing environment ##

The development environment is much more complicated because the migration assistant only copies the files. The problem isn't the link/dynamic library/etc. Issues, instead, it is a lot of developing tools. They were built on X86_64 chips. 

And yes, Rosetta can solve the issue (sort of). But that's not enough. The journey of migrating the development environment to a new mac starts from here.

### iterm ###

After migration from the old laptop, I was trying to open my iterm2, but it exited immediately with an error message:

> A session ended very soon after starting.

First, I reinstall the ierm2 and check if it supports Silicon. iterm2 looks like a universal app which means it supports the new CPU. After a lot of searches, it shows the issue comes from the shell.

### ZSH ###

My ZSH was installed on x86, but if I cannot log in to the shell, I cannot reinstall it. So I change my shell path to `/bin/shell`. However, some issues still happened, but at least I can install `softwareupdate --install-rosetta`.

After installing the Rosetta in shell, I reinstall zsh with Homebrew. Then I found another problem: Every command is stuck a bit. I decided to ignore that first and install rust first. 

### Rust ###

Rust one is pretty straightforward. First, I need back up all the applications I installed through cargo with `cargo install --list`. Second, I reinstall the `rustup` and choose `nightly-aarch64-apple-darwin` as my default toolchain. Third, I need to reinstall all applications I installed before. 

Then, another issue appears, crate `cargo-update` cannot compile. 

### Thanks to openssl ###

The problem is `openssl@3` `dylib's were built on x86 rather than Silicon. I tried to reinstall the openssl@3 by Homebrew, and the issue is still there. 

Now I finally find everything I reinstall with Homebrew are still x86. Then I check `brew config`, it shows `Rosetta 2: true`. So the next problem is to solve the install homebrew natively. 

### Homebrew ###

I try reinstalling Homebrew, but the notification that the install scripts show me isn't right. Homebrew website shows

> This script installs Homebrew to its default, supported, best prefix (/usr/local for macOS Intel, /opt/homebrew for Apple Silicon and /home/linuxbrew/.linuxbrew for Linux)

but the script shows me it will modify `/usr/local/` rather than `/opt/homebrew`. There is no other way, and I have to uninstall homebrew totally and install it back. After uninstalling and cleaning a lot of legacies (some of them were made in 2014, geez, a lot of trash there), the homebrew installation script shows me it is going to change the `/opt/homebrew/` path, finally. After installation, `brew config` shows `Rosetta 2: false`. 

Then I reinstall everything like zsh (and change zsh path from `/usr/local/bin/zsh` to `/opt/homebrew/bin/zsh` in everywhere, like `/etc/shells`, my user login shell, and iterm), pyenv, openssl@3, and so on. 

And it fixed the stuck issue of zsh, and `cargo-update` installation is good now.

### emacs ###

I compile my emacs right after my new laptop migrated, and it takes from 8:45 to 6:30. After I reinstall all dependencies with silicon homebrew, it takes 3:31. Amazing improvement. Then there is another problem: it cannot open. 

After a loooooot search, TL;DR, it is because Apple gives more "security" in Silicon that I have to give one more step to codesign the emacs app.

> codesign --force --deep --sign - /Applications/Emacs.app

And, of course, some packages inside emacs need to change too.

#### aspell ####

Emacs cannot find my aspell command even I install it after emacs give me an error. I think it is because emacs needs to know it is there while it compiling. (maybe?). After recompiling emacs again, it fixed itself. 

#### treesit ####

treesit's needed `.dylib's need to recompile because the current ones are built on my old x86 laptop. 

### pyenv ###

The python I installed with pyenv (on my old laptop) migrated to the new one. Right after reinstalling `pyenv` with Homebrew, I can use it like before...... well, not exactly. Python cannot find the lib in paths, and the path are started with `/usr/local`, another path issue. Looks like the python installed with the path when it had. So, I need to reinstall the python with pyenv, and the problem is solved.

## More? ##

I would add more experience/records about the issue I met with those related migrations. 

