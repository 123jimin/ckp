import re

from .strategy import aheui_get_naive_nonneg

def aheui_from_vals(arr: list[int]) -> list[str]:
    return list(map(aheui_get_naive_nonneg, arr))

def aheui_from_text(text: str) -> str:
    arr_val: list[int] = []
    arr_is_int: list[bool] = []
    for match in re.finditer(r"(0)|([1-9][0-9]*)|(-[1-9][0-9]*)|(.)", text):
        match match.groups():
            case (zero, None, None, None): arr_val.append(0); arr_is_int.append(True)
            case (None, pos, None, None): arr_val.append(int(pos)); arr_is_int.append(True)
            case (None, None, neg, None): arr_val.append(int(neg)); arr_is_int.append(True)
            case (None, None, None, ch): arr_val.append(ord(ch)); arr_is_int.append(False)
    chunks: list[str] = []
    for (chunk, is_int) in zip(aheui_from_vals(arr_val), arr_is_int):
        chunks.extend((chunk, "망" if is_int else "맣"))
    return "".join(chunks)