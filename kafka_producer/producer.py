import time 
import sys
from logger import log
from kafka_producer import schemas
from confluent_kafka import avro
from avro.schema import AvroException as AvroError
from confluent_kafka.avro import AvroProducer
from exceptions import ProducerException,TopicException,AvroException

def delivery_callback(err, msg):
    if err:
        log.error("message failed delivery", error = err)
    else:
        log.info("message delivered",topic=msg.topic(), partition=msg.partition(),offset = msg.offset())


"""
    Produce msg to kakfa.
    The 'topic' name is used to find the avro_schema to that topic.
"""
def produce(topic='',brokers='',value={}):

    if topic not in schemas.keys():
        raise TopicException("incorrect topic name")
    
    avroProducer = schemas[topic]
    try:
        avroProducer.produce(topic=topic,value=value,callback=delivery_callback)
    
    except (avro.ClientError,avro.SerializerError,avro.KeySerializerError,avro.ValueSerializerError,AvroError) as err:
        raise AvroException('invalid avro msg',err)

    # TODO: Check for KafkaException
    except Exception as err:
        raise ProducerException("error producing msg",err) 

    avroProducer.flush()