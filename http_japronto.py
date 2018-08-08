from japronto import Application
import os
import json
from kafka_producer import producer
from exceptions import TopicException,AvroException,ProducerException


def do_POST(request):
    # get request data
    data = {}
    try:
        data = request.json
    except json.JSONDecodeError as err:
        return request.Response(
            code=400,
            json={"error":"JSON Err: {}".format(err)},
        )

    if 'name' not in request.query.keys():
        return request.Response(
            code=400,
            json={"error":"incorrect param specified"},
        )

    # send the message to kafka producer
    topic = request.query["name"]
    try:
        producer.produce(topic,value=data)  
    
    except TopicException as e:
        return request.Response(
            code=400,
            json={"error":'{} :{}'.format(e.args[0],topic)},
        )

    except AvroException as e:
        return request.Response(
            code=400,
            json={"error":'{} , topic:{}'.format(e.message,topic),"data":data},
        )

    except ProducerException as e:
        return request.Response(
            code=500,
            json={"error":'internal error: {}'.format(e.message)},
        )
    
    return request.Response(
            code=200,
            json={"msg":"success"},
        )


def prod_handler(request,exception):
    return request.Response(json="hye")

# The Application instance is a fundamental concept.
# It is a parent to all the resources and all the settings
# can be tweaked here.
app = Application()

# The Router instance lets you register your handlers and execute
# them depending on the url path and methods
app.router.add_route('/event', do_POST)

app.add_error_handler(ProducerException,prod_handler)
# Finally start our server and handle requests until termination is
# requested. Enabling debug lets you see request logs and stack traces.
app.run(debug=True) 