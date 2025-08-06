from typing import List, Iterable
import math

SQRT_2 = math.sqrt(2.0)

def normal_cdf(z: float) -> float:
    """ CDF for the normal distribution. """
    return 0.5 * (1.0 + math.erf(z / SQRT_2))

class StatList:
    """ Sequence of floats with incremental stats. """

    __slots__ = ('_data', '_sum', '_sum_sq', '_min', '_max', '_name')

    _data: List[float]
    _sum: float
    _sum_sq: float
    _min: float|None
    _max: float|None
    _name: str

    def __init__(self, data: Iterable[float] | None = None, name: str = "") -> None:
        self._data, self._sum, self._sum_sq, self._name = [], 0.0, 0.0, name
        self._min, self._max = None, None

        if data is not None: self.extend(data)

    @property
    def name(self) -> str: return self._name

    @name.setter
    def name(self, value: str) -> None: self._name = str(value)

    def append(self, value: float) -> None:
        self._data.append(v := float(value)); self._sum += v; self._sum_sq += v * v
        if self._min is None or value < self._min: self._min = value
        if self._max is None or value > self._max: self._max = value

    def extend(self, values: Iterable[float]) -> None:
        self._data.extend(vals := list(map(float, values)))
        self._sum += sum(vals); self._sum_sq += sum(v * v for v in vals)

        if not vals: return
        min_val, max_val = min(vals), max(vals)
        if self._min is None or min_val < self._min: self._min = min_val
        if self._max is None or max_val > self._max: self._max = max_val

    def mean(self) -> float: return self._sum / len(self._data) if self._data else float("nan")

    def min(self) -> float|None: return self._min
    def max(self) -> float|None: return self._max

    def variance(self) -> float:
        """ Sample variance. """
        if (n := len(self._data)) < 2: return 0.0
        m = self.mean()
        return (self._sum_sq - n * m * m) / (n - 1)

    def stdev(self) -> float:
        """ Sample standard deviation. """
        return math.sqrt(self.variance()) if len(self._data) >= 2 else 0.0

    def compare(self, other: "StatList") -> tuple[float, float, float]:
        """ Welch p-values for >=, =, <= null H0s. """
        n1, n2 = len(self._data), len(other._data)
        if n1 < 2 or n2 < 2: return (float("nan"), float("nan"), float("nan"))
        m1, m2 = self.mean(), other.mean()
        s1_sq, s2_sq = self.variance(), other.variance()
        se = math.sqrt(s1_sq / n1 + s2_sq / n2)
        if se == 0.0: return (1.0, 1.0, 1.0)
        t = (m1 - m2) / se
        return (
            normal_cdf(t),
            2.0 * (1.0 - normal_cdf(abs(t))),
            1.0 - normal_cdf(t),
        )
    
    @staticmethod
    def format_list(stats: Iterable["StatList"], *, val_prec: int = 3, measure_unit: str|None = None) -> str:
        """ Show a formatted list of multiple stats. """
        if not isinstance(stats, list): stats = list(stats)
        if not stats: return ""
        name_w = max(len(s._name) for s in stats) + 1
        lines = [s.__str__(name_w=name_w, val_prec=val_prec, measure_unit=measure_unit) for s in stats]

        if (n := len(stats)) < 2: return "\n".join(lines)

        order = sorted(range(n), key=lambda i: stats[i].mean())
        i_fast, i2 = order[0], order[1]
        p = stats[i_fast].compare(stats[i2])[0]
        lines[i_fast] += f" # fastest (p={p:.3f})"
        
        if n >= 3:
            i_slow, i2s = order[-1], order[-2]
            p2 = stats[i_slow].compare(stats[i2s])[2]
            lines[i_slow] += f" # slowest (p={p2:.3f})"

        return "\n".join(lines)
    
    @staticmethod
    def format_list_ranking(stats: Iterable["StatList"], *, val_prec: int = 3, measure_unit: str|None = None, alpha: float = 0.05) -> str:
        """ Show a formatted, sorted list of multiple stats. """
        if not isinstance(stats, list): stats = list(stats)
        if (n := len(stats)) < 1: return ""

        n_w = len(str(n))
        format_idx = f"#{{:0{n_w}d}}".format
        name_w = max(len(s._name) for s in stats) + 1
        order = sorted(range(n), key=lambda i: stats[i].mean())

        def get_significant_diff(curr: "StatList", inds: Iterable[int], default_ind: int|None, cmp_ind: int) -> "tuple[int, float]|None":
            for i in inds:
                j = order[i]; pv = curr.compare(stats[j])[cmp_ind]
                if pv < alpha: return (i, pv)
            if default_ind is not None:
                j = order[default_ind]
                return (default_ind, curr.compare(stats[j])[cmp_ind])
            return None

        lines = []
        for idx in range(n):
            i = order[idx]; curr = stats[i]

            left_str = ""
            if (left_sig := get_significant_diff(curr, range(idx-1, 0, -1), 0 if idx else None, 2)):
                left_idx, left_p = left_sig
                left_str = f"slower than {format_idx(left_idx+1)} (p={left_p:.3f})"

            right_str = ""
            if (right_sig := get_significant_diff(curr, range(idx+1, n), n-1 if idx < n-1 else None, 0)):
                right_idx, right_p = right_sig
                right_str = f"faster than {format_idx(right_idx+1)} (p={right_p:.3f})"

            cmp_str = ""
            if right_str:
                if left_str: cmp_str = f"{left_str}, {right_str}"
                else: left_str = " " * len(right_str); cmp_str = f"{left_str}  {right_str}"
            elif left_str: cmp_str = left_str

            if cmp_str: cmp_str = f" | {cmp_str}"
            lines.append(f"{format_idx(idx+1)} | {curr.__str__(name_w=name_w, val_prec=val_prec, measure_unit=measure_unit)}{cmp_str}")

        return "\n".join(lines)
    
    @staticmethod
    def format_list_analysis(stats: Iterable["StatList"], *, val_prec: int = 3, measure_unit: str|None = None, alpha: float = 0.05) -> str:
        if not isinstance(stats, list): stats = list(stats)
        if not stats: return ""
        
        summary = StatList.format_list(stats, val_prec=val_prec, measure_unit=measure_unit)
        if len(stats) <= 1: return summary

        return summary + "\n\n" + StatList.format_list_ranking(stats, val_prec=val_prec, measure_unit=measure_unit, alpha=alpha)

    def __iter__(self): return iter(self._data)

    def __str__(self, *, report_range: bool = True, name_w: int = 0, val_prec: int = 3, measure_unit: str|None = None) -> str:
        name_part = (f"{self._name:<{name_w}}: " if self._name else "")
        if not self._data: return f"{name_part}(empty)"
        format_val = f"{{:.{val_prec}f}}".format

        postfix = ""
        if report_range and len(self._data) > 1:
            postfix += f" ({format_val(self._min)} to {format_val(self._max)})"
        
        if measure_unit:
            postfix += f" {measure_unit}"

        return f"{name_part}{format_val(self.mean())} \xB1 {format_val(self.stdev())}{postfix}"

    def __repr__(self) -> str: return f"StatList({self._data!r}, name={self._name!r})"