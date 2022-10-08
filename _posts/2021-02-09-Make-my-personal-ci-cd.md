---
layout: post
title: Personal CI/CD
---

I am not a Jenkins' fan in my whole (not long) career. I always feel frustrated when I have to write jenkinsfile or use some other tools based on jenkins. 

However, when I am thinking about Jenkins and the purpose of CI/CD, like codeable configuration, inheritable build environment, etc. there is a word that jumps into my brain ---- Lisp.

So I am trying to write my personal CI/CD with Common Lisp, for fun. Make Lisp be my Groovy Jenkinsfile, let configuration can be coded, like what emacs does. 

## General Design ##

Firstly, as all other CI/CD tools do, my CI/CD application should has event. It can be timer trigger, it can be git push, it can be some http requests, it has to have a abstract "Event" part.

Secondly, when my application receive a event, there should have a rules file to tell my app what's to do next. Like Jenkinsfile for jenkins, instead, I use legal lisp file for rules file.

Then, that's it, it is general idea in my mind. Because rules files are written in Lisp and Lisp runtime can interpret it and do the jobs, most of work is how to design/code application instead of worrying about how to make a new language of my CI/CD.

### More Details ###

There are some tricks when I am thinking about code detail. Like: every events will generate a single job, and every new jobs will interpret rules. That's means every rules commands should be nested inside the job's environment which inherited from job instance and mutated by rules.

Then I met one major problem, when rules file is interpreted by job instance, rules, which legal lisp code, need running with dynamic environment value. In other word, code running with the values where they are running instead of where they are defined.

Fortunately, Common Lisp have a very convenient way to do this.

```lisp
(declaim (special *a*))
(defun foo () (print *a*))

(let ((*a* 1)) (foo)) ;;=> print 1
(let ((*a* 2)) (foo)) ;;=> print 2
```

> If you have experience of using emacs, you might have heard one of the frequent criticisms of emacs-lisp that it uses dynamic variable by default.

## Implementation ##

There are the [source code](https://github.com/ccqpein/q-cicd/commit/11becebcd293eb3f66f048d00f7a2ee78368ec81).

**rules.lisp**

This file has all "rule commands" like `show`, `shell-command`, or `file-exist`. They are legal lisp functions, make things pretty easy.

**jobs.lisp**

Major function in this file is `run`. I used `cl-threadpool` to create a global `*jobs-pool*` to run job instance. As I mentioned above, before the true rule file running, I bind `*job-env-table*` and `*job-show-log*`for all *rules* using this dynamic env var. 

Then, there is the second `let*` block for a special usage. `header` and `tailer` create one temporary package for protecting the runtime env. If there are `defun` inside rule file, it won't effect the job package, it will disappear with this job's run finishes.

Nothing else special except using `(defmethod initialize-instance :after)` to update job env (a hashmap inside job instance). 

## Leap of Faith ##

I write `example/demo-rules.lisp` for testing how is this CI/CD app work. Start REPL, and run:

```lisp
(ql:quickload '("cicd" "cl-threadpool"))

(get-output-stream-string
 (cl-threadpool:job-result
  (let ((j (jobs:make-job)))
    (jobs:run j "./demo-rules.lisp"))))
```

it will generate `build/file` with number `123` inside.

## Next ##

It is still a demo project for making sure everything in my mind can work when I finish this blog. Of course there are bunch of details are missing. I might add the features when I use this app. Let reality tell me what's feature are necessary.
