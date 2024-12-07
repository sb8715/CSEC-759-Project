## Prerequisites

- Python 3.10.11 or above
- Available port 5000 (or modify the script to use a different port)
- Required Python libraries:
  - `requests`: Install using:
    ```sh
    pip install requests
    ```
  - `Flask`: Install using:
    ```sh
    pip install Flask
    ```

## Running the Project

1. Run the HTTP Packet Generator:

   ```sh
   python3 HTTP Packet Generator.py
   ```
2. Then, run the Fake Fuzzer:
   ```sh
   python3 Fake Fuzzer.py
   ```
## Dataset and Evaluation
As mentioned in our previous presentation, the original project, Nyx-Net, has not been updated in over three years. 

https://github.com/RUB-SysSec/nyx-net

Due to various reasons, this Nyxnet is currently unable to compile and run successfully. Despite our attempts to use different runtime environments and versions, we could not make it operational. If you figure out a way to make it work please please please let us know! Thank you
This limitation prompted us to create a standalone program from scratch rather than modifying the existing Nyx-Net codebase. Consequently, we are currently unable to utilize any datasets for effective evaluation of our project. 
