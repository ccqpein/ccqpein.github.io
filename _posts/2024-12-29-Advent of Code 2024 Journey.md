---
layout: post
title: Advent of Code 2024 Journey
---

As is tradition with my friends, we were all excited leading up to the start of Advent of Code (AOC) 2024. Once again, we grouped together to tackle this year's challenges, sharing ideas and solutions along the way.

## Day 1, 2, and 3 ##

These first few days featured relatively straightforward solutions. However, I encountered an issue during Day 2; in SBCL (a Common Lisp implementation), I forgot that the `sort` function destructively modifies the original list. This minor oversight caused some bugs but was quickly resolved after debugging.

## Day 4 ##

I solved this question using my toolbox’s `map` function from `tools.lisp`. I have to say that the utility code I wrote years ago continues to prove invaluable during AOC. It’s always satisfying when past efforts come back to save the day.

## Day 5 ##

For Day 5’s puzzle, I utilized my graph code along with a custom sort function. I really appreciate the design of languages like Lisp that allow sorting with user-defined predicates. Similarly, tools like `sort_by` in Rust make solving such problems elegant and intuitive.

## Day 6 ##

The first challenging puzzle appeared on Day 6. While Part 1 was straightforward, Part 2 had me scratching my head. I attempted several solutions but kept running into incorrect results. 

Eventually, a friend suggested a clever trick: mark every point on the map with `#` and reprocess the calculations. If the step count exceeded 10,000, it would indicate an infinite loop. This approach worked, but my final output was still slightly off.

After debugging and comparing solutions with my friends, I realized I had missed an edge case: after a turning point, my logic immediately moved forward without rechecking for obstacles. The correct approach should have been to check, turn, and then validate the move in the next loop iteration. 

Interestingly, my incorrect logic still worked for Part 1, as it didn’t hit the edge case. It felt a bit like exploiting a "walk through walls" bug in a video game.

## Day 7 ##

On Day 7, I misinterpreted the puzzle’s instructions. The problem description stated:

> "Operators are always evaluated left-to-right, not according to precedence rules."

However, I initially implemented a solution that evaluated `*` before `+`, following standard precedence rules. This was not only incorrect but also made the puzzle unnecessarily more difficult. Once I fixed my misunderstanding, the solution flowed more easily.

Additionally, I decided to create a utility function based on Day 7’s logic, which you can find in my tools: [link](https://github.com/ccqpein/AdventOfCode/blob/335cc2d45e3a2226cef828e92626a1bd851df1c8/tools/tools.lisp#L135).

## Day 8 ##

This day’s puzzle leaned heavily on map manipulation, so I used my existing Map code to solve it efficiently.

## Day 9 ##

For Day 9, I went with my trusty old friend: brute force. While it worked, my first implementation of Part 2 was incredibly slow, taking over half an hour to run. I later optimized it and got the runtime down to 2 minutes—but clearly, there’s still room for improvement.

## Day 10 ##

This problem had a recursive solution, which I implemented directly. Clean and elegant.

## Day 11 ##

Part 2 of Day 11 initially crushed my stack and ran too slowly with my brute-force approach from Part 1. To address this, I introduced two caching mechanisms: one for intermediate results at 25 steps and another for 50 steps. Additionally, I used my LRU (Least Recently Used)macro to optimize function calls—similar to Python’s `functools.lru_cache`.

A friend shared their Python solution, which cached both the number and frequency of each level. I adapted their logic into Lisp, which sped up my Part 2 runtime from 20 seconds to just 0.025 seconds. I was amazed by the difference!

## Day 12 ##

This was a fun puzzle, and I even ended up adding a new function to my toolbox for map-related operations. [Check it out here](https://github.com/ccqpein/AdventOfCode/blob/335cc2d45e3a2226cef828e92626a1bd851df1c8/tools/tools.lisp#L450).

## Day 13 ##

When working on Part 1, I realized I could solve it using systems of linear equations with two variables. However, I was too lazy to write them out. Of course, I had to tackle them in Part 2 anyway! As a result, my Day 13-2 function could retroactively solve Part 1 as well.

The pure math solution rewarded me with my first top 2,000 ranking on the leaderboard. It was immensely satisfying.

## Day 14 ##

For Part 2, I considered reusing a strategy from past puzzles: ensuring no standalone points were left unconnected. However, this year’s problem introduced a twist—it required consideration of "most of the robots," which invalidated my initial approach.

A friend suggested checking for any line with ten consecutive points. The first occurrence matching this condition became my answer, and it worked perfectly.

## Day 15 ##

The puzzles noticeably increased in difficulty starting from Day 15. Part 1 was straightforward, but Part2 posed a frustrating challenge. It passed all example inputs but failed for the real input!

After comparing outputs with a friend, I pinpointed the discrepancies in my map-handling logic and corrected the bug.

## Day 16 ##

Part 1 was a standard Dijkstra implementation, while Part 2 cleverly leveraged the distance table from Part 1’s Dijkstra function. By pruning unnecessary points from the shortest path, I avoided redundant calculations.

## Day 17 ##

Day 17 was one of the most enjoyable puzzles—a throwback to old-style computer concepts. Part 2 took significant effort. After analyzing the problem, I hardcoded specific steps for my input and discovered a rule: the previous step `A` divided by 8 determined the next `A`. This insight made solving it much simpler.

## Day 18 ##

Another Dijkstra-based solution.

## Day 19 ##

This puzzle utilized a greedy algorithm combined with recursion. Clean and effective.

## Day 20 ##

Dijkstra appeared yet again, this time for calculating shortest steps between available spots on the map.

### Part 1 ###
I looped over all `#` elements on the map. If their vertical or horizontal neighbors were on the path and their saved steps exceeded 100, I counted them as "good."

### Part 2 ###
I checked if the Manhattan distance between the start and end points was less than 20. Additionally, the total saved steps needed to align with the adjusted distance calculations.

It made me want to write a generalized Dijkstra function for my map tools: [link](https://github.com/ccqpein/AdventOfCode/blob/335cc2d45e3a2226cef828e92626a1bd851df1c8/tools/tools.lisp#L386).

## Day 21 ##

Part 1 took me around an hour to implement, but I initially gave up on Part 2, thinking it wouldn’t fit within my memory constraints. 

Later, while lying in bed, the solution came to me: every level only handles one previous "bottom state," creating an elegant recursive pattern. I implemented what I called a "knot recursive" structure (a term I invented back when I played with Haskell), which worked beautifully.

## Day 22 ##

Brute force for the win.

## Day 23 ##

Another recursive solution.

## Day 24 ##

Day 24 Part 2 was unquestionably thehardest puzzle this year. The statistics backed up my feeling—many participants completed Part 1 but couldn’t finish Part 2. 

The input resembled an old-style calculator performing binary addition. While the logic was clear, debugging errors in the recursive checks for `z` values took painstaking effort. By treating each output node as an s-expression, and recursively validating the structure, I finally got the right output. This puzzle made me love Lisp even more.

## Day 25 ##

A straightforward conclusion to this year’s AOC.

## Wrap-Up ##

This year marked my first time finishing AOC without relying on Reddit for tips. Our small group of three stayed focused, discussing and solving the problems together. I enjoyed this year’s puzzles immensely, especially how many of them used recursive solutions. Recursive logic makes the code look clean and solving the puzzles feels deeply satisfying. 

Here’s to hoping for an equally enjoyable AOC 2025!
