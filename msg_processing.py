'''

'''

import os
import sys
import time

files_created = False

PRESS_TEMP_FINE_NAME = None

CATALOG_NAME = "data"

TEMP_PRESS_FRAME_SIZE = 6
PRESS_VALUE_SIZE = 4
TEMP_VALUE_SIZE = 2

def create_files():
    global files_created
    global PRESS_TEMP_FINE_NAME

    if files_created:
        return
    
    actual_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    PRESS_TEMP_FINE_NAME = f"press_temp_data_{actual_time}.csv"

    with open(CATALOG_NAME + "/" + PRESS_TEMP_FINE_NAME, "w") as f:
        f.write("Timestamp,Pressure,Temperature\n")

    files_created = True

def process_press_temp_data(msg: dict):
    create_files()

    if msg["type"] != 0x02:
        print("Invalid message type")
        return
    
    if msg["data_len"] % TEMP_PRESS_FRAME_SIZE != 0:
        print("Invalid data length - can not be divided by ", TEMP_PRESS_FRAME_SIZE)
        return
    
    numer_of_frames = msg["data_len"] // TEMP_PRESS_FRAME_SIZE

    for i in range(numer_of_frames):
        timestamp = msg["timestamp"]
        pressure = int.from_bytes(msg["data"][i * TEMP_PRESS_FRAME_SIZE:i * TEMP_PRESS_FRAME_SIZE + PRESS_VALUE_SIZE], byteorder='little')
        temperature = int.from_bytes(msg["data"][i * TEMP_PRESS_FRAME_SIZE + PRESS_VALUE_SIZE:i * TEMP_PRESS_FRAME_SIZE + TEMP_PRESS_FRAME_SIZE], byteorder='little')

        pressure = round(pressure / 100000.0, 5)
        temperature = round(temperature / 100.0 - 273.15, 2)

        with open(CATALOG_NAME + "/" + PRESS_TEMP_FINE_NAME, "a") as f:
            f.write(f"{timestamp},{pressure},{temperature}\n")
    
    
    




