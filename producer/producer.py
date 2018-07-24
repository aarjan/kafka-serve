from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import time 
import sys

value_schema_str = """
{
    "name":"accesslog",
    "type":"record",
    "fields":[{
        "name":"msg",
        "type":["null","string"]
    },
    {
        "name":"code",
        "type":["null","int"]
    }]
}
"""
value_schema = avro.loads(value_schema_str)

conf = {
    "bootstrap.servers":"localhost:9092",
    "schema.registry.url":"http://localhost:8081"
}

def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %o\n' %
                            (msg.topic(), msg.partition(), msg.offset()))
                            

avroProducer = AvroProducer(conf,default_value_schema=value_schema)


for i in range(100):
    event = {'msg':"hey from python","code":"2"}
    try:
        avroProducer.produce(topic='accesslog',value=event)
    except avro.SerializerError as err:
        print("Error occurred",err)
flush_time = time.time()

avroProducer.flush()