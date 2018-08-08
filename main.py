import os
import env_config
from logger import log
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from http_handler import EventHandler
from http_server import RequestHandler
from http.server import HTTPServer

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
    
    # RequestHandler.logger = log
    # server = HTTPServer((host,port),RequestHandler)

    # try:
    #     server.serve_forever()
    # except KeyboardInterrupt:
    #     pass
    # server.server_close()

    root = Resource()
    handler = EventHandler()
    handler.logger = log
    root.putChild(b"event", handler)
    factory = Site(root)
    endpoint = endpoints.TCP4ServerEndpoint(reactor, 8880)
    endpoint.listen(factory)
    try:
        reactor.run()
    except KeyboardInterrupt:
        pass

    log.info("server closed.")
    print('Server Closed.')
    os._exit(1)

if __name__ == "__main__" :
    Main() 