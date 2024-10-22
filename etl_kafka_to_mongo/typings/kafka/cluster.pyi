"""
This type stub file was generated by pyright.
"""

log = ...
class ClusterMetadata:
    """
    A class to manage kafka cluster metadata.

    This class does not perform any IO. It simply updates internal state
    given API responses (MetadataResponse, GroupCoordinatorResponse).

    Keyword Arguments:
        retry_backoff_ms (int): Milliseconds to backoff when retrying on
            errors. Default: 100.
        metadata_max_age_ms (int): The period of time in milliseconds after
            which we force a refresh of metadata even if we haven't seen any
            partition leadership changes to proactively discover any new
            brokers or partitions. Default: 300000
        bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
            strings) that the client should contact to bootstrap initial
            cluster metadata. This does not have to be the full node list.
            It just needs to have at least one broker that will respond to a
            Metadata API Request. Default port is 9092. If no servers are
            specified, will default to localhost:9092.
    """
    DEFAULT_CONFIG = ...
    def __init__(self, **configs) -> None:
        ...
    
    def is_bootstrap(self, node_id): # -> bool:
        ...
    
    def brokers(self): # -> set[Any]:
        """Get all BrokerMetadata

        Returns:
            set: {BrokerMetadata, ...}
        """
        ...
    
    def broker_metadata(self, broker_id): # -> None:
        """Get BrokerMetadata

        Arguments:
            broker_id (int): node_id for a broker to check

        Returns:
            BrokerMetadata or None if not found
        """
        ...
    
    def partitions_for_topic(self, topic): # -> set[Any] | None:
        """Return set of all partitions for topic (whether available or not)

        Arguments:
            topic (str): topic to check for partitions

        Returns:
            set: {partition (int), ...}
        """
        ...
    
    def available_partitions_for_topic(self, topic): # -> set[Any] | None:
        """Return set of partitions with known leaders

        Arguments:
            topic (str): topic to check for partitions

        Returns:
            set: {partition (int), ...}
            None if topic not found.
        """
        ...
    
    def leader_for_partition(self, partition): # -> None:
        """Return node_id of leader, -1 unavailable, None if unknown."""
        ...
    
    def partitions_for_broker(self, broker_id): # -> set[Any] | None:
        """Return TopicPartitions for which the broker is a leader.

        Arguments:
            broker_id (int): node id for a broker

        Returns:
            set: {TopicPartition, ...}
            None if the broker either has no partitions or does not exist.
        """
        ...
    
    def coordinator_for_group(self, group): # -> None:
        """Return node_id of group coordinator.

        Arguments:
            group (str): name of consumer group

        Returns:
            int: node_id for group coordinator
            None if the group does not exist.
        """
        ...
    
    def ttl(self): # -> float:
        """Milliseconds until metadata should be refreshed"""
        ...
    
    def refresh_backoff(self): # -> int | list[Any]:
        """Return milliseconds to wait before attempting to retry after failure"""
        ...
    
    def request_update(self): # -> Future:
        """Flags metadata for update, return Future()

        Actual update must be handled separately. This method will only
        change the reported ttl()

        Returns:
            kafka.future.Future (value will be the cluster object after update)
        """
        ...
    
    def topics(self, exclude_internal_topics=...): # -> set[Any]:
        """Get set of known topics.

        Arguments:
            exclude_internal_topics (bool): Whether records from internal topics
                (such as offsets) should be exposed to the consumer. If set to
                True the only way to receive records from an internal topic is
                subscribing to it. Default True

        Returns:
            set: {topic (str), ...}
        """
        ...
    
    def failed_update(self, exception): # -> None:
        """Update cluster state given a failed MetadataRequest."""
        ...
    
    def update_metadata(self, metadata): # -> None:
        """Update cluster state given a MetadataResponse.

        Arguments:
            metadata (MetadataResponse): broker response to a metadata request

        Returns: None
        """
        ...
    
    def add_listener(self, listener): # -> None:
        """Add a callback function to be called on each metadata update"""
        ...
    
    def remove_listener(self, listener): # -> None:
        """Remove a previously added listener callback"""
        ...
    
    def add_group_coordinator(self, group, response): # -> str | None:
        """Update with metadata for a group coordinator

        Arguments:
            group (str): name of group from GroupCoordinatorRequest
            response (GroupCoordinatorResponse): broker response

        Returns:
            string: coordinator node_id if metadata is updated, None on error
        """
        ...
    
    def with_partitions(self, partitions_to_add): # -> ClusterMetadata:
        """Returns a copy of cluster metadata with partitions added"""
        ...
    
    def __str__(self) -> str:
        ...
    


