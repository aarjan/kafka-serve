import os

_server_host = os.environ.get('EVENT_SERVER_HOST', 'localhost')
_server_port = os.environ.get('EVENT_SERVER_PORT', 8080)
_debug = os.environ.get('EVENT_SERVER_DEBUG', False)
_log_file_handler = os.environ.get('EVENT_LOG_FILE_HANDLER', False)
_kafka_brokers = os.environ.get('EVENT_KAFKA_BROKERS','localhost:9092')
_system_log_code = os.environ.get('EVENT_SYSTEM_LOG_CODE', 'event-server')

CONFIG = {
    'server_host':_server_host,
    'server_port':_server_port,
    'debug':_debug,
    'log_file_handler':_log_file_handler,
    'kafka_brokers':_kafka_brokers,
    'system_log_code':_system_log_code,
}