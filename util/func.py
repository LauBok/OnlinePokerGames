from typing import Callable, Any

Case : Callable[[Any], Callable[[int], bool]] = lambda x: lambda n: x < n