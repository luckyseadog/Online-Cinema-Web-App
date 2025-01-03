"""
This type stub file was generated by pyright.
"""

import typing
from opentelemetry.context.context import Context
from opentelemetry.propagators import textmap

class TraceContextTextMapPropagator(textmap.TextMapPropagator):
    """Extracts and injects using w3c TraceContext's headers."""
    _TRACEPARENT_HEADER_NAME = ...
    _TRACESTATE_HEADER_NAME = ...
    _TRACEPARENT_HEADER_FORMAT = ...
    _TRACEPARENT_HEADER_FORMAT_RE = ...
    def extract(self, carrier: textmap.CarrierT, context: typing.Optional[Context] = ..., getter: textmap.Getter[textmap.CarrierT] = ...) -> Context:
        """Extracts SpanContext from the carrier.

        See `opentelemetry.propagators.textmap.TextMapPropagator.extract`
        """
        ...
    
    def inject(self, carrier: textmap.CarrierT, context: typing.Optional[Context] = ..., setter: textmap.Setter[textmap.CarrierT] = ...) -> None:
        """Injects SpanContext into the carrier.

        See `opentelemetry.propagators.textmap.TextMapPropagator.inject`
        """
        ...
    
    @property
    def fields(self) -> typing.Set[str]:
        """Returns a set with the fields set in `inject`.

        See
        `opentelemetry.propagators.textmap.TextMapPropagator.fields`
        """
        ...
    


