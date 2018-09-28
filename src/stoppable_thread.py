import threading

class StoppableThread(threading.Thread):
    """
    Extends the treading class to create a thread that can be stopped.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the StoppableThread with some args that are passed to a
        regular thread.

        Keyword argments:
        self -- The caller, StoppableThread instance
        args -- arguments
        kwargs -- other arguments

        Side effects:
        Creates the thread with the provided args and kwargs
        """
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_flag = threading.Event()

    """
    # Sample implementation of a run() method

    def run(self):
        while True:
            if self.stopped():
                break;
            # Program logic goes here
    """

    def stop(self):
        """
        Function to stop the thread.

        Keyword arguments:
        self -- The caller to be stopped.

        Side effects:
        sets the stop flag
        """
        self._stop_flag.set()

    def stopped(self):
        """
        Function that returns if the thread is stopped.

        Keyword arguments:
        self -- The caller to have its flag checked.

        Returns:
        If the stopped flag is set.
        """
        return self._stop_flag.isSet()
