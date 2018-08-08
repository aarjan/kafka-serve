import json
import cgi
import io
import os
from kafka_producer import producer
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import reactor
from twisted.internet.task import deferLater
from exceptions import TopicException,AvroException,ProducerException

class EventHandler(Resource):
    logger = None
    
    def do_HEAD(self,request):
        request.setHeader('Content-Type','application/json')
        request.setHeader('Access-Control-Allow-Origin','*')
        request.setHeader('Access-Control-Allow-Methods','POST,OPTIONS')

    def send_message(self,request,status=200,msg={}):
        request.setResponseCode(status)
        self.do_HEAD(request)
        request.write(json.dumps(msg).encode())
        request.finish()
    
    def send_error(self,request,status,error_msg=''):
        self.send_message(request,status,{"msg":"failed","error":error_msg})

    def render_POST(self, request):
         # get request data
        buffer = io.BufferedReader(request.content)
        body = buffer.read()

        d = deferLater(reactor,5,lambda:request)

        data = {}
        try:
            data = json.loads(body.decode('utf8'))
  
        except json.JSONDecodeError as err:
            self.logger.error("error decoding JSON data",error=err)
            reactor.callLater(5, self.send_error(request, 400,"JSON Err: {}".format(err)), request)
            # d.addCallback(self.send_error(request, 400,"JSON Err: {}".format(err)))
            return NOT_DONE_YET

        # parse the query param
        event_name = request.args
        if b'name' not in event_name.keys():
            self.logger.error("incorrect param specified",param=str(event_name))
            # d.addCallback(self.send_error(request, 400,"incorrect param specified"))
            self.send_error(request, 400,"incorrect param specified")
            return NOT_DONE_YET
            
        # send the message to kafka producer
        topic = event_name[b"name"][0].decode('utf-8')

        try:
            producer.produce(topic,value=data)  
        
        except TopicException as e:
            self.logger.error(e.args[0],topic_name=topic,exception_class=e.__class__)
            d.addCallback(self.send_error(request, 400,'{} :{}'.format(e.args[0],topic)))
            return NOT_DONE_YET

        except AvroException as e:
            self.logger.error(e.message,error=e.expression,topic_name=topic,exception_class=e.expression.__class__)
            d.addCallback(self.send_error(request, 422,'{} , topic:{}'.format(e.message,topic)))
            return NOT_DONE_YET

        except ProducerException as e:
            self.logger.fatal(e.message,error=e.expression,exception_class=e.expression.__class__)
            d.addCallback(self.send_error(request, 500,'internal error: {}'.format(e.message)))
            os._exit(1)
        
        d.addCallback(self.send_message(request,200,{"msg":"success"}))
        return NOT_DONE_YET
        





