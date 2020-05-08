from typing import Callable, Any

CaseLessThan: Callable[[int], Callable[[int], bool]] = lambda x: lambda n: x < n
Case: Callable[[Any], Callable[[Any], bool]] = lambda x: lambda n: x == n