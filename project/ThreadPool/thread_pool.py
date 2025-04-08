import threading
from typing import Callable, Any, Tuple, List, Dict

class ThreadPool:

    def __init__(self, thread_num: int) -> None:
        """
        Пул потоков для выполнения задач.

        Args:
        thread_num (int): Количество потоков в пуле.

        Returns:
        Нет возвращаемого значения.

        Raises:
        Нет явных исключений.
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
        Рабочая функция потока, выполняющая задачи из очереди в бесконечном цикле.

        Args:
        Нет параметров.

        Returns:
        Нет возвращаемого значения.

        Raises:
        Нет явных исключений.
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
        Добавляет задачу в очередь на выполнение.

        Args:
        task (Callable): Функция для выполнения.
        *args (Any): Позиционные аргументы функции.
        **kwargs (Any): Именованные аргументы функции.

        Returns:
        Нет возвращаемого значения.

        Raises:
        Нет явных исключений.
        """
        with self.condition:
            self.tasks_queue.append((task, args, kwargs))
            self.condition.notify()


    def dispose(self):
        """
        Завершает работу пула потоков, ожидая завершения всех текущих задач.

        Args:
        Нет параметров.

        Returns:
        Нет возвращаемого значения.

        Raises:
        Нет явных исключений.
        """


        with self.condition:
            self.stop_flag = True
            self.condition.notify_all() 

        for thread in self.threads:
            thread.join()
        

    