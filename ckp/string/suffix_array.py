def suffix_array_divide_conquer(s: str|list[int], cyclic: bool = False) -> list[int]:
    """
        Returns the suffix array of the string `s`. Runtime complexity: `O(n*log(n))` 
        If `cyclic` is `True`, the suffix array will be based on the cyclic suffixes of `s`.
    """

    L = len(s)

    if L == 0: return []
    if L == 1: return [0]

    q_lookup = dict[str|int, int]()
    q_buckets = list[list[int]]()

    for i in range(L):
        c = s[i]
        if (ind := q_lookup.get(c)) is None:
            q_lookup[c] = len(q_buckets)
            q_buckets.append([i])
        else:
            q_buckets[ind].append(i)
    
    if cyclic:
        qc = 0
    else:
        L += 1
        qc = 1

    q = [0] * L
    for (_, i) in sorted(q_lookup.items()):
        for j in q_buckets[i]: q[j] = qc
        qc += 1

    w = 1
    while w < L:
        q_lookup.clear(); q_buckets.clear()
        j = w

        for i in range(L):
            c = q[i]*qc + q[j]
            if (ind := q_lookup.get(c)) is None:
                q_lookup[c] = len(q_buckets)
                q_buckets.append([i])
            else:
                q_buckets[ind].append(i)
            if (j := j+1) == L: j = 0
        
        qc = 0
        for (_, i) in sorted(q_lookup.items()):
            for j in q_buckets[i]: q[j] = qc
            qc += 1

        w *= 2
    
    if cyclic:
        p = [0] * L
        for i in range(L): p[q[i]] = i
        return p

    p = [0] * (L-1)
    for i in range(L):
        if q[i]: p[q[i]-1] = i

    return p

class SuffixArrayData:
    """ Contains data for storing suffix array and LCP. """

    __slots__ = ('str', 'suffix', 'suffix_pos', 'lcp')

def suffix_array_init(s: str):
    """
        Creates a suffix array based on `s`.
    """
    pass