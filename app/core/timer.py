from datetime import datetime


def timer(func):
    def wraps(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        finish = datetime.now()
        print(f'{func.__name__} function execution time: {finish - start} [h:mm:ss.milliseconds]')
        return result
    return wraps
