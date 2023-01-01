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

### Day 11 ###

It is easy to implement day 11 if the language can use lambda. I let each monkey become a list that contained all items, the operation (lambda), and the test (lambda). Then, the solution is straight forward. 

### Day 12 ###

I write the recursive function at beginning and the status are complex because I used hash-table as record. In common lisp, get the value of hash-table can give the nil (None), and I have to make sure the value after I check if it is nil (None) or not. Just very tricky. So I use another way, an queue, to do day 12.

### Day 13 ###

Day 13 part1 is my favorite. The data input format is so lispy. 

```lisp
(defun replace-input (input)
  (str:replace-all
   "," " "
   (str:replace-all
	"]" ")"
	(str:replace-all "[" "(" input))))

(defun read-one-input (input)
  (read-from-string input))
```

Just the code upper, can change the data input to lisp code. Then I need a compare function to compare the value depends on the type (integer, cons, etc.)

I don't like the part2 because it is too inconsistent. It is easy to get the answer by just using the "sort by" which implemented by a lot languages nowadays. But it means if someone don't know how to use it, and want to brute force all positions. There are a lot options that can be used to insert. 

### Day 14 ###

Day 14 is fun. Not tricky, just fun.

### Day 15 ###

Day 15 logic is
1. find the closest B with S
2. get the Manhattan distance from B to S
3. draw the map. 

The tricky part is part2. I need to find the empty point inside the map. So I loop all row and col and the S-B pair to find the empty point. The Big O is row * col * S-B pairs. It takes a long time. And I find in each row, if I find one point's related S-B, and I can just jump forward depends on the distance from S and B. And after this tiny change. the result appears. Not very fast, but fast enough.

I learned something from the part2, The Big O actually doesn't change, just optimize a bit in each loop can also give a big improvement. 

### Day 16 ###

I failed.

### Day 17 ###

Day 17, I change language from common lisp to Rust. Day 17 is hard, and several tricks inside.

First trick, it is Tetris. Second trick, every line is 7 spots, which means if they are bits, a full line is `1111111`. 

Then the first part has a easy way to determine if this Rock can keep going down or not. When rock reach the old rocks (after 4 steps), put the highest line into the buffer, and compare the buffer with the rock line to line. Each line does `!(a | b == a + b)`, if it is true, means this rock cannot reach this deep. Then rock go back one step, and stop there, and update the results. 

Part 2 looks like hard but actually I noticed the trick when I saw it. It repeats. Means if I split the rock tower with the fulled line (`1111111`), it is going to repeat the height from last fulled line to the next one like x, a, b, c, d, a, b, c, d, etc. So do the rocks number. So I need minus the first rock number of height x, and divide the (a\_rocknum + b\_rocknum + c\_rocknum + d\_rocknum) to get the repeat time. Then module the rocks number to get the real very small input. The get the height of the input and add the x + (a + b + c + d) * repeat.

### Day 18 ###

Part 2 is tricky. Has to use algorithm [Flood fill](https://en.wikipedia.org/wiki/Flood_fill)

### Day 19 ###

Recursive recursive and recursive.

### Day 20 ###

I write day 20 in lisp at beginning, but with the circle list. Find the next number which should be move. It looks good but I forget there might be duplicated numbers. So each number should has flag shows if this number has moved or not.

### Day 21 ###

Day 21 part 1, I use a hash table keep each expression, and keep looping the hash table until all values are number. 

Then part 2 cannot use this brute force, I tried to guess the number but it runs forever. So, the solution is: root node has two arguments, one of it we already know. I just need to reverse back from the root to humn node. 

More interesting is I write part 2 with a lisp parser. Each key can be a lisp expression then reverse back and get the answer isn't that hard. Further more, I re-write part 1 with this solution and get the part 1 result just a `eval` in lisp. 

### Day 22 ###

A lot code in part 1, and when I saw the part 2, I give up.

### Day 23 ###

The hardest part is understanding the meaning of puzzle.

### Day 24 & 25 ###

I give up.

## End ##

I give up right before the end. What a pity. However, I think I will join the next years AOC again for fun. I have several thoughts about AOC this year. 

1. I think some game developers make puzzles of 2022. For example, day22 part2 3D map moving; day 18 part2, 3D surface detection. Just too obviously to use in the game developing. And day17, Tetris.
2. Some algorithm appear often in this year's solutions. BFS/DFS/Dijkstra/etc. straight forward brute force solution cannot solve all puzzles.
3. Even tiny optimization can lead to the huge improvement. Even the Big O doesn't change. 
