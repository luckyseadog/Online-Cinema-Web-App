"""
This type stub file was generated by pyright.
"""

class MetricConfig:
    """Configuration values for metrics"""
    def __init__(self, quota=..., samples=..., event_window=..., time_window_ms=..., tags=...) -> None:
        """
        Arguments:
            quota (Quota, optional): Upper or lower bound of a value.
            samples (int, optional): Max number of samples kept per metric.
            event_window (int, optional): Max number of values per sample.
            time_window_ms (int, optional): Max age of an individual sample.
            tags (dict of {str: str}, optional): Tags for each metric.
        """
        ...
    
    @property
    def samples(self): # -> int:
        ...
    
    @samples.setter
    def samples(self, value): # -> None:
        ...
    


