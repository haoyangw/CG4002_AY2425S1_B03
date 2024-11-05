from typing import MutableSequence
from enum import Enum
from typing import NamedTuple

# Constants
BAUDRATE = 115200
INITIAL_SEQ_NUM = 0
ERROR_VALUE = -1
BLE_TIMEOUT = 0.115
## Timeout value below should match the delay() value for sending packets on the Beetle
BLE_WAIT_TIMEOUT = 0.01
PACKET_SIZE = 20
PACKET_DATA_SIZE = 16
PACKET_TYPE_ID_LENGTH = 4
PACKET_FORMAT = "=BH16sB"
BITS_PER_BYTE = 8
LOWER_4BITS_MASK = 0x0f
IMU_DIMENSION = 3
MAX_SEQ_NUM = 65535
MAX_RETRANSMITS = 5
ACC_LSB_SCALE = 16384.0
GYRO_LSB_SCALE = 131.0
GAME_STATE_QUEUE_TIMEOUT = 1

BLUNO_MAC_ADDR_LIST = [
    "f4:b8:5e:42:67:2b",
    "F4:B8:5E:42:6D:75",
    "F4:B8:5E:42:67:6E",
    # Glove
    "F4:B8:5E:42:61:62",
    # Gun
    "D0:39:72:DF:CA:F2",
    # Vest
    "F4:B8:5E:42:6D:0E",
    # Extra 1
    "B4:99:4C:89:1B:FD",
    # Extra 2
    "B4:99:4C:89:18:1D"
]

BEETLE_MAC_ADDR_MAP = {
    # Below must be player 1 IMU(glove) Beetle
    "F4:B8:5E:42:61:62": 1,
    # Below must be player 1 IMU(ankle) Beetle
    "D0:39:72:DF:CA:F2": 1,
    # Below must be player 1 gun Beetle
    "B4:99:4C:89:18:72": 1,
    # Below must be player 1 vest Beetle
    "F4:B8:5E:42:6D:0E": 1,

    # Below must be player 2 IMU(glove) Beetle
    "B4:99:4C:89:1B:FD": 2,
    # Below must be player 2 IMU(ankle) Beetle
    "34:08:E1:2A:08:61": 2,
    # Below must be player 2 gun Beetle
    "F4:B8:5E:42:67:2B": 2,
    # Below must be player 2 vest Beetle
    "F4:B8:5E:42:6D:75": 2,

    # Extra 1
    "F4:B8:5E:42:67:6E": 1,
    # Extra 2
#    "B4:99:4C:89:18:1D": 2,
}

## Bluno Beetle BLE GATT UUIDs
GATT_SERIAL_SERVICE_UUID = "0000dfb0-0000-1000-8000-00805f9b34fb"
GATT_SERIAL_CHARACTERISTIC_UUID = "0000dfb1-0000-1000-8000-00805f9b34fb"
GATT_MODEL_NUMBER_CHARACTERISTIC_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
GATT_COMMAND_CHARACTERISTIC_UUID = "0000dfb2-0000-1000-8000-00805f9b34fb"

## Bluno Beetle BLE GATT Handles
GATT_COMMAND_CHARACTERISTIC_HANDLE = 40
GATT_MODEL_NUMBER_CHARACTERISTIC_HANDLE = 20
GATT_SERIAL_CHARACTERISTIC_HANDLE = 37

## Bluno Beetle GATT setup
BLUNO_GATT_PASSWORD = "AT+PASSWOR=DFRobot\r\n"
BAUDRATE_SETUP = "AT+CURRUART={}\r\n".format(BAUDRATE)

class bcolors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class BlePacket(NamedTuple):
    metadata: int
    seq_num: int
    data: bytearray
    crc: int

# Packet Type ID
class BlePacketType(Enum):
    HELLO = 0
    ACK = 1
    NACK = 2
    IMU = 3
    IR_RECV = 4
    IR_TRANS = 5
    GAME_STAT = 6
    GAME_ACTION = 7
    INFO = 8

class HandshakeStatus(Enum):
    # Laptop has not sent HELLO packet, will send HELLO
    HELLO = 0
    # Laptop has sent HELLO packet, waiting for ACK from Beetle
    ACK = 1 
    # Laptop received ACK from Beetle, will send SYN+ACK packet to Beetle
    SYN = 2
    # Handshake complete
    COMPLETE = 3

class GunPacket(NamedTuple):
    beetle_mac: str
    gunBoolean: bool

class ImuPacket(NamedTuple):
    beetle_mac: str
    accel: MutableSequence[float]
    gyro: MutableSequence[float]

class VestPacket(NamedTuple):
    beetle_mac: str
    vestBoolean: bool

class GunUpdatePacket(NamedTuple):
    player_id: int
    bullets: int

class VestUpdatePacket(NamedTuple):
    player_id: int
    is_hit: bool
    player_hp: int

# Public functions
def get_player_id_for(beetle_mac_addr):
    return BEETLE_MAC_ADDR_MAP[beetle_mac_addr]

def is_metadata_byte(given_byte):
    packet_type = metadata_to_packet_type(given_byte)
    return packet_type <= BlePacketType.INFO.value and packet_type >= BlePacketType.HELLO.value

def metadata_to_packet_type(metadata):
    return metadata & LOWER_4BITS_MASK
