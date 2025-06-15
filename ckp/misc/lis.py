from bisect import bisect_right

def lis(A: list):
    """
        Returns indices of longest increasing subsequence of A.
        * Time complexity: O(n log n)
    """

    if not A: return []

    L = []
    B = []
    P = [None] * len(A)

    for i, x in enumerate(A):
        if j := bisect_right(B, x): P[i] = L[j-1]
        if j == len(L): L.append(i); B.append(x)
        else: L[j] = i; B[j] = x

    v = L[-1]
    V = []
    while v is not None: V.append(v); v = P[v]
    
    return V[::-1]