# Source code structure
## `beetle.py`: 
- Contains base Beetle class and individual classes that extend Beetle to provide gun, glove and vest functionality
- NOTE: Update the `Beetle.is_debug_printing` variable depending on whether you want to see additional information from the transmission protocol
    - `is_debug_printing = True` causes every Beetle class, to print the hex values of every packet received from the actual Beetle. This helps with debugging transmission or data loss issues

## `ble_delegate.py`: 
- Contains bluepy Delegate used to receive data from Beetle

## `external_main.py`: 
- Runs both internal and external code to transmit and receive data from all the Beetles involved
- This is the code to run and start all the comms protocols running

## `external_utils.py`: 
- Provides helper functions, constants, structs needed for external comms logic

## `imu_data_collector.py`: 
- Basic code to collect IMU data from a specified Beetle and write collected data to a csv file
- Update the `IMU_BEETLE` variable inside it to your Beetle's Bluetooth MAC address using the `BEETLE_MAC_ADDR` Enum imported from internal_utils.py

## `imu_dual_collector.py`: 
- Basic code to collect IMU data from 2 IMU Beetles at once and write collected data to a csv file
- NOTE: Wait for the yellow-coloured message `Synced both queues` to be printed to terminal screen before starting your actions
- Update the `GLOVE_IMU_BEETLE` and `GLOVE2_IMU_BEETLE` variables inside it to your Beetles' respective Bluetooth MAC addresses using the `BEETLE_MAC_ADDR` Enum imported from internal_utils.py

## `internal_main.py`: 
- Main thread for the internal comms protocol
- `external_main.py` automatically initialises the main thread and runs it to connect to all Beetles involved

## `internal_utils.py`: 
- Provides helper functions, constants, structs needed for internal comms logic

## `relay_client.py`: 
- Relay client that connects to relay server(running on the Ultra96) to send raw data from Beetle to the server and update the Beetles involved with the latest game state
- NOTE: Update the `IS_DEBUG_PRINTING` constant depending on whether you want to see additional information on the communication with the relay server code
    - `IS_DEBUG_PRINTING = True` causes relay_client to print every message sent/received from the server, including packets that were forwarded from internal communications to the relay server

## `internal_tests`:
- Component test code for testing Bluetooth(any Beetle), gun Beetle, or vest Beetle

# Quick start
- Run `python3 external_main.py` without any arguments to start all the necessary threads and run the comms protocols
- To end transmission and quit, press `CTRL+C` and wait for all threads to terminate

# List of libraries required
- `anycrc`
- `bluepy`
- `pandas`: For `internal_tests/imu_data_visualiser.py`
- `NumPy`: For `internal_tests/imu_data_visualiser.py`
