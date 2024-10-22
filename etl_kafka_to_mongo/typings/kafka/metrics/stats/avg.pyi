"""
This type stub file was generated by pyright.
"""

from kafka.metrics.stats.sampled_stat import AbstractSampledStat

class Avg(AbstractSampledStat):
    """
    An AbstractSampledStat that maintains a simple average over its samples.
    """
    def __init__(self) -> None:
        ...
    
    def update(self, sample, config, value, now): # -> None:
        ...
    
    def combine(self, samples, config, now): # -> Literal[0]:
        ...
    


