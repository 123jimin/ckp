from bench.util import bench, log_bench_result

from . import problems

problem_names = sorted(p for p in dir(problems) if p.startswith('p'))
print(f"Benchmarking {len(problem_names)} {'problem' if len(problem_names) == 1 else 'problems'}...")

for problem_name in problem_names:
    curr_problem = getattr(problems, problem_name)

    times = bench("curr_test()", num_trials=8, log=False, global_vars={'curr_test': curr_problem.test})
    log_bench_result(f"Problem #{problem_name[1:]}", times)