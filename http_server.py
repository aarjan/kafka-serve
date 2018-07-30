import os
import json
import env_config
from kafka_producer import producer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from exceptions import TopicException,ProducerException,AvroException

    
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
            self.logger.error("error decoding JSON",error=err)
            self.send_error(400,"JSON Err: {}".format(err))
            return
        
        # parse the query param
        parsed_path = urlparse(self.path)
        event_name = parse_qs(parsed_path.query)
        if 'name' not in event_name.keys():
            self.logger.error("incorrect param specified",param=event_name,path=parsed_path.path)
            self.send_error(400,"incorrect param specified")
            return

        # send the message to kafka producer
        topic = event_name["name"][0]
        
        try:
            producer.produce(topic,value=data)  
        
        except TopicException as e:
            self.send_error(500,'{} :{}'.format(e.args[0],topic))
            self.logger.error(e.args[0],topic_name=topic,exception_class=e.__class__)
            return

        except AvroException as e:
            self.send_error(500,'{} , topic:{}'.format(e.message,topic))
            self.logger.error(e.message,error=e.expression,topic_name=topic,exception_class=e.__class__)
            return

        except ProducerException as e:
            self.send_error(500,'internal error: {}'.format(e.message))
            self.logger.fatal(e.message,error=e.expression,exception_class=e.expression.__class__)
            os._exit(1)
        
        self.send_message(200,{"msg":"success"})
        return
