
class ProducerException(Exception):
    """Expression raised for errors producing message to Kafka

    Attributes:
        message -- explanation of error
        expression -- input expression in which the error occurred

    """

    def __init__(self,message,expression):
        self.message = message
        self.expression = expression



class TopicException(Exception):
    """Exceptions raised for incorrect topic name"""
    pass
