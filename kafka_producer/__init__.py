import os
import env_config
from logger import log
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from exceptions import ProducerException

_SCHEMA_PATH = 'schema'
schemas = {}

for f_name in os.listdir(_SCHEMA_PATH):
    
    with open(_SCHEMA_PATH + '/' + f_name,'r') as schema:
        name = f_name.split('.')[0]

        try:
            value_schema = avro.loads(schema.read())
            
            schemas[name] =  AvroProducer(
                {
                    "schema.registry.url":'http://localhost:8081',
                    "bootstrap.servers" : env_config.CONFIG["kafka_brokers"],
                },
                default_value_schema=value_schema,
            )
            log.debug("Loaded avro schema into schema directory",schema_name=name)
        except Exception as e:
            print(name)
            raise ProducerException("could not initialize producer",e)