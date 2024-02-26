# CKP - 파이썬 코드 키트

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> [!CAUTION]
> 이 라이브러리는 현재 개발중입니다.

CKP는 프로그래밍 대회용 알고리즘의 순수 파이썬 구현체를 모아 놓은 라이브러리입니다.

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

CKP를 이용한 코드를 작성하세요. 아래는 그 예입니다.

```py
from ckp.number_theory import is_prime_naive

N = int(input())
print(is_prime_naive(N))
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
import math

# From primality_test.py
def is_prime_naive(n: int) -> bool:
    """
        Naive primality testing.
        - Time: `O(sqrt(n))`
    """
    if n < 100:
        return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or (n % 7 == 0) or (n % 11 == 0):
        return False
    for p in range(13, math.isqrt(n) + 1, 6):
        if n % p == 0 or n % (p + 4) == 0:
            return False
    return True

# From test.py
N = int(input())
print(is_prime_naive(N))
```
