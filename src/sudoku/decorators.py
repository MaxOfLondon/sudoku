# -*- coding: utf-8
import functools
import time


def timer(func):
    """ Print the runtime of the decorated function """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'{time.asctime()} TIMER: Finished {func.__module__}\
            .{func.__name__} in {run_time:.4f} sec')
        return value
    return wrapper_timer

def debug(func):
    """ Print the function signature and return value """
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        signature = ', '.join(args_repr + kwargs_repr)
        print(f'{time.asctime()} DEBUG: Calling {func.__module__}\
            .{func.__name__}({signature})')
        value = func(*args, **kwargs)
        print(f'{time.asctime()} DEBUG: {func.__module__}\
            .{func.__name__} returned {value!r}')
        return value
    return wrapper_debug

def state_print(func):
    @functools.wraps(func)
    def _state_print(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        print(f'{time.asctime()} DEBUG: Calling {func.__module__}\
            .{func.__name__}({args_repr}, {kwargs_repr})')
        print(args[0].state)
        value = func(*args, **kwargs)
        print(args[0].state)
        print(f'{time.asctime()} DEBUG: {func.__module__}\
            .{func.__name__} returned {value!r}')
        return value
    return _state_print
