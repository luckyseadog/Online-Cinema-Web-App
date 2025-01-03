"""
This type stub file was generated by pyright.
"""

from typing import Optional
from opentelemetry.context import create_key, get_value, set_value
from opentelemetry.context.context import Context
from opentelemetry.trace.span import INVALID_SPAN, Span

SPAN_KEY = ...
_SPAN_KEY = ...
def set_span_in_context(span: Span, context: Optional[Context] = ...) -> Context:
    """Set the span in the given context.

    Args:
        span: The Span to set.
        context: a Context object. if one is not passed, the
            default current context is used instead.
    """
    ...

def get_current_span(context: Optional[Context] = ...) -> Span:
    """Retrieve the current span.

    Args:
        context: A Context object. If one is not passed, the
            default current context is used instead.

    Returns:
        The Span set in the context if it exists. INVALID_SPAN otherwise.
    """
    ...

