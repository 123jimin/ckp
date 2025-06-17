"""
    Functions for micro-benchmarking.
"""

import timeit, statistics
from typing import Dict, List, Callable

def stdev_range(times: List[float]):
    return f"{statistics.mean(times):.3f} \xB1 {statistics.stdev(times):.3f} s"

def bench(stmts: List[Callable|str]|Callable|str, repeats_per_trial=1, num_trials=5, *, global_vars = None, log:bool = True) -> List[List[float]]|List[float]:
    is_list = isinstance(stmts, list)
    if not is_list: stmts = [stmts]

    times: List[List[float]] = [[] for _ in stmts]
    timers = [timeit.Timer(stmt, globals=(global_vars or globals())) for stmt in stmts]

    for _ in range(num_trials):
        for i, timer in enumerate(timers):
            times[i].append(timer.timeit(number=repeats_per_trial))
    
    if log:
        for stmt, time in zip(stmts, times):
            print(getattr(stmt, '__name__', None) or str(stmt), stdev_range(time))

    return times if is_list else times[0]