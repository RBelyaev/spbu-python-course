from copy import deepcopy
from inspect import signature, getfullargspec
from typing import Any, Callable


class Isolated:
    """
    Marker class indicating that an argument should be deep copied.
    """

    pass


class Evaluated:
    def __init__(self, function: Callable[..., Any]) -> None:
        """
        A wrapper class that ensures the wrapped function is called when invoked.
        Prohibits passing instances of the Isolated class.

        Args:
            function (Callable[..., Any]): The function to be wrapped.
        """

        self.function = function

    def __call__(self) -> Any:
        """
        Calls the wrapped function.

        Returns:
            Any: The result of the wrapped function execution.
        """
        return self.function()


def smart_args(enable_positional: bool = False) -> Callable[..., Any]:
    """
    Decorator for processing function arguments with support for special Isolated and Evaluated classes.

    Args:
        enable_positional (bool): Flag to enable positional arguments (default: False).

    Returns:
        Callable[..., Any]: Decorator with smart argument processing.
    """

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator that processes function arguments.

        Args:
            function (Callable[..., Any]): The function to be decorated.

        Returns:
            Callable[..., Any]: Wrapped function with argument processing.
        """
        sign = signature(function)
        argspec = getfullargspec(function)

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Processes function arguments by performing deep copy for Isolated and calling for Evaluated.

            Args:
                *args (Any): Positional arguments.
                **kwargs (Any): Keyword arguments.

            Raises:
                TypeError: If positional arguments are passed when they are disabled.
                ValueError: If a required argument with Isolated is not provided.
                TypeError: If duplicate arguments are provided.

            Returns:
                Any: Result of the decorated function execution.
            """
            if not enable_positional and args:
                raise TypeError("Positional arguments are disabled for this function")

            if enable_positional and args:
                positional_params = argspec.args[: len(args)]
                for name, value in zip(positional_params, args):
                    if name in kwargs:
                        raise TypeError(f"Got multiple values for argument '{name}'")
                    kwargs[name] = value

            for key, value in sign.parameters.items():
                if isinstance(value.default, Isolated):
                    if key not in kwargs:
                        raise ValueError(
                            f"Argument '{key}' must be provided when using Isolated()"
                        )
                    kwargs[key] = deepcopy(kwargs[key])
                if isinstance(value.default, Evaluated):
                    if key not in kwargs:
                        kwargs[key] = value.default()

            return function(**kwargs)

        return wrapper

    return decorator
