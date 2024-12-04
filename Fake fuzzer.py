from flask import Flask, request, jsonify
import random

# Flask app setup for simulating the fuzzer
app = Flask(__name__)

@app.route('/api/test', methods=['POST'])
def fuzzer_test():
    # Simulate the testing process by receiving the packet and returning a random result
    data = request.get_json()
    packet = data.get('packet')
    
    # Print the received packet to the console
    print(f"Received packet for testing: {packet}")
    
    # Randomly return 0 (passed) or 1 (failed)
    result = random.choice([0, 1])
    
    # Print the result to the console
    print(f"Test result: {'Passed' if result == 0 else 'Failed'}")
    
    return jsonify({"result": result})

if __name__ == "__main__":
    # Run the fuzzer simulator on port 6000
    print("Starting Fuzzer Simulator on port 6000...")
    app.run(host='0.0.0.0', port=6000)
