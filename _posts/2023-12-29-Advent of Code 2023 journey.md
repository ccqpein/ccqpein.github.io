---
layout: post
title: Advent of Code 2023 journey
---

The AoC 2023 has finished! Just like last year, I am going to record my AoC 2023 journey in this post. This year, I sought a lot of help from my friends in the chatting group we made last year, and the geniuses on Reddit. I truly learned a lot, including several algorithms I had never even heard of before.

## Day 1 & 2 & 3 & 4 ##

On the first day, I was writing in Rust and Common Lisp at the beginning. The coding part was straightforward enough. I was still writing my parser by myself until my friend mentioned Regular Expressions. I feel so foolish; why hadn't I thought about it? So, I rewrote my Day 2 input parser with the regex library. In Common Lisp, I needed to learn the cl-ppcre library.

After that, for Days 3 and 4, I was using regex to write parsers, and I really liked it.

## Day 5 ##

My brute force method couldn't work this time because SBCL on my M2 Silicon Macbook Pro gave the "Heap exhausted (no more space for allocation)" error. It was weird because I didn't see the memory usage being that huge. So, I called for help from my friend and rewrote the major logic by caching more parts. Finally, I finished it with two stars.

## Day 6 ##

Day 6 was interesting because I actually didn't need the code to finish it. I could just solve a quadratic inequality in one variable and give the answer directly. However, I had forgotten how to solve it. It has been a looooong time since junior high school. So, I coded to solve Part 1, but for Part 2, I used an online calculator to get the answer.

## Day 7 ##

I needed to create my own sort function and just replace it within the sort function in Lisp. I remember last year there was a similar type of question. It is good for languages that allow defining custom sort functions.

## Day 8 ##

A misunderstanding of the input took me a while to debug. It made me realize that I need to check the input as well. This actually helped me on Day 20.

## Day 9 ##

My input parser forgot to account for negative numbers. Changing from `\d+` to `-?\d+` just fixed it.

## Day 10 ##

Day 10 is when the difficulty started increasing. The technique I learned from last year's AoC called flood filling—I tried to use it in this day's Part 2. But it didn't work. Then I found a trick that when I scan a line, if they pass in one direction, the empty spots after are included, until they reach the edge of the other direction. It is tricky. I'm pretty sure there are other algorithms like the one from Day 18, but I haven't checked.

## Day 11 ##

Day 11 was straightforward.

## Day 12 ##

I tried to make regex groups and match the inputs, but it didn't work. I went to Reddit and found someone who used regex too. But instead of matching the whole line, they matched groups one by one for each line, and it worked.

## Day 13 ##

For Part 2, I needed to return all possible rows/columns rather than the first one, because the first one might be an obsolete one which I didn't want.

## Day 14 ##

After several updates of my AoC map tool, Day 14 was straightforward enough to solve. In Part 1, I thought it was the offset trick, but actually, it was just map generation.

## Day 15 and 16 ##

Straightforward.

## Day 17 ##

I love Lisp, but maintaining several tables as a cache for dynamic programming is frustrating. I wrote several versions on Day 17 and, eventually, I translated my friend's Python code. It seems that functional languages save a lot of mental energy, and translating from his code wasn't hard at all.

## Day 18 ##

From Day 18, things became more interesting. In Part 1 of Day 18, I finally had the chance to use the flood filling algorithm. You expand the whole map with one additional row up, one down, one column left, and one right. Then start from the (-1, -1) position and try to flood fill the map.

Part 2 made the input huge and I couldn't use the same logic. After chatting with my friends and exploring Reddit, I discovered the algorithm named Shoelace. I learned that it should be paired with Pick's theorem, but I didn't use it. I should learn it; it looks fun.

## Day 19 ##

Affected by last year's puzzle, where making a Lisp expression from the input and evaluating it gave the answer, I spent a long time writing the lambda functions with conditions from this year's Day 19 input. Part 1 is done. For Part 2, I needed a DFS with a few changes, taking all ranges as inputs and picking out all possible outcomes.

## Day 20 ##

Part 1 took me a lot of time because I was sleepy. Fortunately, some of the designs I chose made Part 2 easier. In Part 2, I needed to check the input and figure out which inputs for the '&' node that send a signal to the end (`rx`) would repeat. There were four of them; I printed them out and found their repeating steps. Then, I ran the least common multiple (LCM) of all of them. And on Day 20, Part 2, I jumped to number 2000 on the leaderboard. I think it's my best this year (except for Day 25, Part 2).

## Day 21 ##

For Part 1, I just reused my Day 18 flood fill. Part 2 is pretty hard. Actually, AoC became much harder from Day 21 onwards.

I failed, so I went to Reddit and figured out the output actually repeated as a multivariate polynomial equation. The person I followed used a rule called Cramer's rule. It seems fun to learn as well.

## Day 22 ##

In Part 1, a missing line kept me debugging the whole day. For Part 2, I realized I needed to rewrite most of my code, so I just translated my friend's Python code.

## Day 23 ##

Like on Day 17, Part 1 was fine. Part 2 presented several issues, such as trying to create a specific sort function to sort a queue, which failed; I resorted to list sort instead of using a heap queue (because I didn't want to learn cl-heap), which also failed. Eventually, I had to learn it and rewrite my code. I also had to use my own hash-set (I wrote it years ago, but it needed additional functions because I wanted to write my own hash-set; the one I used before had a bug, and my fix PR has been ignored for 4 years).

After all these changes, I still encountered a block; my SBCL returned the memory issue again. It was so disappointing, so I had to ask for help from my friend again.

## Day 24 ##

For Part 1, I needed to solve a linear equation with two variables from the inputs, find the crossing point, and check if it lies in the feasible region.

Part 2, I just copied my friend’s Python code that used the z3-solver library. (I don’t even know what that is—something I need to learn.)

## Day 25 ##

Brute force again.

## End ##

There are some algorithms I want to learn because I hadn't heard of them before, and they seem fun:

+ Shoelace formula & Pick's theorem for calculating the area inside a shape.
+ Cramer's rule
+ Z3 solver

Next year, I am considering using Rust or OCaml along with some Lisp. So, I need to write some tool functions for my Rust codebase and some algorithms. 
