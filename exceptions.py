class KafkaException(Exception):
    """Exception raised for errors produced from kafka

    Attributes:
        message -- explanation of error
        expression -- input expression in which the error occurred

    """

    def __init__(self,message,expression):
        self.message = message
        self.expression = expression


class AvroException(KafkaException):
    """Exceptions raised for incorrect avro format"""

    
class ProducerException(KafkaException):
    """Exception raised for errors producing message to Kafka"""


class TopicException(Exception):
    """Exceptions raised for incorrect topic name"""
    pass
