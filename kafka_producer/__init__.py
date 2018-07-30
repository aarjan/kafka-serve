import os
import env_config
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from exceptions import ProducerException

schemas = {}
for f_name in os.listdir('schema'):
    with open('schema/'+f_name,'rU') as schema:
        
        name = f_name.split('.')[0]
        
        value_schema = avro.loads(schema.read())

        try:
        
            schemas[name] =  AvroProducer(
                {
                "schema.registry.url":'http://localhost:8081',
                "bootstrap.servers" : env_config.CONFIG["kafka_brokers"],
                },
                default_value_schema=value_schema,
            )
        except Exception as e:
            raise ProducerException("could not initialize producer",e)
