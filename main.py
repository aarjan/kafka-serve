import env_config
import logging
from http.server import HTTPServer
import http_server

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

conf = env_config.CONFIG
log = logging.getLogger(conf["system_log_code"])

if conf["debug"] == True:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

if conf["log_file_handler"] == True:
    handler = logging.FileHandler('/tmp/.event_server/server.log')
else: 
    handler = logging.StreamHandler()

formatter = logging.Formatter(LOG_FORMAT)
handler.setFormatter(formatter)
log.addHandler(handler)

"""
    Running http server that listens at /event
"""
log.info('Starting server at http://localhost:8000')
server = HTTPServer(('localhost', 8000), http_server.RequestHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.server_close()
log.info("Server closed.")