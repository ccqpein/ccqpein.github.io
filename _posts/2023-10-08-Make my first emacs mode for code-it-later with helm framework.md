---
layout: post
title: Make my first emacs mode for code-it-later with helm framework
---

I wrote my first elisp mode. I have my [code-it-later](https://github.com/ccqpein/cl-format-rs) tool that I find myself using everyday. As an Emacs user, I've been wondering if I could call it from inside Emacs, like many other packages. And because I created the [code-it-later](https://github.com/ccqpein/cl-format-rs), it seems appropriate for me to be the one to write this mode for my project.

## Learning from helm-ag ##

Despite playing with Emacs configuration for about 8 years, I've never written any Emacs modes before. Luckily, there's a mode that closely resembles what I had in mind for the code-it-later-mode - it's called helm-ag. helm-ag uses the helm framework to call the ag command and return the results to Emacs interactively. It seems like an ideal learning resource, except in this case, I would be integrating my own tool, `code-it-later`. 

### Utilizing the helm Framework ###

helm-ag employs the helm framework. helm is indeed an impressive framework, but as a beginner attempting to write an Emacs mode, I certainly have a lot to learn.

After reviewing the helm-ag code and the helm [documentation](https://github.com/emacs-helm/helm/wiki/Developing), I understood that I needed to create a helm source, specifically an asynchronous one. helm will take the "source" I provide and handle the display/actions/etc. as defined within the source.

### Async source ###

If I've understood this correctly, the asynchronous source calls the process and sets the stdout as the source's candidates. The source instance will then be utilized by helm to display within its buffer. Asynchronous sources are different from regular ones due to the possibility of the process running for an extended duration. With async sources, helm doesn't have to wait, similar to helm-ag and the code-it-later-mode.

### Actions ###

While I'm not particularly a fan of object-oriented programming (OOP), helm utilizes class structures efficiently. When I define my class that inherits from `helm-source-async`, I can provide the default slots, much like `helm-ag` does. This simplifies things, especially while I'm still learning.

I encountered one issue that stumped me for a prolonged period: why persistent-action runs automatically in helm-ag. According to the [source document](https://github.com/emacs-helm/helm/blob/d6806ad23304277b19b0646ce5b19e1a6509ea06/helm-source.el#L175C7-L175C7), `persistent-action` is an action that can execute without quitting the helm buffer.

helm says I need to press C-j, then return to call the persistent-action. However, I noticed that helm-ag didn't require pressing C-j and it would call the `persistent-action` each time I chose a candidate in the helm buffer.

In helm-ag, the `persistent-action` comprises opening the file and locating the line of the candidate. It makes logical sense to explore the candidate without exiting the helm buffer. After extensive study and even rise the question issue within the helm-ag repository, I discovered that it wasn't `helm-ag` causing this behavior. It was due to me setting `helm-follow-mode-persistent` to true when I loaded `helm-ag`. A single line of code enabled this wonderful feature.

## Modifying Code-It-Later ##

While programming in elisp, I encountered an issue: the process was set to return the `code-it-later` results directly. However, helm was unable to handle this directly. So, I adjusted `code-it-later` to produce list results, which helm could handle more efficiently. One of the advantages of this project is that it allows direct manipulation of the data source as required. 

## Conclusion ##

helm is an excellent tool. However, the development documentation could use some improvement. I often had to refer to comments within the code in order to fully understand the class slots.

Creating my first Emacs mode was a time-consuming but rewarding experience. It was a thrilling exercise as an Emacs user to write my own mode. The addition of the `cl-lib` package, which facilitates writing a lot of Common-Lisp-style code, was particularly beneficial and simplified the whole process.

[Link of helm-code-it-later](https://github.com/ccqpein/helm-code-it-later)
