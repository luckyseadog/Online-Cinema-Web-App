"""
This type stub file was generated by pyright.
"""

from enum import IntEnum

class ConfigResourceType(IntEnum):
    """An enumerated type of config resources"""
    BROKER = ...
    TOPIC = ...


class ConfigResource:
    """A class for specifying config resources.
    Arguments:
        resource_type (ConfigResourceType): the type of kafka resource
        name (string): The name of the kafka resource
        configs ({key : value}): A  maps of config keys to values.
    """
    def __init__(self, resource_type, name, configs=...) -> None:
        ...
    


