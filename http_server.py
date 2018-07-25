import env_config
import json
import producer
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse,parse_qs


class RequestHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','POST,OPTIONS')
        self.end_headers()
        
    def do_OPTIONS(self):
        self.send_response(204)
        self.do_HEAD()
        return

    def do_POST(self):
        post_body = self.rfile.read(int(self.headers['Content-Length']))
        data = {}
        try:
            data = json.loads(post_body.decode('utf8'))
        except json.JSONDecodeError as err:
            print("JSON Err: ",err)
            self.send_response(400)
            self.do_HEAD()
            return
        
        # parse the query param
        parsed_path = urlparse(self.path)
        event_name = parse_qs(parsed_path.query)
        if 'name' not in event_name.keys():
            print(event_name,parsed_path)
            self.send_response(400)
            self.do_HEAD()
            self.wfile.write(json.dumps({"error":"Incorrect param specified"}).encode())
            return

        # send the message to kafka producer
        producer.produce(event_name["name"],env_config.CONFIG["kafka_brokers"],data)  

        self.send_response(200)
        self.do_HEAD()

        self.wfile.write(json.dumps({
            'message':'success',
        }).encode())
        return

# if __name__ == '__main__':
#     print('Starting server at http://localhost:8000')
#     server = HTTPServer(('localhost', 8000), RequestHandler)
#     try:
#         server.serve_forever()
#     except KeyboardInterrupt:
#         pass
#     server.server_close()
#     print("\nServer closed.")
