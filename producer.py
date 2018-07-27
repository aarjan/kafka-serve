import time 
import sys
import os
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from exceptions import ProducerException,TopicException

_conf = {
    "schema.registry.url":"http://localhost:8081"
}

schemas = {}
for f_name in os.listdir('schema'):
    with open('schema/'+f_name,'rU') as schema:
        schemas[f_name.split('.')[0]] = avro.loads(schema.read())


def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %o\n' %
                            (msg.topic(), msg.partition(), msg.offset()))


"""
    Produce msg to kakfa.
    The 'topic' name is used to find the avro_schema to that topic.
"""
def produce(topic='',brokers='',value={}):
    _conf["bootstrap.servers"] = brokers

    if topic not in schemas.keys():
        raise TopicException("incorrect topic name")

    try:
        avroProducer = AvroProducer(_conf,default_value_schema=schemas[topic])
        avroProducer.produce(topic=topic,value=value,callback=delivery_callback)
    except Exception as err:
        raise ProducerException("error Producing msg: ",err) 

    avroProducer.flush()