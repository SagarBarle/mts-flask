from flask import Flask, jsonify, request
import ssl
import requests
import threading
import time

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    return jsonify({"message": "Hello from Server!"}),200

def call_server():
    url = 'https://localhost:5000/api'
    cert = ('certs/client.crt', 'certs/client.key')
    while True:
        try:
            response = requests.get(url, cert=cert, verify='certs/ca-crt.pem')
            print("Client received from Server:", response.json())
        except Exception as e:
            print("Error calling Server:", e)
        time.sleep(10)  

if __name__ == '__main__':
    
    threading.Thread(target=call_server, daemon=True).start()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='certs/server.crt', keyfile='certs/server.key')
    context.load_verify_locations(cafile='certs/ca-crt.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    app.run(host='localhost', port=5001, ssl_context=context)
