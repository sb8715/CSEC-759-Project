import random
import json
import requests
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

# Save test summary to a log file
def save_to_log_file(results, failed_packets, filename="http_test_results.log"):
    with open(filename, "w") as log_file:
        log_file.write("HTTP Request Test Summary:\n")
        for method, result in results.items():
            log_file.write(f"- {method}: {result['passed']} passed, {result['failed']} failed\n")
        
        log_file.write("\nFailed Test Packets:\n")
        for method, packets in failed_packets.items():
            if packets:
                log_file.write(f"\n[{method} Failed Packets]:\n")
                for i, packet in enumerate(packets, 1):
                    log_file.write(f"Failed Packet {i}:\n{packet}\n")
        log_file.write("\nTest completed.\n")
    print(f"\nTest summary saved to {filename}")

# Flask API setup
app = Flask(__name__)

# Load configuration from config file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
num_packets = config['num_packets']
focus_depth = config['focus_depth']
fuzzer_url = config['fuzzer_url']

# To record test results
test_results = {method: {"passed": 0, "failed": 0} for method in HTTP_METHODS}
failed_packets = {method: [] for method in HTTP_METHODS}  # To store failed packets

@app.route('/run_tests', methods=['POST'])
def run_tests():
    print("Starting the testing process...")
    for method in HTTP_METHODS:
        print(f"\nTesting HTTP method: {method}")
        for i in range(num_packets):
            packet = generate_http_request(method)
            print(f"Generated packet {i + 1} for method {method}:\n{packet}\n")
            # Send packet to fuzzer for testing
            response = requests.post(fuzzer_url, json={"packet": packet})
            if response.status_code != 200:
                print("Error: Fuzzer returned an error.")
                return jsonify({"error": "Fuzzer returned an error."}), 500
            
            result = response.json().get('result')
            print(f"Fuzzer returned result: {'Passed' if result == 0 else 'Failed'}")
            if result == 0:
                test_results[method]["passed"] += 1
            elif result == 1:
                test_results[method]["failed"] += 1
                failed_packets[method].append(packet)
                # Focused testing for failed packets
                print(f"Starting focused testing for failed packet {i + 1}...")
                for j in range(focus_depth):
                    focused_packet = generate_http_request(method)
                    print(f"Generated focused packet {j + 1} for method {method}:\n{focused_packet}\n")
                    focused_response = requests.post(fuzzer_url, json={"packet": focused_packet})
                    if focused_response.status_code != 200:
                        print("Error: Fuzzer returned an error during focused testing.")
                        return jsonify({"error": "Fuzzer returned an error during focused testing."}), 500
                    focused_result = focused_response.json().get('result')
                    print(f"Fuzzer returned result for focused packet: {'Passed' if focused_result == 0 else 'Failed'}")
                    if focused_result == 0:
                        test_results[method]["passed"] += 1
                    elif focused_result == 1:
                        test_results[method]["failed"] += 1
                        failed_packets[method].append(focused_packet)
    
    print("\nTesting process completed.")
    return jsonify({"message": "Testing completed."})

@app.route('/test_summary', methods=['GET'])
def test_summary():
    print("Fetching test summary...")
    return jsonify({"results": test_results, "failed_packets": failed_packets})

if __name__ == "__main__":
    print("Starting HTTP Packet Generator on port 5000...")
    app.run(host='0.0.0.0', port=5000)
