"""
Main app for communication using NUS service

"""

import asyncio
import sys
from itertools import count, takewhile
from typing import Iterator

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from msg_processing import process_press_temp_data

DEVICE_NAME = "gait_001"

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

BLE_MSG_HEADER_SIZE = 13

MSG_TYPES = {
    0x00: "ACC_DATA",
    0x01: "GYRO_DATA",
    0x02: "PRESS_TEMP_DATA"
}

last_msg = { # made iit class
    "type": None,
    "current_part": None,
    "total_parts": None,
    "timestamp": None,
    "data_len": None,
    "data": None,
    "ended": True
}

def end_saved_msg():
    print("Processing message type: ", MSG_TYPES[last_msg["type"]], ", timestamp: ", last_msg["timestamp"], ", data_len: ", last_msg["data_len"])
    # print("Data: ", last_msg["data"])
    last_msg["ended"] = True

    if last_msg["type"] == 0x00:
        print("ACC_DATA")
        #TODO: process accelerometer data
    elif last_msg["type"] == 0x01:
        print("GYRO_DATA")
        #TODO process gyroscope data
    elif last_msg["type"] == 0x02:
        print("PRESS_TEMP_DATA")
        process_press_temp_data(last_msg)


def process_data(data: bytes):
    """
    Process the received data from the device. This is where you should put
    your application logic.
    """
    # print("received:", data)

    if len(data) < BLE_MSG_HEADER_SIZE:
        print("Invalid message size")
        return
    
    msg_type = data[0]
    current_part = data[1]
    total_parts = data[2]
    timestamp = int.from_bytes(data[3:11], byteorder='little')
    data_len = int.from_bytes(data[11:13], byteorder='little')

    if msg_type not in MSG_TYPES:
        print("Invalid message type: ", msg_type)
        return
    
    print("Received message type: ", MSG_TYPES[msg_type], " part ", current_part, " of ", total_parts, ", timestamp: ", timestamp, ", data_len: ", data_len)

    if len(data) != BLE_MSG_HEADER_SIZE + data_len:
        print("Invalid message size: ", len(data) + " expected: ", BLE_MSG_HEADER_SIZE + data_len)
        return
    
    if last_msg["ended"]:
        last_msg["type"] = msg_type
        last_msg["current_part"] = current_part
        last_msg["total_parts"] = total_parts
        last_msg["timestamp"] = timestamp
        last_msg["data_len"] = data_len
        last_msg["data"] = data[BLE_MSG_HEADER_SIZE:]
        last_msg["ended"] = False
    else:
        if last_msg["type"] != msg_type or last_msg["current_part"] + 1 != current_part or last_msg["total_parts"] != total_parts or last_msg["timestamp"] != timestamp:
            print("Invalid message. Expected: ", last_msg["type"], " part ", last_msg["current_part"] + 1, " of ", last_msg["total_parts"], ", timestamp: ", last_msg["timestamp"])
            print("Discarding old message and starting new one")
            last_msg["type"] = msg_type
            last_msg["current_part"] = current_part
            last_msg["total_parts"] = total_parts
            last_msg["timestamp"] = timestamp
            last_msg["data_len"] = data_len
            last_msg["data"] = data[BLE_MSG_HEADER_SIZE:]
            last_msg["ended"] = False
        else:
            last_msg["data"] += data[BLE_MSG_HEADER_SIZE:]
            last_msg["current_part"] = current_part
            last_msg["data_len"] += data_len

    if last_msg["current_part"] == last_msg["total_parts"]:
        print("All parts received")
        end_saved_msg()


# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))


async def uart_terminal():
    """This is a simple "terminal" program that uses the Nordic Semiconductor
    (nRF) UART service. It reads from stdin and sends each line of data to the
    remote device. Any data received from the device is printed to stdout.
    """

    # device = await BleakScanner.find_device_by_filter(match_nus_uuid)
    device = await BleakScanner.find_device_by_name(DEVICE_NAME)

    if device is None:
        print("no matching device found")
        sys.exit(1)

    def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
        # print("received:", data)
        process_data(data)

    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        await client.start_notify(UART_TX_CHAR_UUID.lower(), handle_rx)

        print("Connected, start typing and press ENTER...")

        loop = asyncio.get_running_loop()
        nus = client.services.get_service(UART_SERVICE_UUID.lower())
        rx_char = nus.get_characteristic(UART_RX_CHAR_UUID.lower())

        while True:
            # This waits until you type a line and press ENTER.
            # A real terminal program might put stdin in raw mode so that things
            # like CTRL+C get passed to the remote device.
            data = await loop.run_in_executor(None, sys.stdin.buffer.readline)

            # data will be empty on EOF (e.g. CTRL+D on *nix)
            if not data:
                break

            # some devices, like devices running MicroPython, expect Windows
            # line endings (uncomment line below if needed)
            # data = data.replace(b"\n", b"\r\n")

            # Writing without response requires that the data can fit in a
            # single BLE packet. We can use the max_write_without_response_size
            # property to split the data into chunks that will fit.

            for s in sliced(data, rx_char.max_write_without_response_size):
                await client.write_gatt_char(rx_char, s, response=False)

            print("sent:", data)


if __name__ == "__main__":
    try:
        asyncio.run(uart_terminal())
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass