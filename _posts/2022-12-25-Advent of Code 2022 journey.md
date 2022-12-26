---
layout: post
title: Advent of Code 2022 journey
---

As I did last year, I decided do AOC this year. I feel it is a bit harder than last year. This is just the journey of 2022 AOC. All code host on [here](https://github.com/ccqpein/AdventOfCode/tree/master/aoc2022)

### Day 1-6 ###

The logic is pretty straight forward. Just parse the input and write logic plainly in code. 

### Day 7 ###

After transitional warming up for 6 days, it becomes a bit more interesting in day 7. Day 7 is the tree problem. Different from days before, plain writing wasn't the best way. (Even I write it in the plain way). 

I use recursive and keep a hash table for recording of file/dir size. It works, but I think use a tree structure must be better solution.

### Day 8 & 9 ###

Day 8 logic is pretty easy just need a write bunch of code. Day 9 take me a while. I was using a stack for keep the status of directions of nodes of the line. However, I don't need it. There is a general way to [move close](https://github.com/ccqpein/AdventOfCode/blob/0b38c59520f876f562c4372f235a873acfab9c81/aoc2022/lisp-version/day9.lisp#L72) to head. After use that, only thing tricky is day9 part2' head-to-tail movement.

### Day 10 ###

Part 2 of day 10 is pretty fun. Check index every loop and go find if the index located inside the sprite (be calculated by part1 logic). And print letters eventually. I just like the print letter design. 



