# A simple python HTTP-AVRO-KAFKA server

- Collects data from HTTP server and sends it to Kafka producer
- Accepts JSON POST request at __/event?name=[kafka_topic_name]__.
- The JSON data should match the correspoding Avro schema.


## Dependencies

- Python specific dependencies are in the [requirements.txt](requirements.txt)
- Confluent Kafka with schema registry [installer](https://docs.confluent.io/current/installation/installing_cp/zip-tar.html)

## Run

- Fullfill all the above dependencies
- Add the avro schema you want to send in the [schema](schema) folder with the extenstion '.avsc.json'.
- Create a new file __run.env__ & copy the contents of the [run.env.sample](run.env.sample) into __run.env__ and specify the desired environment variables. 
- Run the kafka instance.
- Run the HTTP server `./run.sh`.
- Now, you can send POST request to the endpoint __/event__ with query param __[kafka_topic_name]__.
- Eg:  
    `curl -v -H 'Content-Type:application/json'  'localhost:8000/event?name=acesslog' -d '{"msg":"good"}'`
