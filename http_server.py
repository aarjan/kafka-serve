import os
import json
import config
from kafka_producer import producer
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
    
    def send_message(self,status=200,msg={}):
        self.send_response(status)
        self.do_HEAD()
        self.wfile.write(json.dumps(msg).encode())
    
    def send_error(self,status,error_msg=''):
        self.send_message(status,{"msg":"failed","error":error_msg})
    
    def log_msg(self,msg='',**kwargs):
        self.logger.info(msg,**kwargs)

    def log_error(self,msg='',**kwargs):
        self.logger.error(msg,**kwargs)

    def log_fatal(self,msg='',**kwargs):
        self.logger.fatal(msg,**kwargs)
        os._exit(1)

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
            self.log_error("error decoding JSON",error=err)
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
            producer.produce(topic,value=data)  
        
        except TopicException as e:
            self.send_error(500,'{} :{}'.format(e.args[0],topic))
            self.log_error(e.args[0],topic_name=topic,exception_class=e.__class__)
            return

        except ProducerException as e:
            self.send_error(500,'internal error: {}'.format(e.message))
            self.log_fatal(e.message,error=e.expression,exception_class=e.expression.__class__)
            
        except Exception as e:
            self.send_error(500,str(e))
            self.log_fatal('unknown error',error = str(e),exception_class=e.__class__)

        self.send_message(200,{"msg":"success"})
        return
