from typing import Generator, Tuple, Optional, Callable


def rgba_gen() -> Generator[Tuple[int, int, int, int], None, None]:
    """
    Generator for all possible RGBA color combinations.

    Args:
        No arguments.

    Returns:
        Generator[Tuple[int, int, int, int], None, None]: Generator yielding RGBA tuples.
        - r: Red channel (0-255)
        - g: Green channel (0-255)
        - b: Blue channel (0-255)
        - a: Alpha channel (0-100 with step 2)

    Raises:
        No exceptions.
    """
    return (
        (r, g, b, a)
        for r in range(256)
        for g in range(256)
        for b in range(256)
        for a in range(0, 101, 2)
    )


def get_colour(index: int) -> Tuple[int, int, int, int]:
    """
    Returns RGBA color at specified index in the sequence.

    Args:
        index (int): Color position in the sequence.

    Returns:
        Tuple[int, int, int, int]: RGBA color tuple.

    Raises:
        IndexError: If index is out of valid range.
        StopIteration: If generator is exhausted (theoretically, but handled via IndexError in practice).
    """
    if index < 1 or index > 256**3 * 51:
        raise IndexError("Colour index out of range")
    rgba = rgba_gen()
    for _ in range(index - 1):
        next(rgba)
    return next(rgba)


def prime_dec(func: Callable[[], Generator[int, None, None]]) -> Callable[[int], int]:
    """
    Decorator for prime number generator that modifies its behavior:
    returns k-th prime number and stores last generated prime as an attribute.

    Args:
        func (Callable[[], Generator[int, None, None]]): Prime number generator function.

    Returns:
        Callable[[int], int]: Wrapper function that returns k-th prime number and stores last value.

    Raises:
        ValueError: If k is less than last requested value.
        RuntimeError: If generator didn't yield a value.
    """
    gen = func()
    last_k: int = 0
    last_prime: Optional[int] = None

    def wrapper(k: int) -> int:
        nonlocal last_k, last_prime

        if k < last_k:
            raise ValueError(
                "k must be greater than or equal to the last requested value."
            )

        for _ in range(last_k, k):
            last_prime = next(gen)

        last_k = k
        if last_prime is None:
            raise RuntimeError("Prime generator did not yield a value.")

        return last_prime

    return wrapper


def prime_generator() -> Generator[int, None, None]:
    """
    Prime numbers generator.

    Args:
        No arguments.

    Returns:
        Generator[int, None, None]: Generator yielding prime numbers starting from 2.

    Raises:
        No exceptions.
    """
    num = 2
    flag = True
    while True:
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                flag = False
                break
        if flag:
            yield num
        num += 1
        flag = True
