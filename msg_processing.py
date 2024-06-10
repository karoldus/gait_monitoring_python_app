'''

'''

import os
import sys
import time

files_created = False

PRESS_TEMP_FILE_NAME = None
ACC_FILE_NAME = None
GYRO_FILE_NAME = None

CATALOG_NAME = "data"

TEMP_PRESS_FRAME_SIZE = 6
PRESS_VALUE_SIZE = 4
TEMP_VALUE_SIZE = 2

ACC_FRAME_SIZE = 6
ACC_VALUE_SIZE = 2

GYRO_FRAME_SIZE = 6
GYRO_VALUE_SIZE = 2

def create_files():
    global files_created
    global PRESS_TEMP_FILE_NAME
    global ACC_FILE_NAME
    global GYRO_FILE_NAME

    if files_created:
        return
    
    actual_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    PRESS_TEMP_FILE_NAME = f"press_temp_data_{actual_time}.csv"
    ACC_FILE_NAME = f"acc_data_{actual_time}.csv"
    GYRO_FILE_NAME = f"gyro_data_{actual_time}.csv"

    with open(CATALOG_NAME + "/" + PRESS_TEMP_FILE_NAME, "w") as f:
        f.write("Timestamp,Pressure,Temperature\n")

    with open(CATALOG_NAME + "/" + ACC_FILE_NAME, "w") as f:
        f.write("Timestamp,AccX,AccY,AccZ\n")

    with open(CATALOG_NAME + "/" + GYRO_FILE_NAME, "w") as f:
        f.write("Timestamp,GyroX,GyroY,GyroZ\n")

    files_created = True

def process_press_temp_data(msg: dict):
    create_files()

    if msg["type"] != 0x02:
        print("Invalid message type")
        return
    
    if msg["data_len"] % TEMP_PRESS_FRAME_SIZE != 0:
        print("Invalid data length - can not be divided by ", TEMP_PRESS_FRAME_SIZE)
        return
    
    number_of_frames = msg["data_len"] // TEMP_PRESS_FRAME_SIZE

    end_time = msg["timestamp"]
    start_time = end_time - msg["data_period_ms"] * (number_of_frames - 1)

    for i in range(number_of_frames):

        timestamp = start_time + i * msg["data_period_ms"]
        
        pressure = int.from_bytes(msg["data"][i * TEMP_PRESS_FRAME_SIZE:i * TEMP_PRESS_FRAME_SIZE + PRESS_VALUE_SIZE], byteorder='little')
        temperature = int.from_bytes(msg["data"][i * TEMP_PRESS_FRAME_SIZE + PRESS_VALUE_SIZE:i * TEMP_PRESS_FRAME_SIZE + TEMP_PRESS_FRAME_SIZE], byteorder='little')

        pressure = round(pressure / 100000.0, 5)
        temperature = round(temperature / 100.0 - 273.15, 2)

        with open(CATALOG_NAME + "/" + PRESS_TEMP_FILE_NAME, "a") as f:
            f.write(f"{timestamp},{pressure},{temperature}\n")
    
def process_acc_data(msg: dict):
    create_files()

    if msg["type"] != 0x00:
        print("Invalid message type")
        return
    
    if msg["data_len"] % ACC_FRAME_SIZE != 0:
        print("Invalid data length - can not be divided by ", ACC_FRAME_SIZE)
        return
    
    number_of_frames = msg["data_len"] // ACC_FRAME_SIZE

    end_time = msg["timestamp"]
    start_time = end_time - msg["data_period_ms"] * (number_of_frames - 1)

    for i in range(number_of_frames):
        timestamp = start_time + i * msg["data_period_ms"]
        acc_x = int.from_bytes(msg["data"][i * ACC_FRAME_SIZE:i * ACC_FRAME_SIZE + ACC_VALUE_SIZE], byteorder='little')
        acc_y = int.from_bytes(msg["data"][i * ACC_FRAME_SIZE + ACC_VALUE_SIZE:i * ACC_FRAME_SIZE + 2 * ACC_VALUE_SIZE], byteorder='little')
        acc_z = int.from_bytes(msg["data"][i * ACC_FRAME_SIZE + 2 * ACC_VALUE_SIZE:i * ACC_FRAME_SIZE + ACC_FRAME_SIZE], byteorder='little')

        acc_x = round((acc_x - 32768) / 1000.0, 3)
        acc_y = round((acc_y - 32768) / 1000.0, 3)
        acc_z = round((acc_z - 32768) / 1000.0, 3)

        with open(CATALOG_NAME + "/" + ACC_FILE_NAME, "a") as f:
            f.write(f"{timestamp},{acc_x},{acc_y},{acc_z}\n")

def process_gyro_data(msg: dict):
    create_files()

    if msg["type"] != 0x01:
        print("Invalid message type")
        return
    
    if msg["data_len"] % GYRO_FRAME_SIZE != 0:
        print("Invalid data length - can not be divided by ", GYRO_FRAME_SIZE)
        return
    
    number_of_frames = msg["data_len"] // GYRO_FRAME_SIZE

    end_time = msg["timestamp"]
    start_time = end_time - msg["data_period_ms"] * (number_of_frames - 1)

    for i in range(number_of_frames):
        timestamp = start_time + i * msg["data_period_ms"]
        gyro_x = int.from_bytes(msg["data"][i * GYRO_FRAME_SIZE:i * GYRO_FRAME_SIZE + GYRO_VALUE_SIZE], byteorder='little')
        gyro_y = int.from_bytes(msg["data"][i * GYRO_FRAME_SIZE + GYRO_VALUE_SIZE:i * GYRO_FRAME_SIZE + 2 * GYRO_VALUE_SIZE], byteorder='little')
        gyro_z = int.from_bytes(msg["data"][i * GYRO_FRAME_SIZE + 2 * GYRO_VALUE_SIZE:i * GYRO_FRAME_SIZE + GYRO_FRAME_SIZE], byteorder='little')

        gyro_x = round((gyro_x - 32768) / 1000.0, 3)
        gyro_y = round((gyro_y - 32768) / 1000.0, 3)
        gyro_z = round((gyro_z - 32768) / 1000.0, 3)

        with open(CATALOG_NAME + "/" + GYRO_FILE_NAME, "a") as f:
            f.write(f"{timestamp},{gyro_x},{gyro_y},{gyro_z}\n")
    
    




