# Numeric Functions

`ckp.numeric` contains constants and functions for accurate numeric computations.

## Convention

In this document, when a function `foo`'s signature is listed like this:

> `foo() -> float | fractions.Fractions | decimal.Decimal`

then it means that there are different versions of `foo` available to use:

- `foo() -> float` returns a float (IEEE 754 binary64), usually within $10^{-9}$ relative error (*not guaranteed*).
- `foo_exact() -> fractions.Fractions (or int)` returns an exact value.
- `foo_decimal() -> decimal.Decimal` returns a `decimal.Decimal` value, respecting current decimal context.

(Unfortunately, currently there's no function that returns values other than `float`.)

## Constants

CKP does not provide any global variables, neither does this package. Call the function and store the value to a global variable if you wish.

- `euler_gamma() -> float` returns the euler's constant $\gamma \simeq 0.57721 \, 56649$.
- `golden_phi() -> float` returns the golden ratio $\phi \simeq 1.61803 \, 39887$.
- `catalans_constant() -> float` returns the Catalan's constant $G = \sum_{n=0}^{\infty} \frac{(-1)^n}{(2n+1)^2} \simeq 0.91596 \, 55942$.

## Functions

> `log_falling_factorial(n: int, k: int) -> float`

Computes the log value of the falling factorial $(n)_k = n \times (n-1) \times \cdots \times (n-k+1) = \frac{n!}{(n-k)!}$.

Usually, `math.lgamma(n+1) - math.lgamma(n-k+1)` gives the desired answer, but when n is extremely large compared to k, that method would yield an incorrect result.

`log_falling_factorial` uses the following formula, based on Stirling's approximation.

$$\log \Gamma(z) = z \log z - z - \frac{1}{2} \log z + \frac{1}{2} \log 2 \pi + \frac{1}{12 z} + O(\frac{1}{z^3})$$

> `log_comb(n: int, k: int) -> float`

This function assumes that $0 \le k \le n$.

Computes $\log {n \choose k}$. Usually, `math.lgamma(n+1) - math.lgamma(n-k+1) - math.lgamma(k+1)` gives the desired answer, but when n is extremely large compared to k, that method would yield an incorrect result.

`log_comb` uses the same Stirling's approximation `log_falling_function` does.

> `harmonic_number(n: int) -> float`

Computes the n-th harmonic number $H_n = \sum_{i=1}^n \frac{1}{i}$ in constant time, using the following approximation.

$$H_n = \log n + \gamma + \frac{1}{2n} - \frac{1}{12n^2} + \frac{1}{120n^4} - \frac{1}{252n^6} + \frac{1}{240n^8} + \cdots$$

Every harmonic numbers are rational numbers, but the exact version of this function (returning `fractions.Fraction`) is *not* planned to be implemented, as it's practically useless.
