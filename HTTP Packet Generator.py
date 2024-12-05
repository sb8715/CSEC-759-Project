import random
import json
from flask import Flask, request, jsonify

# Define HTTP methods and packet generation rules
HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]

# Expanded set of hostnames and paths
HOSTNAMES = ["example.com", "google.com", "rit.edu", "openai.com", "github.com"]
URL_PATHS = ["/", "/index", "/home", "/api/v1/resource", "/docs", "/search"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "curl/7.68.0",
    "HTTPie/2.4.0",
    "PostmanRuntime/7.28.4",
]

# Flask app setup
app = Flask(__name__)

# Load configuration from a file
def load_config(filename="config.json"):
    with open(filename, "r") as config_file:
        config = json.load(config_file)
    return config

# Generate an HTTP request packet with diverse content
def generate_http_request(method):
    hostname = random.choice(HOSTNAMES)
    url = random.choice(URL_PATHS)
    headers = [
        f"Host: {hostname}",
        f"User-Agent: {random.choice(USER_AGENTS)}",
        "Accept: */*",
        "Connection: keep-alive",
    ]
    body = '{"key":"value", "id":123, "status":"active"}'  # Example JSON body

    header_str = "\r\n".join(headers)

    if method in ["POST", "PUT"]:
        request = f"{method} {url} HTTP/1.1\r\n{header_str}\r\n\r\n{body}"
    else:
        request = f"{method} {url} HTTP/1.1\r\n{header_str}\r\n\r\n"
    return request

# API endpoint to start packet generation
@app.route('/start', methods=['POST'])
def start_generation():
    config = load_config()
    num_packets = config.get("num_packets", 10)
    focus_depth = config.get("focus_depth", 5)

    results = {method: {"passed": 0, "failed": 0} for method in HTTP_METHODS}
    failed_packets = {method: [] for method in HTTP_METHODS}  # To store failed packets

    # Iterate over each HTTP method and generate packets
    for method in HTTP_METHODS:
        for i in range(num_packets):
            packet = generate_http_request(method)
            # Send packet to the external program and wait for the response
            response = request.json.get(f"{method}_packet_{i}_result", "0")
            if response == "0":
                results[method]["passed"] += 1
            elif response == "1":
                results[method]["failed"] += 1
                failed_packets[method].append(packet)
                for j in range(focus_depth):
                    focused_packet = generate_http_request(method)
                    focused_response = request.json.get(f"focused_{method}_packet_{j}_result", "0")
                    if focused_response == "0":
                        results[method]["passed"] += 1
                    elif focused_response == "1":
                        results[method]["failed"] += 1
                        failed_packets[method].append(focused_packet)

    # Return test summary as a response
    summary = {method: {"passed": results[method]["passed"], "failed": results[method]["failed"]} for method in HTTP_METHODS}
    return jsonify(summary)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
