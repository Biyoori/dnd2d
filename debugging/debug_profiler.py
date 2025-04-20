import time
from .debug_logger import logger

class DebugProfiler:
    @staticmethod
    def profile(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.log(f"Function {func.__name__} executed in {elapsed_time: .4f} seconds", "PERFORMANCE")
            return result
        return wrapper