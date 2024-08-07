import threading


class Utils:

    @staticmethod
    def set_interval(func, sec):
        def func_wrapper():
            Utils.set_interval(func, sec)
            func()

        timer = threading.Timer(sec, func_wrapper)
        timer.start()
        return timer
