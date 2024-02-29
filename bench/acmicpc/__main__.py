import argparse
from bench.util import bench, log_bench_result

parser = argparse.ArgumentParser(prog="bench.acmicpc", description="Benchmark CKP with one or more problems from acmicpc.net")
parser.add_argument('problem_name', nargs='?')

args = parser.parse_args()

from . import problems

if args.problem_name:
    problem_name = args.problem_name
    if not problem_name.startswith('p'):
        problem_name = 'p' + ('0' * max(0, 5 - len(problem_name))) + problem_name
    problem_names = [problem_name]
else:
    problem_names = sorted(p for p in dir(problems) if p.startswith('p'))
print(f"Benchmarking {len(problem_names)} {'problem' if len(problem_names) == 1 else 'problems'}...")

for problem_name in problem_names:
    curr_problem = getattr(problems, problem_name)

    times = bench("bench()", num_trials=8, log=False, global_vars={'bench': curr_problem.bench})
    log_bench_result(f"Problem #{problem_name[1:]}", times)