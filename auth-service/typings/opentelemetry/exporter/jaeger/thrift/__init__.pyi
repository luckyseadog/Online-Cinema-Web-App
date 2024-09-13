"""
This type stub file was generated by pyright.
"""

import logging
from os import environ
from typing import Optional
from deprecated import deprecated
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift.gen.jaeger import Collector as jaeger_thrift
from opentelemetry.exporter.jaeger.thrift.send import AgentClientUDP, Collector
from opentelemetry.exporter.jaeger.thrift.translate import ThriftTranslator, Translate
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_JAEGER_AGENT_HOST, OTEL_EXPORTER_JAEGER_AGENT_PORT, OTEL_EXPORTER_JAEGER_AGENT_SPLIT_OVERSIZED_BATCHES, OTEL_EXPORTER_JAEGER_ENDPOINT, OTEL_EXPORTER_JAEGER_PASSWORD, OTEL_EXPORTER_JAEGER_TIMEOUT, OTEL_EXPORTER_JAEGER_USER
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace.export import SpanExportResult, SpanExporter

"""

OpenTelemetry Jaeger Thrift Exporter
------------------------------------

The **OpenTelemetry Jaeger Thrift Exporter** allows to export `OpenTelemetry`_ traces to `Jaeger`_.
This exporter always sends traces to the configured agent using the Thrift compact protocol over UDP.
When it is not feasible to deploy Jaeger Agent next to the application, for example, when the
application code is running as Lambda function, a collector can be configured to send spans
using Thrift over HTTP. If both agent and collector are configured, the exporter sends traces
only to the collector to eliminate the duplicate entries.

Usage
-----

.. code:: python

    from opentelemetry import trace
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    trace.set_tracer_provider(
    TracerProvider(
            resource=Resource.create({SERVICE_NAME: "my-helloworld-service"})
        )
    )
    tracer = trace.get_tracer(__name__)

    # create a JaegerExporter
    jaeger_exporter = JaegerExporter(
        # configure agent
        agent_host_name='localhost',
        agent_port=6831,
        # optional: configure also collector
        # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
        # username=xxxx, # optional
        # password=xxxx, # optional
        # max_tag_value_length=None # optional
    )

    # Create a BatchSpanProcessor and add the exporter to it
    span_processor = BatchSpanProcessor(jaeger_exporter)

    # add to the tracer
    trace.get_tracer_provider().add_span_processor(span_processor)

    with tracer.start_as_current_span('foo'):
        print('Hello world!')

You can configure the exporter with the following environment variables:

- :envvar:`OTEL_EXPORTER_JAEGER_USER`
- :envvar:`OTEL_EXPORTER_JAEGER_PASSWORD`
- :envvar:`OTEL_EXPORTER_JAEGER_ENDPOINT`
- :envvar:`OTEL_EXPORTER_JAEGER_AGENT_PORT`
- :envvar:`OTEL_EXPORTER_JAEGER_AGENT_HOST`
- :envvar:`OTEL_EXPORTER_JAEGER_AGENT_SPLIT_OVERSIZED_BATCHES`
- :envvar:`OTEL_EXPORTER_JAEGER_TIMEOUT`

API
---
.. _Jaeger: https://www.jaegertracing.io/
.. _OpenTelemetry: https://github.com/open-telemetry/opentelemetry-python/
"""
DEFAULT_AGENT_HOST_NAME = ...
DEFAULT_AGENT_PORT = ...
DEFAULT_EXPORT_TIMEOUT = ...
logger = ...
class JaegerExporter(SpanExporter):
    """Jaeger span exporter for OpenTelemetry.

    Args:
        agent_host_name: The host name of the Jaeger-Agent.
        agent_port: The port of the Jaeger-Agent.
        collector_endpoint: The endpoint of the Jaeger collector that uses
            Thrift over HTTP/HTTPS.
        username: The user name of the Basic Auth if authentication is
            required.
        password: The password of the Basic Auth if authentication is
            required.
        max_tag_value_length: Max length string attribute values can have. Set to None to disable.
        udp_split_oversized_batches: Re-emit oversized batches in smaller chunks.
        timeout: Maximum time the Jaeger exporter should wait for each batch export.
    """
    @deprecated(version="1.16.0", reason="Since v1.35, the Jaeger supports OTLP natively. Please use the OTLP exporter instead. Support for this exporter will end July 2023.")
    def __init__(self, agent_host_name: Optional[str] = ..., agent_port: Optional[int] = ..., collector_endpoint: Optional[str] = ..., username: Optional[str] = ..., password: Optional[str] = ..., max_tag_value_length: Optional[int] = ..., udp_split_oversized_batches: bool = ..., timeout: Optional[int] = ...) -> None:
        ...
    
    def export(self, spans) -> SpanExportResult:
        ...
    
    def shutdown(self): # -> None:
        ...
    
    def force_flush(self, timeout_millis: int = ...) -> bool:
        ...
    


