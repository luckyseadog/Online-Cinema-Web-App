"""
This type stub file was generated by pyright.
"""

class MetricName:
    """
    This class encapsulates a metric's name, logical group and its
    related attributes (tags).

    group, tags parameters can be used to create unique metric names.
    e.g. domainName:type=group,key1=val1,key2=val2

    Usage looks something like this:

        # set up metrics:
        metric_tags = {'client-id': 'producer-1', 'topic': 'topic'}
        metric_config = MetricConfig(tags=metric_tags)

        # metrics is the global repository of metrics and sensors
        metrics = Metrics(metric_config)

        sensor = metrics.sensor('message-sizes')
        metric_name = metrics.metric_name('message-size-avg',
                                          'producer-metrics',
                                          'average message size')
        sensor.add(metric_name, Avg())

        metric_name = metrics.metric_name('message-size-max',
        sensor.add(metric_name, Max())

        tags = {'client-id': 'my-client', 'topic': 'my-topic'}
        metric_name = metrics.metric_name('message-size-min',
                                          'producer-metrics',
                                          'message minimum size', tags)
        sensor.add(metric_name, Min())

        # as messages are sent we record the sizes
        sensor.record(message_size)
    """

    def __init__(self, name, group, description=..., tags=...) -> None:
        """
        Arguments:
            name (str): The name of the metric.
            group (str): The logical group name of the metrics to which this
                metric belongs.
            description (str, optional): A human-readable description to
                include in the metric.
            tags (dict, optional): Additional key/val attributes of the metric.

        """

    @property
    def name(self):  # -> Any:
        ...
    @property
    def group(self):  # -> Any:
        ...
    @property
    def description(self):  # -> None:
        ...
    @property
    def tags(self):  # -> dict[Any, Any] | None:
        ...
    def __hash__(self) -> int: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
