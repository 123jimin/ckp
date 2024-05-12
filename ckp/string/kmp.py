def kmp_build(pattern: str|list[int]) -> list[int]:
    N = len(pattern)
    table = [0] * (N+1)
    table[0] = -1

    j = 0
    
    for i in range(1, N):
        c = pattern[i]
        if c == pattern[j]:
            table[i] = table[j]
        else:
            table[i] = j
            while j >= 0 and c != pattern[j]: j = table[j]
        j += 1
    
    table[N] = j

    return table

def kmp_search(haystack: str|list[int], needle: str|list[int], kmp_table: list[int] = None):
    if not kmp_table: kmp_table = kmp_build(needle)

    N, j = len(needle), 0
    for i in range(len(haystack)):
        c = haystack[i]
        while j >= 0 and c != needle[j]: j = kmp_table[j]
        j += 1
        if j == N:
            yield i - (N-1)
            j = kmp_table[j]