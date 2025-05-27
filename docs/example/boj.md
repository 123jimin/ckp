# Using CKP to Solve BOJ Problems

Here are several example solutions for problems on [Baekjoon Online Judge](https://www.acmicpc.net/), demonstrating how CKP can be used to solve competitive programming problems.

## Problem 5615

> Submission ID: 86417301

```py
import sys
from ckp.number_theory import is_prime

print(sum(is_prime(2*int(sys.stdin.readline())+1) for _ in range(int(sys.stdin.readline()))))
```
