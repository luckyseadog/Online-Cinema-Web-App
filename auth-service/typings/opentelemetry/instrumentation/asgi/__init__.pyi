"""
This type stub file was generated by pyright.
"""

import typing
import urllib
from collections import defaultdict
from functools import wraps
from timeit import default_timer
from typing import Any, Awaitable, Callable, DefaultDict, Tuple
from asgiref.compatibility import guarantee_single_callable
from opentelemetry import context, trace
from opentelemetry.instrumentation._semconv import _HTTPStabilityMode, _OpenTelemetrySemanticConventionStability, _OpenTelemetryStabilitySignalType, _filter_semconv_active_request_count_attr, _filter_semconv_duration_attrs, _get_schema_url, _report_new, _report_old, _server_active_requests_count_attrs_new, _server_active_requests_count_attrs_old, _server_duration_attrs_new, _server_duration_attrs_old, _set_http_flavor_version, _set_http_host_server, _set_http_method, _set_http_net_host_port, _set_http_peer_ip_server, _set_http_peer_port_server, _set_http_scheme, _set_http_target, _set_http_url, _set_http_user_agent, _set_status
from opentelemetry.instrumentation.asgi.types import ClientRequestHook, ClientResponseHook, ServerRequestHook
from opentelemetry.instrumentation.asgi.version import __version__
from opentelemetry.instrumentation.propagators import get_global_response_propagator
from opentelemetry.instrumentation.utils import _start_internal_or_server_span
from opentelemetry.metrics import get_meter
from opentelemetry.propagators.textmap import Getter, Setter
from opentelemetry.semconv._incubating.metrics.http_metrics import create_http_server_active_requests, create_http_server_request_body_size, create_http_server_response_body_size
from opentelemetry.semconv.metrics import MetricInstruments
from opentelemetry.semconv.metrics.http_metrics import HTTP_SERVER_REQUEST_DURATION
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import set_span_in_context
from opentelemetry.util.http import OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SANITIZE_FIELDS, OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST, OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE, SanitizeValue, _parse_url_query, get_custom_headers, normalise_request_header_name, normalise_response_header_name, remove_url_credentials, sanitize_method

"""
The opentelemetry-instrumentation-asgi package provides an ASGI middleware that can be used
on any ASGI framework (such as Django-channels / Quart) to track request timing through OpenTelemetry.

Usage (Quart)
-------------

.. code-block:: python

    from quart import Quart
    from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

    app = Quart(__name__)
    app.asgi_app = OpenTelemetryMiddleware(app.asgi_app)

    @app.route("/")
    async def hello():
        return "Hello!"

    if __name__ == "__main__":
        app.run(debug=True)


Usage (Django 3.0)
------------------

Modify the application's ``asgi.py`` file as shown below.

.. code-block:: python

    import os
    from django.core.asgi import get_asgi_application
    from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asgi_example.settings')

    application = get_asgi_application()
    application = OpenTelemetryMiddleware(application)


Usage (Raw ASGI)
----------------

.. code-block:: python

    from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

    app = ...  # An ASGI application.
    app = OpenTelemetryMiddleware(app)


Configuration
-------------

Request/Response hooks
**********************

This instrumentation supports request and response hooks. These are functions that get called
right after a span is created for a request and right before the span is finished for the response.

- The server request hook is passed a server span and ASGI scope object for every incoming request.
- The client request hook is called with the internal span and an ASGI scope when the method ``receive`` is called.
- The client response hook is called with the internal span and an ASGI event when the method ``send`` is called.

For example,

.. code-block:: python

    def server_request_hook(span: Span, scope: dict[str, Any]):
        if span and span.is_recording():
            span.set_attribute("custom_user_attribute_from_request_hook", "some-value")

    def client_request_hook(span: Span, scope: dict[str, Any], message: dict[str, Any]):
        if span and span.is_recording():
            span.set_attribute("custom_user_attribute_from_client_request_hook", "some-value")

    def client_response_hook(span: Span, scope: dict[str, Any], message: dict[str, Any]):
        if span and span.is_recording():
            span.set_attribute("custom_user_attribute_from_response_hook", "some-value")

   OpenTelemetryMiddleware().(application, server_request_hook=server_request_hook, client_request_hook=client_request_hook, client_response_hook=client_response_hook)

Capture HTTP request and response headers
*****************************************
You can configure the agent to capture specified HTTP headers as span attributes, according to the
`semantic convention <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/semantic_conventions/http.md#http-request-and-response-headers>`_.

Request headers
***************
To capture HTTP request headers as span attributes, set the environment variable
``OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST`` to a comma delimited list of HTTP header names.

For example,
::

    export OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST="content-type,custom_request_header"

will extract ``content-type`` and ``custom_request_header`` from the request headers and add them as span attributes.

Request header names in ASGI are case-insensitive. So, giving the header name as ``CUStom-Header`` in the environment
variable will capture the header named ``custom-header``.

Regular expressions may also be used to match multiple headers that correspond to the given pattern.  For example:
::

    export OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST="Accept.*,X-.*"

Would match all request headers that start with ``Accept`` and ``X-``.

To capture all request headers, set ``OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST`` to ``".*"``.
::

    export OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST=".*"

The name of the added span attribute will follow the format ``http.request.header.<header_name>`` where ``<header_name>``
is the normalized HTTP header name (lowercase, with ``-`` replaced by ``_``). The value of the attribute will be a
list containing the header values.

For example:
``http.request.header.custom_request_header = ["<value1>", "<value2>"]``

Response headers
****************
To capture HTTP response headers as span attributes, set the environment variable
``OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE`` to a comma delimited list of HTTP header names.

For example,
::

    export OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE="content-type,custom_response_header"

will extract ``content-type`` and ``custom_response_header`` from the response headers and add them as span attributes.

Response header names in ASGI are case-insensitive. So, giving the header name as ``CUStom-Header`` in the environment
variable will capture the header named ``custom-header``.

Regular expressions may also be used to match multiple headers that correspond to the given pattern.  For example:
::

    export OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE="Content.*,X-.*"

Would match all response headers that start with ``Content`` and ``X-``.

To capture all response headers, set ``OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE`` to ``".*"``.
::

    export OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE=".*"

The name of the added span attribute will follow the format ``http.response.header.<header_name>`` where ``<header_name>``
is the normalized HTTP header name (lowercase, with ``-`` replaced by ``_``). The value of the attribute will be a
list containing the header values.

For example:
``http.response.header.custom_response_header = ["<value1>", "<value2>"]``

Sanitizing headers
******************
In order to prevent storing sensitive data such as personally identifiable information (PII), session keys, passwords,
etc, set the environment variable ``OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SANITIZE_FIELDS``
to a comma delimited list of HTTP header names to be sanitized.  Regexes may be used, and all header names will be
matched in a case-insensitive manner.

For example,
::

    export OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SANITIZE_FIELDS=".*session.*,set-cookie"

will replace the value of headers such as ``session-id`` and ``set-cookie`` with ``[REDACTED]`` in the span.

Note:
    The environment variable names used to capture HTTP headers are still experimental, and thus are subject to change.

API
---
"""
class ASGIGetter(Getter[dict]):
    def get(self, carrier: dict, key: str) -> typing.Optional[typing.List[str]]:
        """Getter implementation to retrieve a HTTP header value from the ASGI
        scope.

        Args:
            carrier: ASGI scope object
            key: header name in scope
        Returns:
            A list with a single string with the header value if it exists,
                else None.
        """
        ...
    
    def keys(self, carrier: dict) -> typing.List[str]:
        ...
    


asgi_getter = ...
class ASGISetter(Setter[dict]):
    def set(self, carrier: dict, key: str, value: str) -> None:
        """Sets response header values on an ASGI scope according to `the spec <https://asgi.readthedocs.io/en/latest/specs/www.html#response-start-send-event>`_.

        Args:
            carrier: ASGI scope object
            key: response header name to set
            value: response header value
        Returns:
            None
        """
        ...
    


asgi_setter = ...
def collect_request_attributes(scope, sem_conv_opt_in_mode=...): # -> dict[Any, Any]:
    """Collects HTTP request attributes from the ASGI scope and returns a
    dictionary to be used as span creation attributes."""
    ...

def collect_custom_headers_attributes(scope_or_response_message: dict[str, Any], sanitize: SanitizeValue, header_regexes: list[str], normalize_names: Callable[[str], str]) -> dict[str, list[str]]:
    """
    Returns custom HTTP request or response headers to be added into SERVER span as span attributes.

    Refer specifications:
     - https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/semantic_conventions/http.md#http-request-and-response-headers
    """
    ...

def get_host_port_url_tuple(scope): # -> tuple[Any | str, Any | str | int, Any]:
    """Returns (host, port, full_url) tuple."""
    ...

def set_status_code(span, status_code, metric_attributes=..., sem_conv_opt_in_mode=...): # -> None:
    """Adds HTTP response attributes to span using the status_code argument."""
    ...

def get_default_span_details(scope: dict) -> Tuple[str, dict]:
    """
    Default span name is the HTTP method and URL path, or just the method.
    https://github.com/open-telemetry/opentelemetry-specification/pull/3165
    https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/http/#name

    Args:
        scope: the ASGI scope dictionary
    Returns:
        a tuple of the span name, and any attributes to attach to the span.
    """
    ...

class OpenTelemetryMiddleware:
    """The ASGI application middleware.

    This class is an ASGI middleware that starts and annotates spans for any
    requests it is invoked with.

    Args:
        app: The ASGI application callable to forward requests to.
        default_span_details: Callback which should return a string and a tuple, representing the desired default span name and a
                      dictionary with any additional span attributes to set.
                      Optional: Defaults to get_default_span_details.
        server_request_hook: Optional callback which is called with the server span and ASGI
                      scope object for every incoming request.
        client_request_hook: Optional callback which is called with the internal span, and ASGI
                      scope and event which are sent as dictionaries for when the method receive is called.
        client_response_hook: Optional callback which is called with the internal span, and ASGI
                      scope and event which are sent as dictionaries for when the method send is called.
        tracer_provider: The optional tracer provider to use. If omitted
            the current globally configured one is used.
        meter_provider: The optional meter provider to use. If omitted
            the current globally configured one is used.
    """
    def __init__(self, app, excluded_urls=..., default_span_details=..., server_request_hook: ServerRequestHook = ..., client_request_hook: ClientRequestHook = ..., client_response_hook: ClientResponseHook = ..., tracer_provider=..., meter_provider=..., tracer=..., meter=..., http_capture_headers_server_request: list[str] | None = ..., http_capture_headers_server_response: list[str] | None = ..., http_capture_headers_sanitize_fields: list[str] | None = ...) -> None:
        ...
    
    async def __call__(self, scope: dict[str, Any], receive: Callable[[], Awaitable[dict[str, Any]]], send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
        """The ASGI application

        Args:
            scope: An ASGI environment.
            receive: An awaitable callable yielding dictionaries
            send: An awaitable callable taking a single dictionary as argument.
        """
        ...
    


