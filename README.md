# A simple python HTTP-AVRO-KAFKA server

- Accepts JSON POST request at '/event?name=[kafka_topic_name]'.
- The JSON data should match the correspoding Avro schema.
- Eg:  
    `curl -v -H 'Content-Type:application/json'  'localhost:8000/event?name=acesslog' -d '{"msg":"good"}'`

## Dependencies

- Python specific dependencies are in the [requirements.txt](requirements.txt)
- Confluent Kafka with schema registry [installer](https://docs.confluent.io/current/installation/installing_cp/zip-tar.html)