from __future__ import annotations

import abc
import string
from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from typing import ClassVar

from schwifty.domain import Component


_alphabet: str = string.digits + string.ascii_uppercase


def numerify(value: str) -> int:
    return int("".join(str(_alphabet.index(c)) for c in value))


def iso7064(
    n: int,
    mod: int,
    post_process: Callable[[int], int],
    n_digits: int = 2,
) -> str:
    return f"{post_process(n % mod):0{n_digits}d}"


def weighted(
    value: str,
    mod: int,
    weights: list[int],
) -> int:
    return sum(n * int(c) for n, c in zip(weights, value)) % mod


class Algorithm(metaclass=abc.ABCMeta):
    name: ClassVar[str]
    accepts: ClassVar[list[Component]] = [
        Component.BANK_CODE,
        Component.BRANCH_CODE,
        Component.ACCOUNT_CODE,
    ]

    @abc.abstractmethod
    def compute(self, components: list[str]) -> str:
        return ""

    def validate(self, components: list[str], expected: str) -> bool:
        return self.compute(components) == expected


class ISO7064_mod97_10(Algorithm):  # noqa: N801
    def post_process(self, r: int) -> int:
        return 98 - r

    def pre_process(self, components: list[str]) -> int:
        return numerify("".join(components)) * 100

    def compute(self, components: list[str]) -> str:
        return iso7064(self.pre_process(components), 97, self.post_process)


algorithms: dict[str, Algorithm] = {}


def register(*prefixes) -> Callable[[type[Algorithm]], type[Algorithm]]:
    def wrapper(algorithm_cls: type[Algorithm]) -> type[Algorithm]:
        key = algorithm_cls.name
        for prefix in prefixes:
            algorithms[f"{prefix}:{key}"] = algorithm_cls()
        return algorithm_cls

    return wrapper


this = Path(__file__)
for path in this.parent.glob("*.py"):
    if path == this:
        continue
    import_module(f"schwifty.checksum.{path.stem}")
