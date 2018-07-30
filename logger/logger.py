import logging.config
import json
from config import env_config
import structlog
from structlog import configure, processors, stdlib, threadlocal


configure(
    context_class=threadlocal.wrap_dict(dict),
    logger_factory=stdlib.LoggerFactory(),
    wrapper_class=stdlib.BoundLogger,
    processors=[
        stdlib.filter_by_level,
        stdlib.add_logger_name,
        stdlib.add_log_level,
        stdlib.PositionalArgumentsFormatter(),
        processors.TimeStamper(fmt="iso"),
        processors.StackInfoRenderer(),
        processors.format_exc_info,
        processors.UnicodeDecoder(),
        stdlib.render_to_log_kwargs]
)

LOGLEVEL = None
log = None
with open('logger/config.json') as f:
    dictConfig = json.loads(f.read())
        
    conf = env_config.CONFIG

    if conf["debug"] == True:
        LOGLEVEL = logging.DEBUG
    else:
        LOGLEVEL = logging.DEBUG

    if conf["log_file_handler"] == True:
        dictConfig["handlers"]["json"]["class"] = 'logging.FileHandler'
        dictConfig["handlers"]["json"]["filename"]= '/tmp/.event_server/server.log'
    else: 
        dictConfig["handlers"]["json"]["class"] = 'logging.StreamHandler'

    dictConfig["loggers"][""]["level"] = LOGLEVEL
    logging.config.dictConfig(dictConfig)

    log = structlog.getLogger(conf["system_log_code"])
    log.info("Logging initialized")     