from enum import Enum
from typing import NamedTuple

# Constants
INITIAL_SEQ_NUM = 0
ERROR_VALUE = -1
BLE_TIMEOUT = 0.25
PACKET_SIZE = 20
PACKET_DATA_SIZE = 16
PACKET_TYPE_ID_LENGTH = 4
PACKET_FORMAT = "=BH16sB"
BITS_PER_BYTE = 8
LOWER_4BITS_MASK = 0x0f
MAX_SEQ_NUM = 65535

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

## BLE GATT
GATT_SERIAL_SERVICE_UUID = "0000dfb0-0000-1000-8000-00805f9b34fb"
GATT_SERIAL_CHARACTERISTIC_UUID = "0000dfb1-0000-1000-8000-00805f9b34fb"

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
    P1_IMU = 3
    P1_IR_RECV = 4
    P1_IR_TRANS = 5
    P2_IMU = 6
    P2_IR_RECV = 7
    P2_IR_TRANS = 8
    GAME_STAT = 9

# Public functions
def is_metadata_byte(given_byte):
    packet_type = metadata_to_packet_type(given_byte)
    return packet_type <= BlePacketType.GAME_STAT.value and packet_type >= BlePacketType.HELLO.value

def metadata_to_packet_type(metadata):
    return metadata & LOWER_4BITS_MASK
