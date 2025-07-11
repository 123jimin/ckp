""" Strategy to print shortest possible Aheui code. """

from functools import cache
import math, itertools
from typing import Callable

AHEUI_NUMERALS = ('반반타', '발밤타', '반', '받', '밤', '발', '밦', '밝', '밣', '밞')

def aheui_generate_small_optimal_codes() -> list[dict[int, str]]:
    """ Creates a database of optimal Aheui codes for small integers, for code length 1/3/5. """
    optimal_codes: list[dict[int, str]] = [
        {i: AHEUI_NUMERALS[i] for i in range(2, 10)},
        len_3 := dict(),
        len_5 := dict(),
    ]

    for i in range(2, 10):
        for j in range(2, 10):
            for (c, k) in (("다", i+j), ("따", i*j), ("타", i-j)):
                if 2 <= k <= 9: continue
                if k in len_3: continue
                len_3[k] = AHEUI_NUMERALS[i] + AHEUI_NUMERALS[j] + c
    
    for (v, code) in len_3.items():
        if v < 10: continue
        v_sq = v*v
        if v_sq in len_3: continue
        len_5[v_sq] = code + "빠따"

    for i in range(2, 10):
        i_code = AHEUI_NUMERALS[i]
        for (j, j_code) in len_3.items():
            for (new_code, k) in (
                (i_code + j_code + "다", i+j),
                (i_code + j_code + "따", i*j),
                (i_code + j_code + "타", i-j),
                (j_code + i_code + "타", j-i),
            ):
                if 2 <= k <= 9: continue
                if k in len_3 or k in len_5: continue
                len_5[k] = new_code

    return optimal_codes

AHEUI_SMALL_OPTIMALS = aheui_generate_small_optimal_codes()
AHEUI_DIV_OPPORTUNITY = {
    k//d: k
    for k in AHEUI_SMALL_OPTIMALS[2].keys()
    for d in range(2, 10)
}

@cache
def aheui_push_nonneg_int_naive(n: int) -> str:
    assert(n >= 0)

    for small_optimals in AHEUI_SMALL_OPTIMALS:
        if (code := small_optimals.get(n)): return code

        for i in range(9, 1, -1):
            if (code := small_optimals.get(n-i)): return code + AHEUI_NUMERALS[i] + "다"
            if (code := small_optimals.get(n+i)): return code + AHEUI_NUMERALS[i] + "타"
    
    n_sqrt = math.isqrt(n)
    if n_sqrt*n_sqrt == n: return aheui_push_nonneg_int_naive(n_sqrt) + "빠따"

    for d in range(9, 1, -1):
        if n%d == 0: return AHEUI_NUMERALS[d] + aheui_push_nonneg_int_naive(n // d) + "따"
    
    if n%9 < 2 and n%8 >= 2:
        return AHEUI_NUMERALS[n%8] + AHEUI_NUMERALS[8] + aheui_push_nonneg_int_naive(n//8) + "따다"
    
    return AHEUI_NUMERALS[n%9] + AHEUI_NUMERALS[9] + aheui_push_nonneg_int_naive(n//9) + "따다"

@cache
def aheui_push_neg_int_naive(n: int) -> str:
    assert(n < 0)
    
    for small_optimals in AHEUI_SMALL_OPTIMALS:
        if (code := small_optimals.get(n)): return code

        for i in range(9, 1, -1):
            if (code := small_optimals.get(i-n)): return AHEUI_NUMERALS[i] + code + "타"
    
    for d in range(9, 1, -1):
        if n%d == 0: return AHEUI_NUMERALS[d] + aheui_push_neg_int_naive(n // d) + "따"

    return "반" + aheui_push_nonneg_int_naive(2-n) + "타"

def aheui_push_int_naive(n: int) -> str:
    """
        Returns any "good enough" Aheui code that pushes `n` onto an empty stack.
    """
    if n < 0: return aheui_push_neg_int_naive(n)
    else: return aheui_push_nonneg_int_naive(n)

# Minimal and maximal values where the function is optimal between them.
aheui_push_int_naive.min_optimal = -418
aheui_push_int_naive.max_optimal = 459

def aheui_push_int_from_trivial(top: int, value: int) -> str:
    """ Returns trivially optimal code that pushes `value` onto a stack, replacing `top`. """

    ## len == 0 ##
    if top == value: return ""

    # No further improvements possible for top == 0
    if not top:
        for optimals in AHEUI_SMALL_OPTIMALS:
            if (code := optimals.get(value)): return "마" + code
        return None
    
    ## len == 2 ##
    if 2 <= value <= 9: return "마" + AHEUI_NUMERALS[value]
    if not value: return "빠타"
    if value == 1: return "빠나"
    if top*top == value: return "빠따"

    if 2 <= (delta := value-top) <= 9: return AHEUI_NUMERALS[delta] + "다"
    if 2 <= (delta := top-value) <= 9: return AHEUI_NUMERALS[delta] + "타"
    if value%top == 0 and 2 <= (d := value//top) <= 9: return AHEUI_NUMERALS[d] + "따"
    if 2 <= (d := top//value) <= 9 and top//d == value: return AHEUI_NUMERALS[d] + "나"

    ## len == 3 ##
    if 2 <= (n := top+value) <= 9: return AHEUI_NUMERALS[n] + "파타"
    if 2 <= (n := top*value) <= 9: return AHEUI_NUMERALS[n] + "파나"

    return None

def aheui_push_int_from_naive(top: int|None, value: int) -> str:
    if top is None: return aheui_push_int_naive(value)
    if (code := aheui_push_int_from_trivial(top, value)) is not None: return code

    # Only attempt the simplest strategies.
    return min(
        "마" + aheui_push_int_naive(value),
        aheui_push_int_naive(value-top) + "다",
        aheui_push_int_naive(top-value) + "타",
        key=len
    )

def _aheui_push_int_get_strategies(func: Callable[[int|None, int, int], str], top: int, value: int):
    # Assume that (top, value) is not trivial.

    yield "마" + func(None, value)
    if not top: return
    if not value: return

    yield func(top, value)

    for d in range(2, 10):
        yield func(top, value-d, 2) + AHEUI_NUMERALS[d] + "다"
        yield func(top, value+d, 2) + AHEUI_NUMERALS[d] + "타"
        
        yield AHEUI_NUMERALS[d] + "다" + func(top+d, value, 2)
        yield AHEUI_NUMERALS[d] + "타" + func(top-d, value, 2)
        yield AHEUI_NUMERALS[d] + "따" + func(top*d, value, 2)
        yield AHEUI_NUMERALS[d] + "나" + func(top//d, value, 2)

    yield func(None, value-top) + "다"
    yield "빠" + func(top, value-top, 2) + "다"

    yield func(None, top-value) + "타"
    yield "빠" + func(top, top-value, 2) + "타"

    if value%top == 0:
        yield func(None, value//top) + "따"
        yield "빠" + func(top, value//top) + "따"
    else:
        yield func(None, value//top) + "따" + func((value//top)*top, value, 2)
        yield "빠" + func(top, value//top) + "따" + func((value//top)*top, value, 2)

        yield func(None, 1+value//top) + "따" + func((1+value//top)*top, value, 2)
        yield "빠" + func(top, 1+value//top) + "따" + func((1+value//top)*top, value, 2)

    if abs(value) >= 100:
        value_sqrt = math.isqrt(abs(value))
        for i in range(10):
            target_0 = value_sqrt - i
            target_1 = value//target_0
            mul = target_0*target_1
            rest = func(mul, value, 2)

            yield func(top, target_0) + "빠" + func(target_0, target_1, 1 if value > 0 else 2) + "따" + rest
            yield func(top, target_1) + "빠" + func(target_1, target_0, 1 if value > 0 else 2) + "따" + rest

            if target_1 == target_0 + 1:
                yield func(top, target_0) + "빠빠따다" + rest
                yield func(top, target_1) + "빠빠따파타" + rest

    if value >= 500 and (target := AHEUI_DIV_OPPORTUNITY.get(value)):
        d = target // value
        assert(target // d == value)
        yield func(top, target) + func(None, d) + "나"

    yield "빠따" + func(top*top, value)

@cache
def aheui_push_int_from(top: int|None, value: int, effort: int = 0) -> str:
    if top is None:
        for optimals in AHEUI_SMALL_OPTIMALS:
            if (code := optimals.get(value)): return code

        naive_code = aheui_push_int_naive(value)
        if aheui_push_int_naive.min_optimal <= value <= aheui_push_int_naive.max_optimal: return naive_code

        return min(
            naive_code,
            *(AHEUI_NUMERALS[top] + aheui_push_int_from(top, value, effort) for top in range(2, 10)),
            key=len
        )

    if (code := aheui_push_int_from_trivial(top, value)) is not None: return code

    next_func = lambda top, value, delta=1: aheui_push_int_from(top, value, new_effort) if (new_effort:=effort-delta) >= 0 else aheui_push_int_from_naive(top, value)
    return min(_aheui_push_int_get_strategies(next_func, top, value), key=len)

# Minimal and maximal values where the function is optimal between them, for `effort == 2`.
aheui_push_int_from.min_optimal = -587
aheui_push_int_from.max_optimal = 1000

def aheui_stack_from_vals(arr: list[int], effort: int = 2) -> list[str]:
    prev = None
    codes = []

    for x in arr:
        from_none = aheui_push_int_from(None, x, effort)
        from_prev = "빠" + aheui_push_int_from(prev, x, effort)
        codes.append(min(from_none, from_prev, key=len))

        prev = x
    
    return codes

def aheui_from_vals(arr: list[int], effort: int = 2) -> list[str]:
    reuse_count = [0] * len(arr)
    codes = []
    stack = []
    
    for i in range(len(arr)):
        x = arr[i]
        from_none = aheui_push_int_from(None, x, effort)
        min_stack_ind = min(
            range(len(stack)),
            key=lambda si: len(aheui_push_int_from(arr[stack[si]], x, effort)),
            default=-1
        )
        
        min_ind = stack[min_stack_ind] if min_stack_ind >= 0 else -1
        from_stack_len = 1 + len(aheui_push_int_from(arr[min_ind], x, effort) if min_ind >= 0 else from_none)
        if from_stack_len < len(from_none):
            assert(min_stack_ind >= 0 and min_ind >= 0)
            reuse_count[min_ind] += 1
            stack = stack[:min_stack_ind]
            codes.append(aheui_push_int_from(arr[min_ind], x, effort))
        else:
            codes.append(from_none)
        
        stack.append(i)
    
    for i in range(len(codes)):
        codes[i] += "빠" * reuse_count[i]
    
    return codes