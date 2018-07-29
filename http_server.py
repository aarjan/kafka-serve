import env_config
import json
import producer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from exceptions import TopicException,ProducerException

    
class RequestHandler(BaseHTTPRequestHandler):
    logger = None

    def do_HEAD(self):
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','POST,OPTIONS')
        self.end_headers()
    
    def send_message(self,status,msg={}):
        self.send_response(status)
        self.do_HEAD()
        self.wfile.write(json.dumps(msg).encode())
    
    def send_error(self,status,error_msg=''):
        self.send_message(status,{"msg":"failed","error":error_msg})
    
    def log_message(self,msg='',**kwargs):
        self.logger.info(msg,**kwargs)

    def log_error(self,error='',**kwargs):
        self.logger.error(error,**kwargs)

    def do_OPTIONS(self):
        self.send_response(204)
        self.do_HEAD()
        return

    def do_POST(self):
        # get request data
        post_body = self.rfile.read(int(self.headers['Content-Length']))
        data = {}
        try:
            data = json.loads(post_body.decode('utf8'))
  
        except json.JSONDecodeError as err:
            self.log_error("error decoding JSON",msg=err)
            self.send_error(400,"JSON Err: {}".format(err))
            return
        
        # parse the query param
        parsed_path = urlparse(self.path)
        event_name = parse_qs(parsed_path.query)
        if 'name' not in event_name.keys():
            self.log_error("incorrect param specified",param=event_name,path=parsed_path.path)
            self.send_error(400,"incorrect param specified")
            return

        # send the message to kafka producer
        topic = event_name["name"][0]
        
        try:
            producer.produce(topic,env_config.CONFIG["kafka_brokers"],data)  
        
        except TopicException as e:
            self.log_error(e.args[0],msg=topic,exception_class=e.__cause__)
            self.send_error(500,str(e.args))
            return

        except ProducerException as e:
            self.log_error(e.message,msg=e.expression,exception_class=e.__cause__)
            self.send_error(500,str(e.args))
            return

        self.log_message("successfully sent data to kafka",body=data)
        self.send_message("sucess")
        return
