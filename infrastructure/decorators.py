
import time
from functools import wraps
from typing import Callable, Coroutine


def sync_time_log_decorator(message: str = "") -> Callable:
    def inner_decorator(func: Callable) -> Callable:
        @wraps(func)    
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)

            time_taken = time.perf_counter() - start
            print(f"{message} Выполнение заняло {time_taken:.2f} секунд.")

            return result

        return wrapper
    return inner_decorator


def async_time_log_decorator(message: str = "") -> Coroutine:
    def inner_decorator(func: Coroutine) -> Coroutine:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)

            time_taken = time.perf_counter() - start
            print(f"{message} Выполнение заняло {time_taken:.2f} секунд.")

            return result

        return wrapper
    return inner_decorator
