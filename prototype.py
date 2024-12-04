import random

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

# Main function
def main():
    print("Welcome to the HTTP Request Packet Generator!")
    
    # Step 1: User inputs the number of packets to generate for each HTTP method
    num_packets = int(input("Enter the number of packets to generate for each HTTP method: "))
    
    # Step 2: User inputs the additional number of packets for focused testing
    focus_depth = int(input("Enter the number of additional packets for focused testing: "))
    
    # To record test results
    results = {method: {"passed": 0, "failed": 0} for method in HTTP_METHODS}
    failed_packets = {method: [] for method in HTTP_METHODS}  # To store failed packets
    
    # Step 3: Iterate over each HTTP method and generate packets
    for method in HTTP_METHODS:
        print(f"\nGenerating {method} packets...")
        for i in range(num_packets):
            packet = generate_http_request(method)
            print(f"\nGenerated {method} Packet {i + 1}:\n{packet}\n")
            
            # Step 4: Wait for user input to determine the test result
            test_result = input(f"Enter the test result for {method} Packet (0 for passed, 1 for failed): ").strip()
            if test_result == "0":
                print(f"{method} Packet passed. Continuing to the next packet.\n")
                results[method]["passed"] += 1
                continue
            elif test_result == "1":
                print(f"{method} Packet failed. Starting focused testing...")
                results[method]["failed"] += 1
                failed_packets[method].append(packet)  # Save the failed packet
                for j in range(focus_depth):
                    focused_packet = generate_http_request(method)
                    print(f"\nGenerated Focused {method} Packet {j + 1}:\n{focused_packet}\n")
                    # Focused test packets also require user input
                    focused_result = input(f"Enter the test result for Focused {method} Packet (0 for passed, 1 for failed): ").strip()
                    if focused_result == "0":
                        results[method]["passed"] += 1
                    elif focused_result == "1":
                        results[method]["failed"] += 1
                        failed_packets[method].append(focused_packet)  # Save the failed packet
                break
            else:
                print("Invalid input. Please enter 0 or 1.")

    # Print the test summary
    print("\nTest completed! Here is the test summary:")
    for method, result in results.items():
        print(f"- {method}: {result['passed']} passed, {result['failed']} failed")
    
    # Save the test summary to a log file
    save_to_log_file(results, failed_packets)
    print("\nExiting the program.")

if __name__ == "__main__":
    main()
