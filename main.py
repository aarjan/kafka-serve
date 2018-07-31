from logger import log
from http.server import HTTPServer
from http_server import RequestHandler
import env_config

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

def Main():
    if log == None:
        raise 'log not initialized'

    """
        Running http server that listens at /event
    """

    host = env_config.CONFIG["server_host"]
    port = env_config.CONFIG["server_port"]

    print('Starting server at http://{}:{}'.format(host,port))
    log.info('server started',host=host,port=port)
    
    RequestHandler.logger = log
    server = HTTPServer((host,port),RequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

    log.info("server closed.")
    print('Server Closed.')

if __name__ == "__main__" :
    Main() 