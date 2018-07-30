from logger.logger import log
from http.server import HTTPServer
from http_server import RequestHandler

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

def Main():
    if log == None:
        raise 'log not initialized'
    
    
    """
        Running http server that listens at /event
    """

    log.info('Starting server at http://localhost:8000')
    
    RequestHandler.logger = log
    server = HTTPServer(('localhost', 8000),RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    log.info("Server closed.")


if __name__ == "__main__" :
    Main() 