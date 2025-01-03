"""
This type stub file was generated by pyright.
"""

from enum import Enum
from deprecated import deprecated

@deprecated(version="1.25.0", reason="Use attributes defined in the :py:const:`opentelemetry.semconv.attributes` and :py:const:`opentelemetry.semconv._incubating.attributes` modules instead.")
class SpanAttributes:
    SCHEMA_URL = ...
    CLIENT_ADDRESS = ...
    CLIENT_PORT = ...
    CLIENT_SOCKET_ADDRESS = ...
    CLIENT_SOCKET_PORT = ...
    HTTP_METHOD = ...
    HTTP_STATUS_CODE = ...
    HTTP_SCHEME = ...
    HTTP_URL = ...
    HTTP_TARGET = ...
    HTTP_REQUEST_CONTENT_LENGTH = ...
    HTTP_RESPONSE_CONTENT_LENGTH = ...
    NET_SOCK_PEER_NAME = ...
    NET_SOCK_PEER_ADDR = ...
    NET_SOCK_PEER_PORT = ...
    NET_PEER_NAME = ...
    NET_PEER_PORT = ...
    NET_HOST_NAME = ...
    NET_HOST_PORT = ...
    NET_SOCK_HOST_ADDR = ...
    NET_SOCK_HOST_PORT = ...
    NET_TRANSPORT = ...
    NET_PROTOCOL_NAME = ...
    NET_PROTOCOL_VERSION = ...
    NET_SOCK_FAMILY = ...
    DESTINATION_DOMAIN = ...
    DESTINATION_ADDRESS = ...
    DESTINATION_PORT = ...
    EXCEPTION_TYPE = ...
    EXCEPTION_MESSAGE = ...
    EXCEPTION_STACKTRACE = ...
    HTTP_REQUEST_METHOD = ...
    HTTP_RESPONSE_STATUS_CODE = ...
    NETWORK_PROTOCOL_NAME = ...
    NETWORK_PROTOCOL_VERSION = ...
    SERVER_ADDRESS = ...
    SERVER_PORT = ...
    HTTP_ROUTE = ...
    URL_SCHEME = ...
    EVENT_NAME = ...
    EVENT_DOMAIN = ...
    LOG_RECORD_UID = ...
    FEATURE_FLAG_KEY = ...
    FEATURE_FLAG_PROVIDER_NAME = ...
    FEATURE_FLAG_VARIANT = ...
    LOG_IOSTREAM = ...
    LOG_FILE_NAME = ...
    LOG_FILE_PATH = ...
    LOG_FILE_NAME_RESOLVED = ...
    LOG_FILE_PATH_RESOLVED = ...
    SERVER_SOCKET_ADDRESS = ...
    POOL = ...
    TYPE = ...
    SERVER_SOCKET_DOMAIN = ...
    SERVER_SOCKET_PORT = ...
    SOURCE_DOMAIN = ...
    SOURCE_ADDRESS = ...
    SOURCE_PORT = ...
    AWS_LAMBDA_INVOKED_ARN = ...
    CLOUDEVENTS_EVENT_ID = ...
    CLOUDEVENTS_EVENT_SOURCE = ...
    CLOUDEVENTS_EVENT_SPEC_VERSION = ...
    CLOUDEVENTS_EVENT_TYPE = ...
    CLOUDEVENTS_EVENT_SUBJECT = ...
    OPENTRACING_REF_TYPE = ...
    DB_SYSTEM = ...
    DB_CONNECTION_STRING = ...
    DB_USER = ...
    DB_JDBC_DRIVER_CLASSNAME = ...
    DB_NAME = ...
    DB_STATEMENT = ...
    DB_OPERATION = ...
    NETWORK_TRANSPORT = ...
    NETWORK_TYPE = ...
    DB_MSSQL_INSTANCE_NAME = ...
    DB_CASSANDRA_PAGE_SIZE = ...
    DB_CASSANDRA_CONSISTENCY_LEVEL = ...
    DB_CASSANDRA_TABLE = ...
    DB_CASSANDRA_IDEMPOTENCE = ...
    DB_CASSANDRA_SPECULATIVE_EXECUTION_COUNT = ...
    DB_CASSANDRA_COORDINATOR_ID = ...
    DB_CASSANDRA_COORDINATOR_DC = ...
    DB_REDIS_DATABASE_INDEX = ...
    DB_MONGODB_COLLECTION = ...
    URL_FULL = ...
    DB_SQL_TABLE = ...
    DB_COSMOSDB_CLIENT_ID = ...
    DB_COSMOSDB_OPERATION_TYPE = ...
    USER_AGENT_ORIGINAL = ...
    DB_COSMOSDB_CONNECTION_MODE = ...
    DB_COSMOSDB_CONTAINER = ...
    DB_COSMOSDB_REQUEST_CONTENT_LENGTH = ...
    DB_COSMOSDB_STATUS_CODE = ...
    DB_COSMOSDB_SUB_STATUS_CODE = ...
    DB_COSMOSDB_REQUEST_CHARGE = ...
    OTEL_STATUS_CODE = ...
    OTEL_STATUS_DESCRIPTION = ...
    FAAS_TRIGGER = ...
    FAAS_INVOCATION_ID = ...
    CLOUD_RESOURCE_ID = ...
    FAAS_DOCUMENT_COLLECTION = ...
    FAAS_DOCUMENT_OPERATION = ...
    FAAS_DOCUMENT_TIME = ...
    FAAS_DOCUMENT_NAME = ...
    URL_PATH = ...
    URL_QUERY = ...
    MESSAGING_SYSTEM = ...
    MESSAGING_OPERATION = ...
    MESSAGING_BATCH_MESSAGE_COUNT = ...
    MESSAGING_CLIENT_ID = ...
    MESSAGING_DESTINATION_NAME = ...
    MESSAGING_DESTINATION_TEMPLATE = ...
    MESSAGING_DESTINATION_TEMPORARY = ...
    MESSAGING_DESTINATION_ANONYMOUS = ...
    MESSAGING_MESSAGE_ID = ...
    MESSAGING_MESSAGE_CONVERSATION_ID = ...
    MESSAGING_MESSAGE_PAYLOAD_SIZE_BYTES = ...
    MESSAGING_MESSAGE_PAYLOAD_COMPRESSED_SIZE_BYTES = ...
    FAAS_TIME = ...
    FAAS_CRON = ...
    FAAS_COLDSTART = ...
    FAAS_INVOKED_NAME = ...
    FAAS_INVOKED_PROVIDER = ...
    FAAS_INVOKED_REGION = ...
    NETWORK_CONNECTION_TYPE = ...
    NETWORK_CONNECTION_SUBTYPE = ...
    NETWORK_CARRIER_NAME = ...
    NETWORK_CARRIER_MCC = ...
    NETWORK_CARRIER_MNC = ...
    NETWORK_CARRIER_ICC = ...
    PEER_SERVICE = ...
    ENDUSER_ID = ...
    ENDUSER_ROLE = ...
    ENDUSER_SCOPE = ...
    THREAD_ID = ...
    THREAD_NAME = ...
    CODE_FUNCTION = ...
    CODE_NAMESPACE = ...
    CODE_FILEPATH = ...
    CODE_LINENO = ...
    CODE_COLUMN = ...
    HTTP_REQUEST_METHOD_ORIGINAL = ...
    HTTP_REQUEST_BODY_SIZE = ...
    HTTP_RESPONSE_BODY_SIZE = ...
    HTTP_RESEND_COUNT = ...
    RPC_SYSTEM = ...
    RPC_SERVICE = ...
    RPC_METHOD = ...
    AWS_REQUEST_ID = ...
    AWS_DYNAMODB_TABLE_NAMES = ...
    AWS_DYNAMODB_CONSUMED_CAPACITY = ...
    AWS_DYNAMODB_ITEM_COLLECTION_METRICS = ...
    AWS_DYNAMODB_PROVISIONED_READ_CAPACITY = ...
    AWS_DYNAMODB_PROVISIONED_WRITE_CAPACITY = ...
    AWS_DYNAMODB_CONSISTENT_READ = ...
    AWS_DYNAMODB_PROJECTION = ...
    AWS_DYNAMODB_LIMIT = ...
    AWS_DYNAMODB_ATTRIBUTES_TO_GET = ...
    AWS_DYNAMODB_INDEX_NAME = ...
    AWS_DYNAMODB_SELECT = ...
    AWS_DYNAMODB_GLOBAL_SECONDARY_INDEXES = ...
    AWS_DYNAMODB_LOCAL_SECONDARY_INDEXES = ...
    AWS_DYNAMODB_EXCLUSIVE_START_TABLE = ...
    AWS_DYNAMODB_TABLE_COUNT = ...
    AWS_DYNAMODB_SCAN_FORWARD = ...
    AWS_DYNAMODB_SEGMENT = ...
    AWS_DYNAMODB_TOTAL_SEGMENTS = ...
    AWS_DYNAMODB_COUNT = ...
    AWS_DYNAMODB_SCANNED_COUNT = ...
    AWS_DYNAMODB_ATTRIBUTE_DEFINITIONS = ...
    AWS_DYNAMODB_GLOBAL_SECONDARY_INDEX_UPDATES = ...
    AWS_S3_BUCKET = ...
    AWS_S3_KEY = ...
    AWS_S3_COPY_SOURCE = ...
    AWS_S3_UPLOAD_ID = ...
    AWS_S3_DELETE = ...
    AWS_S3_PART_NUMBER = ...
    GRAPHQL_OPERATION_NAME = ...
    GRAPHQL_OPERATION_TYPE = ...
    GRAPHQL_DOCUMENT = ...
    MESSAGING_RABBITMQ_DESTINATION_ROUTING_KEY = ...
    MESSAGING_KAFKA_MESSAGE_KEY = ...
    MESSAGING_KAFKA_CONSUMER_GROUP = ...
    MESSAGING_KAFKA_DESTINATION_PARTITION = ...
    MESSAGING_KAFKA_MESSAGE_OFFSET = ...
    MESSAGING_KAFKA_MESSAGE_TOMBSTONE = ...
    MESSAGING_ROCKETMQ_NAMESPACE = ...
    MESSAGING_ROCKETMQ_CLIENT_GROUP = ...
    MESSAGING_ROCKETMQ_MESSAGE_DELIVERY_TIMESTAMP = ...
    MESSAGING_ROCKETMQ_MESSAGE_DELAY_TIME_LEVEL = ...
    MESSAGING_ROCKETMQ_MESSAGE_GROUP = ...
    MESSAGING_ROCKETMQ_MESSAGE_TYPE = ...
    MESSAGING_ROCKETMQ_MESSAGE_TAG = ...
    MESSAGING_ROCKETMQ_MESSAGE_KEYS = ...
    MESSAGING_ROCKETMQ_CONSUMPTION_MODEL = ...
    RPC_GRPC_STATUS_CODE = ...
    RPC_JSONRPC_VERSION = ...
    RPC_JSONRPC_REQUEST_ID = ...
    RPC_JSONRPC_ERROR_CODE = ...
    RPC_JSONRPC_ERROR_MESSAGE = ...
    MESSAGE_TYPE = ...
    MESSAGE_ID = ...
    MESSAGE_COMPRESSED_SIZE = ...
    MESSAGE_UNCOMPRESSED_SIZE = ...
    RPC_CONNECT_RPC_ERROR_CODE = ...
    EXCEPTION_ESCAPED = ...
    URL_FRAGMENT = ...
    NET_PEER_IP = ...
    NET_HOST_IP = ...
    HTTP_SERVER_NAME = ...
    HTTP_HOST = ...
    HTTP_RETRY_COUNT = ...
    HTTP_REQUEST_CONTENT_LENGTH_UNCOMPRESSED = ...
    HTTP_RESPONSE_CONTENT_LENGTH_UNCOMPRESSED = ...
    MESSAGING_DESTINATION = ...
    MESSAGING_DESTINATION_KIND = ...
    MESSAGING_TEMP_DESTINATION = ...
    MESSAGING_PROTOCOL = ...
    MESSAGING_PROTOCOL_VERSION = ...
    MESSAGING_URL = ...
    MESSAGING_CONVERSATION_ID = ...
    MESSAGING_KAFKA_PARTITION = ...
    FAAS_EXECUTION = ...
    HTTP_USER_AGENT = ...
    MESSAGING_RABBITMQ_ROUTING_KEY = ...
    MESSAGING_KAFKA_TOMBSTONE = ...
    NET_APP_PROTOCOL_NAME = ...
    NET_APP_PROTOCOL_VERSION = ...
    HTTP_CLIENT_IP = ...
    HTTP_FLAVOR = ...
    NET_HOST_CONNECTION_TYPE = ...
    NET_HOST_CONNECTION_SUBTYPE = ...
    NET_HOST_CARRIER_NAME = ...
    NET_HOST_CARRIER_MCC = ...
    NET_HOST_CARRIER_MNC = ...
    MESSAGING_CONSUMER_ID = ...
    MESSAGING_KAFKA_CLIENT_ID = ...
    MESSAGING_ROCKETMQ_CLIENT_ID = ...


@deprecated(version="1.18.0", reason="Removed from the specification in favor of `network.protocol.name` and `network.protocol.version` attributes")
class HttpFlavorValues(Enum):
    HTTP_1_0 = ...
    HTTP_1_1 = ...
    HTTP_2_0 = ...
    HTTP_3_0 = ...
    SPDY = ...
    QUIC = ...


@deprecated(version="1.18.0", reason="Removed from the specification")
class MessagingDestinationKindValues(Enum):
    QUEUE = ...
    TOPIC = ...


@deprecated(version="1.21.0", reason="Renamed to NetworkConnectionTypeValues")
class NetHostConnectionTypeValues(Enum):
    WIFI = ...
    WIRED = ...
    CELL = ...
    UNAVAILABLE = ...
    UNKNOWN = ...


@deprecated(version="1.21.0", reason="Renamed to NetworkConnectionSubtypeValues")
class NetHostConnectionSubtypeValues(Enum):
    GPRS = ...
    EDGE = ...
    UMTS = ...
    CDMA = ...
    EVDO_0 = ...
    EVDO_A = ...
    CDMA2000_1XRTT = ...
    HSDPA = ...
    HSUPA = ...
    HSPA = ...
    IDEN = ...
    EVDO_B = ...
    LTE = ...
    EHRPD = ...
    HSPAP = ...
    GSM = ...
    TD_SCDMA = ...
    IWLAN = ...
    NR = ...
    NRNSA = ...
    LTE_CA = ...


@deprecated(version="1.25.0", reason="Use :py:const:`opentelemetry.semconv.attributes.NetworkTransportValues` instead.")
class NetTransportValues(Enum):
    IP_TCP = ...
    IP_UDP = ...
    PIPE = ...
    INPROC = ...
    OTHER = ...


@deprecated(version="1.25.0", reason="Use :py:const:`opentelemetry.semconv.attributes.NetworkType` instead.")
class NetSockFamilyValues(Enum):
    INET = ...
    INET6 = ...
    UNIX = ...


@deprecated(version="1.25.0", reason="Use :py:const:`opentelemetry.semconv.attributes.HttpRequestMethodValues` instead.")
class HttpRequestMethodValues(Enum):
    CONNECT = ...
    DELETE = ...
    GET = ...
    HEAD = ...
    OPTIONS = ...
    PATCH = ...
    POST = ...
    PUT = ...
    TRACE = ...
    OTHER = ...


@deprecated(version="1.25.0", reason="Removed from the specification.")
class EventDomainValues(Enum):
    BROWSER = ...
    DEVICE = ...
    K8S = ...


@deprecated(version="1.25.0", reason="Use :py:const:`opentelemetry.semconv._incubating.attributes.LogIostreamValues` instead.")
class LogIostreamValues(Enum):
    STDOUT = ...
    STDERR = ...


@deprecated(version="1.25.0", reason="Removed from the specification.")
class TypeValues(Enum):
    HEAP = ...
    NON_HEAP = ...


@deprecated(version="1.25.0", reason="Use :py:const:`opentelemetry.semconv._incubating.attributes.OpentracingRefTypeValues` instead.")
class OpentracingRefTypeValues(Enum):
    CHILD_OF = ...
    FOLLOWS_FROM = ...


class DbSystemValues(Enum):
    OTHER_SQL = ...
    MSSQL = ...
    MSSQLCOMPACT = ...
    MYSQL = ...
    ORACLE = ...
    DB2 = ...
    POSTGRESQL = ...
    REDSHIFT = ...
    HIVE = ...
    CLOUDSCAPE = ...
    HSQLDB = ...
    PROGRESS = ...
    MAXDB = ...
    HANADB = ...
    INGRES = ...
    FIRSTSQL = ...
    EDB = ...
    CACHE = ...
    ADABAS = ...
    FIREBIRD = ...
    DERBY = ...
    FILEMAKER = ...
    INFORMIX = ...
    INSTANTDB = ...
    INTERBASE = ...
    MARIADB = ...
    NETEZZA = ...
    PERVASIVE = ...
    POINTBASE = ...
    SQLITE = ...
    SYBASE = ...
    TERADATA = ...
    VERTICA = ...
    H2 = ...
    COLDFUSION = ...
    CASSANDRA = ...
    HBASE = ...
    MONGODB = ...
    REDIS = ...
    COUCHBASE = ...
    COUCHDB = ...
    COSMOSDB = ...
    DYNAMODB = ...
    NEO4J = ...
    GEODE = ...
    ELASTICSEARCH = ...
    MEMCACHED = ...
    COCKROACHDB = ...
    OPENSEARCH = ...
    CLICKHOUSE = ...
    SPANNER = ...
    TRINO = ...


class NetworkTransportValues(Enum):
    TCP = ...
    UDP = ...
    PIPE = ...
    UNIX = ...


class NetworkTypeValues(Enum):
    IPV4 = ...
    IPV6 = ...


class DbCassandraConsistencyLevelValues(Enum):
    ALL = ...
    EACH_QUORUM = ...
    QUORUM = ...
    LOCAL_QUORUM = ...
    ONE = ...
    TWO = ...
    THREE = ...
    LOCAL_ONE = ...
    ANY = ...
    SERIAL = ...
    LOCAL_SERIAL = ...


class DbCosmosdbOperationTypeValues(Enum):
    INVALID = ...
    CREATE = ...
    PATCH = ...
    READ = ...
    READ_FEED = ...
    DELETE = ...
    REPLACE = ...
    EXECUTE = ...
    QUERY = ...
    HEAD = ...
    HEAD_FEED = ...
    UPSERT = ...
    BATCH = ...
    QUERY_PLAN = ...
    EXECUTE_JAVASCRIPT = ...


class DbCosmosdbConnectionModeValues(Enum):
    GATEWAY = ...
    DIRECT = ...


class OtelStatusCodeValues(Enum):
    OK = ...
    ERROR = ...


class FaasTriggerValues(Enum):
    DATASOURCE = ...
    HTTP = ...
    PUBSUB = ...
    TIMER = ...
    OTHER = ...


class FaasDocumentOperationValues(Enum):
    INSERT = ...
    EDIT = ...
    DELETE = ...


class MessagingOperationValues(Enum):
    PUBLISH = ...
    RECEIVE = ...
    PROCESS = ...


class FaasInvokedProviderValues(Enum):
    ALIBABA_CLOUD = ...
    AWS = ...
    AZURE = ...
    GCP = ...
    TENCENT_CLOUD = ...


class NetworkConnectionTypeValues(Enum):
    WIFI = ...
    WIRED = ...
    CELL = ...
    UNAVAILABLE = ...
    UNKNOWN = ...


class NetworkConnectionSubtypeValues(Enum):
    GPRS = ...
    EDGE = ...
    UMTS = ...
    CDMA = ...
    EVDO_0 = ...
    EVDO_A = ...
    CDMA2000_1XRTT = ...
    HSDPA = ...
    HSUPA = ...
    HSPA = ...
    IDEN = ...
    EVDO_B = ...
    LTE = ...
    EHRPD = ...
    HSPAP = ...
    GSM = ...
    TD_SCDMA = ...
    IWLAN = ...
    NR = ...
    NRNSA = ...
    LTE_CA = ...


class RpcSystemValues(Enum):
    GRPC = ...
    JAVA_RMI = ...
    DOTNET_WCF = ...
    APACHE_DUBBO = ...
    CONNECT_RPC = ...


class GraphqlOperationTypeValues(Enum):
    QUERY = ...
    MUTATION = ...
    SUBSCRIPTION = ...


class MessagingRocketmqMessageTypeValues(Enum):
    NORMAL = ...
    FIFO = ...
    DELAY = ...
    TRANSACTION = ...


class MessagingRocketmqConsumptionModelValues(Enum):
    CLUSTERING = ...
    BROADCASTING = ...


class RpcGrpcStatusCodeValues(Enum):
    OK = ...
    CANCELLED = ...
    UNKNOWN = ...
    INVALID_ARGUMENT = ...
    DEADLINE_EXCEEDED = ...
    NOT_FOUND = ...
    ALREADY_EXISTS = ...
    PERMISSION_DENIED = ...
    RESOURCE_EXHAUSTED = ...
    FAILED_PRECONDITION = ...
    ABORTED = ...
    OUT_OF_RANGE = ...
    UNIMPLEMENTED = ...
    INTERNAL = ...
    UNAVAILABLE = ...
    DATA_LOSS = ...
    UNAUTHENTICATED = ...


class MessageTypeValues(Enum):
    SENT = ...
    RECEIVED = ...


class RpcConnectRpcErrorCodeValues(Enum):
    CANCELLED = ...
    UNKNOWN = ...
    INVALID_ARGUMENT = ...
    DEADLINE_EXCEEDED = ...
    NOT_FOUND = ...
    ALREADY_EXISTS = ...
    PERMISSION_DENIED = ...
    RESOURCE_EXHAUSTED = ...
    FAILED_PRECONDITION = ...
    ABORTED = ...
    OUT_OF_RANGE = ...
    UNIMPLEMENTED = ...
    INTERNAL = ...
    UNAVAILABLE = ...
    DATA_LOSS = ...
    UNAUTHENTICATED = ...


