def matrix_chain_min_cost_naive(v: list[int]) -> int:
    assert(len(v) >= 3)
    if len(v) == 3: return v[0]*v[1]*v[2]
    
    D = [[0]*(len(v)-1), [v[i] * v[i+1] * v[i+2] for i in range(len(v)-2)]]
    
    for l in range(3, len(v)):
        D.append(d := [])
        dap = d.append
        for i in range(len(v)-l):
            w = v[i]*v[i+l]; dap(min(D[p-1][i] + D[l-p-1][i+p] + w*v[i+p] for p in range(1, l)))
    
    return D[-1][0]