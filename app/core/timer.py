from datetime import datetime


def timer(func):
    def wraps(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        finish = datetime.now()
        print(f'execution time: {finish - start} [h:mm:ss.milliseconds]')
        return
    return wraps
