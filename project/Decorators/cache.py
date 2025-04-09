from functools import wraps
from collections import OrderedDict
from typing import Callable, Any, Tuple


def cache(max_size: int = 0) -> Callable[[Callable], Callable]:
    """
    Декоратор для кэширования результатов функции с ограничением по размеру кэша.

    Args:
    max_size (int): Максимальный размер кэша. Если 0, кэширование отключено.
    Должен быть неотрицательным числом.

    Returns:
    Callable[[Callable], Callable]: Декоратор, который принимает функцию и возвращает
    её обертку с кэшированием.

    Raises:
    ValueError: Если max_size отрицательное число.
    """

    if max_size < 0:
        raise ValueError("max_size must be a non-negative integer")

    def cache_inner(function: Callable) -> Callable:
        """
        Inner decorator function implementing caching logic.

        Args:
            function (Callable): Function to be wrapped for caching.

        Returns:
            Callable: Wrapped function with added caching logic.

        Raises:
            No exceptions raised.
        """
        cached: OrderedDict[Tuple[Tuple[Any, ...], frozenset], Any] = OrderedDict()

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Function wrapper that implements result caching.

            Args:
                *args (Any): Positional arguments of the original function.
                **kwargs (Any): Keyword arguments of the original function.

            Returns:
                Any: Function result (either from cache or newly computed).

            Raises:
                No exceptions raised.
            """
            cache_key = (args, frozenset(kwargs.items()))

            if cache_key in cached:
                return cached[cache_key]

            result = function(*args, **kwargs)

            if max_size > 0:
                if len(cached) >= max_size and max_size > 0:
                    cached.popitem(last=False)
                cached[cache_key] = result

            return result

        return wrapper

    return cache_inner
