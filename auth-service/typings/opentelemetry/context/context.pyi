"""
This type stub file was generated by pyright.
"""

import typing
from abc import ABC, abstractmethod

class Context(typing.Dict[str, object]):
    def __setitem__(self, key: str, value: object) -> None:
        ...
    


class _RuntimeContext(ABC):
    """The RuntimeContext interface provides a wrapper for the different
    mechanisms that are used to propagate context in Python.
    Implementations can be made available via entry_points and
    selected through environment variables.
    """
    @abstractmethod
    def attach(self, context: Context) -> object:
        """Sets the current `Context` object. Returns a
        token that can be used to reset to the previous `Context`.

        Args:
            context: The Context to set.
        """
        ...
    
    @abstractmethod
    def get_current(self) -> Context:
        """Returns the current `Context` object."""
        ...
    
    @abstractmethod
    def detach(self, token: object) -> None:
        """Resets Context to a previous value

        Args:
            token: A reference to a previous Context.
        """
        ...
    


__all__ = ["Context"]
