from typing import List, Generator, Tuple
import itertools
from concurrent.futures import ProcessPoolExecutor


def cartesian_product_gen(
    sets: List[List[int]],
) -> Generator[Tuple[int, ...], None, None]:
    """
    Generator for Cartesian product (all possible combinations) of a list of integer sets.

    Args:
        sets (List[List[int]]): List of integer lists for which to compute the Cartesian product.

    Returns:
        Generator[Tuple[int, ...], None, None]: Generator yielding tuples with combinations
                                              of elements from input sets.

    Raises:
        No exceptions.
    """
    for combination in itertools.product(*sets):
        yield combination


def cartesian_product_sum(thread_num: int, sets: List[List[int]]) -> int:
    """
    Calculates the sum of all elements in the Cartesian product using multithreading.

    Args:
        thread_num (int): Number of threads for parallel computation.
        sets (List[List[int]]): List of integer lists to process.

    Returns:
        int: Sum of all elements of all combinations in the Cartesian product.

    Raises:
        No exceptions.
    """
    gen = cartesian_product_gen(sets)
    total_sum = 0
    with ProcessPoolExecutor(max_workers=thread_num) as executor:
        futures = executor.map(sum, gen)
        total_sum = sum(futures)
    return total_sum
