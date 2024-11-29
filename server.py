from flask import Flask, jsonify, request
import ssl
import requests
import threading
import time

app = Flask(__name__)

@app.before_request
def extract_client_cert():
    """Extract client certificate from the SSL connection."""
    peer_cert = request.environ.get('SSL_CLIENT_CERT')  # Access SSL_CLIENT_CERT if set by the WSGI server
    if peer_cert:
        request.client_cert = peer_cert
    else:
        request.client_cert = None

@app.route('/api', methods=['GET'])
def api():
    # Check if client certificate is present
    if request.client_cert:
        return jsonify({
            "message": "Hello from Server!",
            "client_cert": request.client_cert
        })
    return jsonify({"error": "No client certificate provided"}), 403

# Periodic function to call Client
def call_client():
    url = 'https://localhost:5001/api'
    cert = ('certs/client.crt', 'certs/client.key')
    while True:
        try:
            response = requests.get(url, cert=cert, verify='certs/ca-crt.pem')
            print("Server received from Client:", response.json())
        except Exception as e:
            print("Error calling Client:", e)
        time.sleep(10)  # Call every 10 seconds

if __name__ == '__main__':
    # Start periodic thread
    threading.Thread(target=call_client, daemon=True).start()

    # Start Flask server with mTLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='certs/server.crt', keyfile='certs/server.key')
    context.load_verify_locations(cafile='certs/ca-crt.pem')
    context.verify_mode = ssl.CERT_REQUIRED
    app.run(host='localhost', port=5000, ssl_context=context)
