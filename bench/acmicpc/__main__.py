import argparse, cProfile
from bench.util import bench, stdev_range

parser = argparse.ArgumentParser(prog="bench.acmicpc", description="Benchmark CKP with one or more problems from acmicpc.net")
parser.add_argument('problem_name', help="specify this to benchmark a specific problem", nargs='?')
parser.add_argument('-p', '--profile', help="set this flag to profile (instead of benchmarking)", action='store_true')

args = parser.parse_args()

from . import problems

if args.problem_name:
    problem_name = args.problem_name
    if not problem_name.startswith('p'):
        problem_name = 'p' + ('0' * max(0, 5 - len(problem_name))) + problem_name
    problem_names = [problem_name]
else:
    problem_names = sorted(p for p in dir(problems) if p.startswith('p'))

print(f"{'Profiling' if args.profile else 'Benchmarking'} {len(problem_names)} {'problem' if len(problem_names) == 1 else 'problems'}...")

for problem_name in problem_names:
    curr_problem = getattr(problems, problem_name)

    if args.profile:
        print(f"## Profile stats for Problem #{problem_name[1:]}:")
        cProfile.run("[curr_problem.bench() for _ in range(5)]", sort='tottime')
    else:
        times = bench(curr_problem.bench, num_trials=10, log=False)
        print(f"Problem #{problem_name[1:]}", stdev_range(times))