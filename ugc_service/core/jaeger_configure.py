from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider

from core.config import configs


def configure_tracer() -> None:
    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: configs.project_name}))
    jaeger_exporter = JaegerExporter(agent_host_name=configs.jaeger_host, agent_port=configs.jaeger_port)
    processor = BatchSpanProcessor(jaeger_exporter)
    provider.add_span_processor(processor)
    set_tracer_provider(provider)
