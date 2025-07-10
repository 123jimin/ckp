# CKP - 파이썬 코드 키트

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> [!CAUTION]
> 이 라이브러리는 현재 개발중입니다. API가 언제든지 변경될 수 있습니다.

CKP는 프로그래밍 대회용 알고리즘의 **의존성 없는 순수 파이썬 구현체**를 모아 놓은 라이브러리입니다.

CKP는 성능을 해치지 않으면서, 유연하게 쓰일 수 있는 인터페이스를 제공하는 것을 목표로 합니다.

CKP는 한 파이썬 코드와 그 코드가 의존하는 모듈의 코드를 합쳐 하나의 파일로 만들어 주는 도구인 [impacker](https://github.com/123jimin/impacker)와 호환됩니다. 그렇기 때문게, CKP는 하나의 소스 코드 파일만 제출 가능한 온라인 저지 시스템 상에서도 사용 가능합니다.

## 참고사항

`SortedList` 및 `SortedDict` 구현은 `sortedcontainers` (<https://github.com/grantjenks/python-sortedcontainers>)를 기반으로 합니다. 원 프로젝트는 Apache License, version 2.0 (<http://www.apache.org/licenses/LICENSE-2.0>)를 따릅니다.

프로그래밍 대회 이외의 용도로 CKP를 사용하는 것은 적절하지 않습니다. 순수 파이썬으로 쓰여저 있어서 성능에 제약을 받기 때문입니다.

순수 파이썬을 사용해야만 하는 상황이 아니라면, C 확장 모듈을 직접 만들거나, 다른 프로그래밍 언어를 사용하는 것을 강력히 권장합니다.

## 사용 방법

### 설치

[Poetry](https://python-poetry.org/) 사용을 *강력하게* 권장합니다.

```sh
poetry add git+https://github.com/123jimin/ckp.git
```

### 사용

아래는 CKP를 사용해 소수 판별을 하는 프로그램 코드의 예시입니다.


```py
from ckp.number_theory.primality_test import is_prime_trial_division

N = int(input())
print(is_prime_trial_division(N))
```

코드 실행은 이렇게 할 수 있습니다.

```sh
poetry run python test.py
```

### 패킹

CKP를 소스 코드에 포함시키려면, 우선 [impacker](https://github.com/123jimin/impacker)를 설치하세요.

```sh
poetry add git+https://github.com/123jimin/impacker.git
```

아까 작성한 소스 코드의 이름이 `code.py`이고, 패킹한 파일 이름을 `out.py`로 하고 싶은 경우라면, 아래와 같은 방식으로 impacker를 사용하면 됩니다.

```sh
poetry run python -m impacker code.py out.py
```

`out.py`에 온라인 저지 시스템에 제출 가능한 형태의 소스 코드가 저장됩니다.

```py
from math import isqrt

# is_prime_trial_division | from primality_test.py, line 3
def is_prime_trial_division(n: int) -> bool:
    """ Primality testing using trial division. Slow but good enough for simple problems. """
    if n < 53:
        return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
    if not (n & 1 and n % 3 and n % 5 and n % 7 and n % 11 and n % 13):
        return False
    if n < 289:
        return True
    for p in range(17, isqrt(n) + 1, 6):
        if not (n % p and n % (p + 2)):
            return False
    return True

# From main code
N = int(input())
print(is_prime_trial_division(N))
```
