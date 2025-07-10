""" Strategy to print shortest possible Aheui code. """

from functools import cache

AHEUI_NUMERALS = ('반반타', '발밤타', '반', '받', '밤', '발', '밦', '밝', '밣', '밞')

@cache
def aheui_get_naive_nonneg(n: int) -> str:
    """ Returns code that pushes `n` on the stack. """
    assert(0 <= n)

    if n < len(AHEUI_NUMERALS): return AHEUI_NUMERALS[n]
    if n <= 2*(len(AHEUI_NUMERALS)-1):
        m = n // 2
        return AHEUI_NUMERALS[m] + AHEUI_NUMERALS[n-m] + "다"
    
    for d in range(9, 1, -1):
        if n%d == 0: return AHEUI_NUMERALS[d] + aheui_get_naive_nonneg(n // d) + "따"
    
    if n%9 < 2 and n%8 >= 2:
        return AHEUI_NUMERALS[n%8] + AHEUI_NUMERALS[8] + aheui_get_naive_nonneg(n//8) + "따다"
    
    return AHEUI_NUMERALS[n%9] + AHEUI_NUMERALS[9] + aheui_get_naive_nonneg(n//9) + "따다"

@cache
def aheui_make_naive_from(top: int|None, value: int) -> str:
    if top is None: return min((AHEUI_NUMERALS[top] + aheui_make_naive_from(top, value) for top in range(2, 10)), key=len)
    if top == value: return ""
    if not value: return "빠타"
    if value == 1: return "빠나"
    if 2 <= value <= 9: return "마" + AHEUI_NUMERALS[value]
    if top*top == value: return "빠따"

    candidates = []
    if value > top:
        candidates.append(aheui_get_naive_nonneg(value - top) + "다")

        if value % top == 0:
            candidates.append(aheui_get_naive_nonneg(value // top) + "따")
        else:
            candidates.append(aheui_get_naive_nonneg(value // top) + "따" + aheui_get_naive_nonneg(value % top) + "다")
            candidates.append(aheui_get_naive_nonneg(1 + value // top) + "따" + aheui_get_naive_nonneg(top - value % top) + "타")
    else:
        candidates.append(aheui_get_naive_nonneg(top - value) + "타")

    return min(candidates, key=len)

@cache
def aheui_make_from(top: int|None, value: int, effort: int = 0) -> str:
    if top is None:
        if 0 <= value < 200: return aheui_make_naive_from(None, value)
        return min((AHEUI_NUMERALS[top] + aheui_make_from(top, value, effort) for top in range(2, 10)), key=len)
    if top == value: return ""
    if not value: return "빠타"
    if value == 1: return "빠나"
    if 2 <= value <= 9: return "마" + AHEUI_NUMERALS[value]
    if 2 <= value-top <= 9: return AHEUI_NUMERALS[value-top] + "다"
    if 2 <= top-value <= 9: return AHEUI_NUMERALS[top-value] + "타"
    if value%top == 0 and 2 <= value//top <= 9: return AHEUI_NUMERALS[value//top] + "따"
    if top*top == value: return "빠따"
    
    if not effort: return aheui_make_naive_from(top, value)

    candidates = [aheui_make_from(top, value, effort-1)]
    if value > top:
        candidates.append(aheui_make_from(None, value-top, effort-1) + "다")

        if value % top == 0:
            candidates.append(aheui_make_from(None, value//top, effort-1) + "따")
            candidates.append("빠" + aheui_make_from(top, value//top, effort-1) + "따")
        else:
            candidates.append(aheui_make_from(None, value//top, effort-1) + "따" + aheui_make_from(top*(value//top), value, effort-1))
            candidates.append(aheui_make_from(None, 1 + value//top, effort-1) + "따" + aheui_make_from(top*(value//top+1), value, effort-1))
            
            candidates.append("빠" + aheui_make_from(top, value//top, effort-1) + "따" + aheui_make_from(top*(value//top), value, effort-1))
            candidates.append("빠" + aheui_make_from(top, 1 + value//top, effort-1) + "따" + aheui_make_from(top*(value//top+1), value, effort-1))
    else:
        candidates.append(aheui_make_from(None, top-value, effort-1) + "타")

    return min(candidates, key=len)

def aheui_from_vals(arr: list[int]) -> list[str]:
    prev_val = None
    result: list[str] = []
    for x in arr:
        if prev_val is None:
            result.append(aheui_make_from(None, x, 4))
        else:
            from_none = aheui_make_from(None, x, 4)
            from_prev = aheui_make_from(prev_val, x, 4)
            if len(from_none) < len(from_prev)+1:
                result.append(from_none)
            else:
                result[-1] += "빠"
                result.append(from_prev)
        prev_val = x
    return result