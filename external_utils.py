from enum import Enum
import os
from typing import MutableSequence, NamedTuple

# Constants
## Number of packets to send to AI for inference per potential action
PACKETS_PER_ACTION = 60
## Cooldown period after each action in seconds
COOLDOWN_PERIOD = 3
QUEUE_GET_TIMEOUT = 1

class ImuRelayState(Enum):
    WAITING_FOR_ACTION = 0
    SENDING_ACTION = 1
    COOLDOWN = 2

class ImuPacket(NamedTuple):
    playerID: int
    accel: MutableSequence[float]
    gyro: MutableSequence[float]
class AnklePacket(NamedTuple):
    playerID: int
    accel: MutableSequence[float]
    gyro: MutableSequence[float]
class GameStatePacket(NamedTuple):
    playerID: int
    playerHP: int
    shieldHP: int
    gunAmmo: int
class GunPacket(NamedTuple):
    playerID: int
    isFired: bool
class VestPacket(NamedTuple):
    playerID: int
    isHit: bool
class PlayerData(NamedTuple):
    playerID: int
    accel: float
    gyro: float
    isFired: bool
    isHit: bool

def dump_to_file(queue, data_type):
    filename = input(f"""Enter the filename to dump {data_type} to: """)
    target_file_path = f"""output/{filename}.dat"""
    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    with open(target_file_path, 'w') as output_file:
        while not queue.empty():
            output_file.write(str(queue.get()) + '\n')
    output_file.close()

def read_user_input(prompt):
    return input(prompt)

def write_packet_to(filepath, packet):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'a') as output_file:
        output_file.write(str(packet) + '\n')
    output_file.close()
