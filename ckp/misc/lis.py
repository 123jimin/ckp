from bisect import bisect_right

def lis(A: list):
    """
        Returns indices of longest increasing subsequence of A.
        * Time complexity: O(n log n)
    """

    if not A: return []

    L = [0]
    P = [None] * len(A)

    for i in range(1, len(A)):
        if j := bisect_right(L, A[i], key=lambda v: A[v]):
            P[i] = L[j-1]
        if j == len(L): L.append(j)
        else: L[j] = i

    v = L[-1]
    V = []
    while v is not None: V.append(v); v = P[v]
    
    return V[::-1]