from flask import Flask, jsonify, request
import ssl
import requests
import threading
import time

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    return jsonify({"message": "Hello from Server!"})

def call_client():
    url = 'https://localhost:5001/api'
    cert = ('certs/server.crt', 'certs/server.key')
    while True:
        try:
            response = requests.get(url, cert=cert, verify='certs/ca-crt.pem')
            print("Server received from Client:", response.json())
        except Exception as e:
            print("Error calling Server:", e)
        time.sleep(10)
        
if __name__ == '__main__':
    threading.Thread(target=call_client, daemon=True).start()
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='certs/server.crt', keyfile='certs/server.key')
    context.load_verify_locations(cafile='certs/ca-crt.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    app.run(host='localhost', port=5000, ssl_context=context)
