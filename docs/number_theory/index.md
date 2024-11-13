# Number Theory

Several functions receive `n_factors` as a parameter, which represents a previously-computed factorization of `n`.

When `n_factors` is given, then it would be regarded as the factorization of `n`. In this case, `n` should be either `0` or the original value that was used to obtain `n_factors`.

`n_factors` can either be a generator/list of prime factors (i.e. return value of `factor`), or a `collections.Counter` created from it.

## Arithmetic Functions

> `num_divisors(n: int, n_factors = None) -> int`

Returns the \# of divisors of n; equivalent but a bit faster than `len(list(divisors(n, n_factors)))`.

> `sum_divisors(n: int, n_factors = None) -> int`

Returns the sum of every divisors of n; equivalent but a bit faster than `sum(divisors(n, n_factors))`.

> `euler_phi(n: int, n_factors = None) -> int`

This is the Euler-phi function $\varphi(n)$, which returns \# of numbers $x$ coprime to $n$, such that $1 \le x < n$.

## Basic Modular Arithmatic

> Class `ZMod`

This is a convenient, yet quite slow (4x slower than simply using `%`), class for representing numbers in $\mathbb{Z}/m\mathbb{Z}$.

> `chinese_mod(*l: list[tuple[int, int]]) -> int`

Given $(a_1, m_1), (a_2, m_2), \cdots$, where $0 \le a_i < m_i$ and every pairs of $(m_i, m_j)$ for $i \ne j$ are coprime, returns an integer $x < m_1 \cdot m_2 \cdot \cdots$ such that $x \equiv a_i \pmod{m_i}$ for every $i$.

> `comb_mod_prime(n: int, k: int, p: int) -> int`

Given a prime number $p$, returns $\binom n k \pmod p$.

> `solve_linear_mod(a: int, b: int, m: int) -> int`

Returns the smallest integer $x$ such that $x \ge 0$ and $ax+b \equiv 0 \pmod m$.
Returns -1 if there's no such number.

## Primality Testing

An example of testing whether some numbers are primes:

```py
from ckp.number_theory import is_prime

# Prints `True`, `False`, and `True`.
print(is_prime(2), is_prime(2**32 + 1), is_prime(10**100 + 267))
```

> `is_prime(n: int) -> bool`

Returns whether `n` is a prime number. The best algorithm will be picked depending on `n`.

This is a probable primality test, but there's no known counter-example.

- Time Complexity: $\Theta(\log^4 n)$

### Specific Algorithms under `ckp.number_theory.primality_test`

> `is_prime_naive(n: int) -> bool`

Performs primality testing using trial division.

Do use this function instead of `is_prime` when `n` is small (million-ish) and you wish the full code to be small.

- Time Complexity: $\Theta(\sqrt n)$

> `is_prime_miller_rabin_with_base(n: int, al: list[int]) -> bool`

Returns whether `n` is a probable prime, using `al` as a list of bases for the Miller-Rabin test.

- Time Complexity: $\Theta(\log^4 n)$

## Prime Sieves

An implementation of the sieve of Eratosthenes. (TODO: implement a better prime sieves...?)

> `prime_sieve_init(max_n: int = 1)`

Create a new prime sieve for numbers up to `max_n`.

The sieve will be extended whenever needed, so providing `max_n` is not necessary.

Still, providing `max_n` is generally preferable for performance reason (less call to `prime_sieve_extend`).

> `prime_sieve_primes(sieve) -> Generator[int]`

Yields prime numbers inferable from the sieve.

> `prime_sieve_query(sieve, n: int) -> bool`

Check whether `n` is a prime number, querying `sieve`. When `n` is an odd number, the sieve might get extended.

> `prime_sieve_factor(sieve, n: int) -> Generator[int]`

Yields every prime factors of `n` with repeats, in *no particular order*.

> `prime_sieve_extend(sieve, max_n: int)`

Extend the sieve, so that the primality test up to `max_n` with this sieve can be done.

Other prime sieve functions call this function as needed, so calling this function is not necessary.

> Class `PrimeSieve`

A conveient class to manage prime sieves in an OOP manner.
Using this class is as efficient as using individual prime sieve functions, but impacker would emit a code with unused functions.

## Integer Factorization

An example of factoring some integers:

```py
from ckp.number_theory import factor

# Prints `2 2 2 3`.
print(*factor(24))

# Prints `3 415141630193 8142767081771726171`.
print(*factor(2**103 + 1))
```

Often, using `collections.Counter` is convenient, especially for obtaining the natural representation $\Pi {p_i}^{k_i}$.

```py
from collections import Counter

# Prints `(2, 3) (3, 2) (5, 1)`
f = Counter(factor(360))
print(*f.items())
```

An example of getting divisors of some integers:

```py
from ckp.number_theory import factor, divisors

# Prints `1 7 3 21 2 14 6 42`
print(*divisors(42))

# Prints all divisors of 360, twice.
print(*divisors(0, factor(360)))
print(*divisors(0, list(factor(360))))

from collections import Counter
# This also prints all divisors of 360.
print(*divisors(0, Counter(factor(360))))
```

> `factor(n: int) -> Generator[int]`

Yields every prime factors of `n` (with duplicates), in *no particular order*. The best algorithm will be picked depending on `n`.

> `divisors(n: int, n_factors = None) -> Generator[int]`

Yields every divisors of `n`, in *no particular order*.

### Specific Algorithms under `ckp.number_theory.factor`

> `factor_naive(n: int) -> Generator[int]`

Factor `n` using trial division.

> `factor_pollard_rho(n: int) -> Generator[int]`

Factor `n` using Pollard's rho algorithm.

> `pollard_rho_find_divisor(n: int, start: int = 2) -> int`

## Advanced Modular Arithmetic

> `legendre_symbol(a: int, p: int) -> int`

For a prime number $p$, returns the Legendre symbol $(a/p)$.

> `sqrt_mod(n: int, m: int, m_factors = None) -> int`

Given an integer $m \ge 2$, either returns $x$ such that $x^2 \equiv n \pmod m$, or returns $0$ if there's no such $x$.

> `sqrt_mod_prime(n: int, p: int) -> int`

Same as `sqrt_mod(n, p)`, but for a prime number `p`.

This function implements the Tonelli-Shanks algorithm.

> `sqrt_mod_prime_power(n: int, p: int, k: int) -> int`

Same as `sqrt_mod(n, p**k)`, but for a prime power `p**k`.

## Miscellaneous

> `iterate_idiv(x: int) -> Generator[tuple[int, int, int]]`

Yields tuples $(v, i_b, i_e)$, such that $v = \lfloor \frac{x}{i} \rfloor$ if and only if $i_b \le i < i_e$, in a decreasing order of v.

- Time Complexity: $\Theta(\sqrt x)$

> `extended_gcd(x: int, y: int) -> tuple[int, int, int]`

Returns $(g, a, b)$ such that $g = \gcd(x, y)$ and $ax + by = g$.

> `factorial_prime_power(n: int, p: int) -> int`

Given that $p$ is a prime number, returns maximal integer $i \ge 0$ such that $p^i$ divides $n!$.

> `comb_prime_power(n: int, k: int, p: int) -> int`

Given that $p$ is a prime number, returns maximal integer $i \ge 0$ such that $p^i$ divides $\binom n k$.

> `count_zero_mod(a: int, b: int, m: int, l: int, r: int) -> int`

Efficiently computes `sum((a*x + b)%m == 0 for x in range(l, r))`. `m` must be a positive integer.

> `sum_floor_linear(a: int, b: int, m: int, n: int) -> int`

Efficiently computes `sum((a*x + b) // m for x in range(n))`. This function is also known as `floor_sum`.
