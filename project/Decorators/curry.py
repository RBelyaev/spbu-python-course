from typing import Callable, Any, Tuple


def curry_explicit(function: Callable, arity: int) -> Callable:
    """
    Converts a function into its curried version with specified arity.

    A curried function allows partial application of arguments. If enough arguments
    (equal to the function's arity) are provided, the function is executed. Otherwise,
    a new function expecting the remaining arguments is returned.

    Args:
        function (Callable): The function to be curried.
        arity (int): The number of arguments the function expects (its arity).

    Returns:
        Callable: The curried version of the original function.

    Raises:
        ValueError: If arity is negative.
        TypeError: If too many arguments are provided.
    """
    if arity == 0:
        return function
    if arity < 0:
        raise ValueError("Arity must be a non-negative integer")

    def inner_curry(args: Tuple[Any, ...]) -> Callable:
        """
        Internal helper function for currying that accumulates arguments.

        Args:
            args (Tuple[Any, ...]): Tuple of already accumulated arguments.

        Returns:
            Callable: Either the function result (if enough arguments) or a new function
                     expecting the next argument.
        """
        if len(args) == arity:
            return function(*args)
        else:
            return lambda arg: inner_curry(args + (arg,))

    return inner_curry(())


def uncurry_explicit(function: Callable, arity: int) -> Callable:
    """
    Converts a curried function back to its uncurried version with specified arity.

    Args:
        function (Callable): The curried function to be converted.
        arity (int): The number of arguments the function expects (its arity).

    Returns:
        Callable: The uncurried version of the original function.

    Raises:
        ValueError: If arity is negative or argument count doesn't match.
        TypeError: If provided arguments don't match function expectations.
    """
    if arity < 0:
        raise ValueError("Arity must be a non-negative integer")
    if arity == 0:
        return function()

    def inner_uncurry(*args: Any) -> Any:
        """
        Internal helper function that applies all arguments at once.

        Args:
            *args (Any): Provided arguments.

        Returns:
            Any: Result of executing the original curried function.

        Raises:
            ValueError: If argument count doesn't match arity.
        """
        if len(args) != arity:
            raise ValueError(f"Expected {arity} arguments, but got {len(args)}")

        result = function
        for arg in args:
            result = result(arg)
        return result

    return inner_uncurry
