import threading
from typing import Callable, Any, Tuple, List, Dict


class ThreadPool:
    """
    A thread pool for executing tasks concurrently.

    Args:
        thread_num (int): Number of threads in the pool.

    Attributes:
        thread_num (int): Number of threads in the pool.
        tasks_queue (List[Tuple[Callable, Tuple[Any, ...], Dict[str, Any]]]): Queue of tasks to be executed.
        threads (List[threading.Thread]): List of worker threads.
        stop_flag (bool): Flag to signal threads to stop.
        lock (threading.Lock): Lock for thread synchronization.
        condition (threading.Condition): Condition variable for task notification.
    """

    def __init__(self, thread_num: int) -> None:
        """
        Initializes the thread pool with the specified number of threads.

        Args:
            thread_num (int): Number of threads to create in the pool.

        Returns:
            None

        Raises:
            None
        """

        self.thread_num = thread_num
        self.tasks_queue: List[Tuple[Callable, Tuple[Any, ...], Dict[str, Any]]] = []

        self.threads: List[threading.Thread] = []

        self.stop_flag: bool = False
        self.lock: threading.Lock = threading.Lock()
        self.condition: threading.Condition = threading.Condition(self.lock)

        for _ in range(thread_num):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self):
        """
        Worker function that executes tasks from the queue in an infinite loop.

        Waits for tasks to be available and executes them until the pool is disposed.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        while True:
            with self.condition:
                while not self.tasks_queue and not self.stop_flag:
                    self.condition.wait()

                if self.stop_flag and not self.tasks_queue:
                    break

            with self.lock:
                if self.tasks_queue:
                    task, args, kwargs = self.tasks_queue.pop(0)
                else:
                    continue

            task(*args, **kwargs)

    def enqueue(self, task: Callable, *args: Any, **kwargs: Any):
        """
        Adds a task to the execution queue.

        Args:
            task (Callable): The function to be executed.
            *args (Any): Positional arguments for the function.
            **kwargs (Any): Keyword arguments for the function.

        Returns:
            None

        Raises:
            None
        """
        with self.condition:
            self.tasks_queue.append((task, args, kwargs))
            self.condition.notify()

    def dispose(self):
        """
        Shuts down the thread pool gracefully, waiting for all current tasks to complete.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """

        with self.condition:
            self.stop_flag = True
            self.condition.notify_all()

        for thread in self.threads:
            thread.join()
