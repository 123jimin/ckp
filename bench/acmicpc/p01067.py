from ckp.fourier import ComplexCooleyTukeyFFT

import random
N = 30000

X = []
Y = []

def setup():
    global X, Y

    random.seed(42)
    X = [random.randint(0, 100) for _ in range(N)] * 2
    Y = [random.randint(0, 100) for _ in range(N)][::-1]

def bench():
    fft = ComplexCooleyTukeyFFT.get_common_fft(X, Y)
    fX = fft(X)
    fY = fft(Y)
    for i in range(len(fft)): fX[i] *= fY[i]
    Z = fft(fX, inverse=True)
    ans = max(round(abs(z)) for z in Z)
    assert(ans == 76038571)

tags = {'fft'}