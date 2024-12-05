import requests
import random
import json

def generate_fake_results(num_packets, focus_depth):
    results = {}
    for method in ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]:
        for i in range(num_packets):
            # Simulate a random pass or fail result for each packet
            results[f"{method}_packet_{i}_result"] = str(random.choice([0, 1]))
            # If failed, generate results for focused packets
            if results[f"{method}_packet_{i}_result"] == "1":
                for j in range(focus_depth):
                    results[f"focused_{method}_packet_{j}_result"] = str(random.choice([0, 1]))
    return results

if __name__ == "__main__":
    # Load configuration
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    num_packets = config.get("num_packets", 10)
    focus_depth = config.get("focus_depth", 5)

    # Generate fake results for testing
    fake_results = generate_fake_results(num_packets, focus_depth)

    # Start the packet generation process by making a POST request
    response = requests.post("http://localhost:5000/start", json=fake_results)
    
    # Print the response from the packet generator
    if response.status_code == 200:
        print("Test summary:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to connect to packet generator. Status code: {response.status_code}")
