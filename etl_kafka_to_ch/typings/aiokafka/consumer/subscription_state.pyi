"""
This type stub file was generated by pyright.
"""

import contextlib
from enum import Enum
from re import Pattern
from collections.abc import Iterable
from aiokafka.abc import ConsumerRebalanceListener
from aiokafka.structs import OffsetAndMetadata, TopicPartition

log = ...

class SubscriptionType(Enum):
    NONE = ...
    AUTO_TOPICS = ...
    AUTO_PATTERN = ...
    USER_ASSIGNED = ...

class SubscriptionState:
    """Intermediate bridge to coordinate work between Consumer, Coordinator
    and Fetcher primitives.

        The class is different from kafka-python's implementation to provide
    a more friendly way to interact in asynchronous paradigm. The changes
    focus on making the internals less mutable (subscription, topic state etc.)
    paired with futures for when those change.
        Before there was a lot of trouble if user say did a subscribe between
    yield statements of a rebalance or other critical IO operation.
    """

    _subscription_type: SubscriptionType = ...
    _subscribed_pattern: str = ...
    _subscription: Subscription = ...
    _listener: ConsumerRebalanceListener = ...
    def __init__(self, loop=...) -> None: ...
    @property
    def subscription(self) -> Subscription: ...
    @property
    def subscribed_pattern(self) -> Pattern: ...
    @property
    def listener(self) -> ConsumerRebalanceListener: ...
    @property
    def topics(self):  # -> set[Any]:
        ...
    def assigned_partitions(self) -> set[TopicPartition]: ...
    @property
    def reassignment_in_progress(self):  # -> bool:
        ...
    def partitions_auto_assigned(self) -> bool: ...
    def is_assigned(self, tp: TopicPartition) -> bool: ...
    def subscribe(self, topics: set[str], listener=...):  # -> None:
        """Subscribe to a list (or tuple) of topics

        Caller: Consumer.
        Affects: SubscriptionState.subscription
        """

    def subscribe_pattern(self, pattern: Pattern, listener=...):  # -> None:
        """Subscribe to all topics matching a regex pattern.
        Subsequent calls `subscribe_from_pattern()` by Coordinator will provide
        the actual subscription topics.

        Caller: Consumer.
        Affects: SubscriptionState.subscribed_pattern
        """

    def assign_from_user(self, partitions: Iterable[TopicPartition]):  # -> None:
        """Manually assign partitions. After this call automatic assignment
        will be impossible and will raise an ``IllegalStateError``.

        Caller: Consumer.
        Affects: SubscriptionState.subscription
        """

    def unsubscribe(self):  # -> None:
        """Unsubscribe from the last subscription. This will also clear the
        subscription type.

        Caller: Consumer.
        Affects: SubscriptionState.subscription
        """

    def subscribe_from_pattern(self, topics: set[str]):  # -> None:
        """Change subscription on cluster metadata update if a new topic
        created or one is removed.

        Caller: Coordinator
        Affects: SubscriptionState.subscription
        """

    def assign_from_subscribed(self, assignment: set[TopicPartition]):  # -> None:
        """Set assignment if automatic assignment is used.

        Caller: Coordinator
        Affects: SubscriptionState.subscription.assignment
        """

    def begin_reassignment(self):  # -> None:
        """Signal from Coordinator that a group re-join is needed. For example
        this will be called if a commit or heartbeat fails with an
        InvalidMember error.

        Caller: Coordinator
        """

    def seek(self, tp: TopicPartition, offset: int):  # -> None:
        """Force reset of position to the specified offset.

        Caller: Consumer, Fetcher
        Affects: TopicPartitionState.position
        """

    def wait_for_subscription(self):  # -> Future[Any]:
        """Wait for subscription change. This will always wait for next
        subscription.
        """

    def wait_for_assignment(self):  # -> Future[Any]:
        """Wait for next assignment. Be careful, as this will always wait for
        next assignment, even if the current one is active.
        """

    def register_fetch_waiters(self, waiters):  # -> None:
        ...
    def abort_waiters(self, exc):  # -> None:
        """Critical error occurred, we will abort any pending waiter"""

    def pause(self, tp: TopicPartition) -> None: ...
    def paused_partitions(self) -> set[TopicPartition]: ...
    def resume(self, tp: TopicPartition) -> None: ...
    @contextlib.contextmanager
    def fetch_context(self):  # -> Generator[None, Any, None]:
        ...
    @property
    def fetcher_idle_time(self):  # -> float | Literal[0]:
        """How much time (in seconds) spent without consuming any records"""

class Subscription:
    """Describes current subscription to a list of topics. In case of pattern
    subscription a new instance of this class will be created if number of
    matched topics change.

    States:
        * Subscribed
        * Assigned (assignment was set)
        * Unsubscribed
    """

    def __init__(self, topics: Iterable[str], loop=...) -> None: ...
    @property
    def active(self):  # -> bool:
        ...
    @property
    def topics(self): ...
    @property
    def assignment(self):  # -> Assignment:
        ...

class ManualSubscription(Subscription):
    """Describes a user assignment"""

    def __init__(self, user_assignment: Iterable[TopicPartition], loop=...) -> None: ...

class Assignment:
    """Describes current partition assignment. New instance will be created
    on each group rebalance if automatic assignment is used.

    States:
        * Assigned
        * Unassigned
    """

    def __init__(self, topic_partitions: Iterable[TopicPartition]) -> None: ...
    @property
    def tps(self):  # -> frozenset[TopicPartition]:
        ...
    @property
    def active(self):  # -> bool:
        ...
    def state_value(self, tp: TopicPartition) -> TopicPartitionState: ...
    def all_consumed_offsets(self) -> dict[TopicPartition, OffsetAndMetadata]:
        """Returns consumed offsets as {TopicPartition: OffsetAndMetadata}"""

    def requesting_committed(self):  # -> list[Any]:
        """Return all partitions that are requesting commit point fetch"""

class PartitionStatus(Enum):
    AWAITING_RESET = ...
    CONSUMING = ...
    UNASSIGNED = ...

class TopicPartitionState:
    """Shared Partition metadata state.

    After creation the workflow is similar to:

        * Partition assigned to this consumer (AWAITING_RESET)
        * Fetcher either uses commit save point or resets position in respect
          to defined reset policy (AWAITING_RESET -> CONSUMING)
        * Fetcher loads a new batch of records, yields results to consumer
          and updates consumed position (CONSUMING)
        * Assignment changed or subscription changed (CONSUMING -> UNASSIGNED)

    """

    def __init__(self, assignment) -> None: ...
    @property
    def paused(self):  # -> bool:
        ...
    @property
    def resume_fut(self):  # -> Future[Any] | None:
        ...
    @property
    def has_valid_position(self) -> bool: ...
    @property
    def position(self) -> int: ...
    @property
    def awaiting_reset(self):  # -> bool:
        ...
    @property
    def reset_strategy(self) -> int: ...
    def await_reset(self, strategy):  # -> None:
        """Called by either Coonsumer in `seek_to_*` or by Coordinator after
        setting initial committed point.
        """

    def fetch_committed(self):  # -> Future[Any]:
        ...
    def update_committed(self, offset_meta: OffsetAndMetadata):  # -> None:
        """Called by Coordinator on successful commit to update commit cache."""

    def consumed_to(self, position: int):  # -> None:
        """Called by Fetcher when yielding results to Consumer"""

    def reset_to(self, position: int):  # -> None:
        """Called by Fetcher after performing a reset to force position to
        a new point.
        """

    def seek(self, position: int):  # -> None:
        """Called by Consumer to force position to a specific offset"""

    def wait_for_position(self):  # -> Future[Any]:
        ...
    def pause(self):  # -> None:
        ...
    def resume(self):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
