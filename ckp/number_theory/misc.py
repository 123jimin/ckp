def iterate_idiv(x):
    """
        Yields tuples of ([x/i], i_begin, i_end), in a decreasing order for [x/i].

        In other words, when this function yields `(a, b, c)`, then `x//i == a` holds for all `i` precisely in `range(b, c)`. 

        Time complexity: O(sqrt(x))
    """
    prev_val = x
    prev_i = 1
    if x == 2:
        yield (2, 1, 2)
        yield (1, 2, 3)
        return
    for i in range(2, x+1):
        curr_val = x // i
        if curr_val == prev_val:
            prev_i = i-1
            break
        yield (prev_val, i-1, i)
        prev_val = curr_val
    for k in range(prev_val, 0, -1):
        ub = x//k
        yield (k, prev_i, ub+1)
        prev_i = ub+1