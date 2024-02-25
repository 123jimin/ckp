"""
    Functions for micro-benchmarking.
"""

import timeit, statistics

def log_bench_result(label:str, times:list[float]):
    print(f"{label}: {statistics.mean(times):.3f} \xB1 {statistics.stdev(times):.3f} s")

def bench(codes:str|list[str], repeats_per_trial=1, num_trials=5, *, log:bool = True) -> list[float]:
    is_list = isinstance(code, list)
    if not is_list: codes = [codes]
    times: list[list[float]] = [[] for _ in codes]

    for _ in range(num_trials):
        for i, code in enumerate(codes):
            times[i].append(timeit.timeit(code, globals=globals(), number=repeats_per_trial))
    
    if log:
        for code, time in zip(codes, times):
            log_bench_result(code, time)

    return times if is_list else times[0]