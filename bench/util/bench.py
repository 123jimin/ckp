from typing import Callable, TypeAlias, List, Any, Dict
import timeit

from .stat_list import StatList

BenchTarget: TypeAlias = Callable | str

def bench(
    stmts: List[BenchTarget] | BenchTarget,
    repeats_per_trial: int = 1,
    num_trials: int = 5,
    *,
    timer = timeit.default_timer,
    global_vars: Dict[str, Any] | None = None,
    log: bool = True,
) -> List[StatList] | StatList:
    """ Run micro-benchmarks and return timing statistics. """
    stmts_list = [stmts] if (single := not isinstance(stmts, list)) else stmts
    stats = [StatList(name=getattr(s, "__name__", f"Code #{i}")) for i, s in enumerate(stmts_list, 1)]
    timers = [timeit.Timer(stmt, timer=timer, globals=(global_vars or globals())) for stmt in stmts_list]
    for _ in range(num_trials):
        for s, t in zip(stats, timers): s.append(t.timeit(number=repeats_per_trial))
    if log: print(StatList.format_list_analysis(stats, measure_unit="sec"))
    return stats[0] if single else stats