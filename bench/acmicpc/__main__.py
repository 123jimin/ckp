import argparse, cProfile
from typing import Any
from bench.util import bench, stdev_range

parser = argparse.ArgumentParser(prog="bench.acmicpc", description="Benchmark CKP with one or more problems from acmicpc.net")
parser.add_argument('problem_name', help="specify this to benchmark a specific problem", nargs='?')
parser.add_argument('-i', '--interleave', help="interleave execution of benchmark problems", action='store_true') # TODO: implement this
parser.add_argument('-t', '--tag', help="filter problems by tag")
parser.add_argument('-p', '--profile', help="set this flag to profile (instead of benchmarking)", action='store_true')

def filter_problem_tag(filter_tag: str|None, problem):
    if filter_tag is None: return True
    if (tags := getattr(problem, 'tags', None)) is None: return True
    return any(tag.lower() == filter_tag for tag in tags)

def do_setup(problem):
    if (problem_setup := getattr(problem, 'setup', None)): problem_setup()

def do_profile(label: str, problem):
    do_setup(problem)

    print(f"## Profile stats for {label}:")
    cProfile.runctx("for _ in range(10): f()", {'f': getattr(problem, 'bench')}, {}, sort='tottime')

def do_bench(problem_pairs: list[tuple[str, Any]]):
    for (_name, problem) in problem_pairs: do_setup(problem)
    
    times_list = bench([getattr(problem, 'bench') for (_name, problem) in problem_pairs], log=False)
    for ((name, _problem), times) in zip(problem_pairs, times_list):
        print(f"{name}:", stdev_range(times))

args = parser.parse_args()
filter_tag = args.tag.lower() if args.tag else None

from . import problems

problem_names: list[str] = []

if args.problem_name:
    problem_name = args.problem_name
    if not problem_name.startswith('p'):
        problem_name = 'p' + ('0' * max(0, 5 - len(problem_name))) + problem_name
    problem_names = [problem_name]
else:
    problem_names = sorted(p for p in dir(problems) if p.startswith('p'))

problem_list = [(f"Problem #{name[1:]}", getattr(problems, name)) for name in problem_names]
problem_list = [(name, problem) for (name, problem) in problem_list if filter_problem_tag(filter_tag, problem)]
problem_count_str = f"{len(problem_list)} {'problem' if len(problem_list) == 1 else 'problems'}"

if args.profile:
    print(f"Profiling {problem_count_str}...")
    for (name, problem) in problem_list:
        do_profile(name, problem)
else:
    print(f"Benchmarking {problem_count_str}...")
    if args.interleave:
        do_bench(problem_list)
    else:
        for pair in problem_list:
            do_bench([pair])