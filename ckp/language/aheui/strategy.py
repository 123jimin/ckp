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

