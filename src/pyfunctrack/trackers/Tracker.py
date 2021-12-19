from abc import abstractmethod

class Tracker:

    def do(self,
        parameter=None,
        function=None,
        args=None,
        kwargs=None,
        return_value=None,
        start_time=None,
        end_time=None,
        message=None
    ):
        self.tracker_method(
            parameter=parameter,
            function=function.__name__,
            args=args if len(args) > 0 else None,
            kwargs=kwargs if len(kwargs) > 0 else None,
            return_value=return_value,
            start_time=start_time,
            end_time=end_time,
            message=message
        )

    @abstractmethod
    def tracker_method(self,
        parameter=None,
        function=None,
        args=None,
        kwargs=None,
        return_value=None,
        start_time=None,
        end_time=None,
        message=None
    ):
        ...