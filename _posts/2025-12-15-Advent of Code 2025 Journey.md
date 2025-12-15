---
layout: post
title: Advent of Code 2025 Journey
---

This is the year that AOC changed to 12 days. I kind of understand why the AOC team did it, but I still feel a bit sad that all parties truly have an ending, don't they?

## Day 1

Part 1 was pretty easy because Lisp's modulo can get the answer directly. Modulo on negative numbers is always charming to me. Part 2 wasted me a lot of time. I was trying to find a formula to get the answer, but it kept failing me. So I went back to my best friend, brute force, and got the answer with a lot of loops.

## Day 2

No special trick, cut the string with a length that can be divided by the full length. Then check if they are equal or not.

## Day 3

This day's Part 2 needed some dynamic programming (I like to call it cache-ism). My machine's memory would run out because Lisp cannot garbage collect memory that is still in use by recursion. It makes sense because it's still being used, right?

Then I found that the positions in the sequence are fixed; the first result of my recursion is always the maximum value. So I just picked the first one returned from the function. This reduced the cache size and memory usage, and then I got the answer.

## Day 4

Most of my time was spent reviewing my AOC map tools library that I wrote before. After that, the solution was pretty straightforward.

## Day 5

Part 1: It took me some time because I thought it wanted the "spoiled" number (such a stupid mistake). I needed to add `(- (length ..) ...)`.

Part 2: The range problems. I remember seeing them several times in AOC.

## Day 6

This day was pretty straightforward, but the code was pretty ugly. Then I had an idea to treat the input as a big matrix and transpose it. After the transpose, the input looked clearer, and I could use my debugger (print).

## Day 7

Since this day, puzzles became more interesting and tougher. I thought Part 2 was a factorial problem, but it was actually addition.

Each teleporter just creates two forks, each keeping the possible path number from the input. For example, if the input has 3 possible ways to reach it, the output will be two '3's on each side of the teleporter. Then, just sum them.

## Day 8

I used my graph library and brute force.

Then my friend recommended an algorithm called `union-find`. So I rewrote a new version afterward and added the union-find algorithm to my tools library.

## Day 9

Part 1 was simple; Part 2 I gave up.

I found the Python `Shapely` library to be exactly what I needed for Part 2.

## Day 10

Part 2 took a lot of time, and I had to rewrite it in Rust. Even then, it took several hours to get the answer. It must have some good solution for it; my friend told me [this solution](https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/) is pretty ingenious.

## Day 11

Part 1 was easy; I just used my graph library.

Part 2 took a lot of time and involved brainstorming many ideas. Just the moment I went to bed, my friend in the chat group mentioned that simply caching the ID/has-DAC/has-FFT could get the answer. I never thought to cache those two flags.

## Day 12

I gave up immediately when I saw this day's puzzle.

But I was still brainstorming in the chat group. Then, another friend found that if you just check if all shapes' areas are larger than the region's area, you can get the answer. And it worked for me.

This solution cannot pass the demo, but it can pass the real input. They definitely did it on purpose.

What a big troll, LOL.

## Wrap-Up

I think because this year only had 12 days, the difficulty curve was steep. But it was still fun. As every year before, I learned something.
