import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# TIME = "2024-08-17_18_53_20"
TIME = "2024-08-17_19_46_27"

PRESS_TEMP_FILE_NAME = f"press_temp_data_{TIME}.csv"
ACC_FILE_NAME = f"acc_data_{TIME}.csv"
GYRO_FILE_NAME = f"gyro_data_{TIME}.csv"


def slice_data(acc_df, gyro_df, press_temp_df, start_time, end_time, filename):
    new_acc_df = acc_df[(acc_df["Timestamp"] >= start_time) & (acc_df["Timestamp"] <= end_time)]
    new_gyro_df = gyro_df[(gyro_df["Timestamp"] >= start_time) & (gyro_df["Timestamp"] <= end_time)]
    new_press_temp_df = press_temp_df[(press_temp_df["Timestamp"] >= start_time) & (press_temp_df["Timestamp"] <= end_time)]

    # timestamp relative to start_time
    new_acc_df["Timestamp"] = new_acc_df["Timestamp"] - start_time
    new_gyro_df["Timestamp"] = new_gyro_df["Timestamp"] - start_time
    new_press_temp_df["Timestamp"] = new_press_temp_df["Timestamp"] - start_time

    new_acc_df.to_csv(f"sliced/{filename}.acc.csv", index=False)
    new_gyro_df.to_csv(f"sliced/{filename}.gyro.csv", index=False)
    new_press_temp_df.to_csv(f"sliced/{filename}.presstemp.csv", index=False)


df_acc = pd.read_csv(ACC_FILE_NAME)
df_gyro = pd.read_csv(GYRO_FILE_NAME)
df_press_temp = pd.read_csv(PRESS_TEMP_FILE_NAME)

# sort by timestamp
df_acc = df_acc.sort_values(by="Timestamp")
df_gyro = df_gyro.sort_values(by="Timestamp")
df_press_temp = df_press_temp.sort_values(by="Timestamp")

# calculate avg, min, max temperature
avg_temp = df_press_temp["Temperature"].mean()
min_temp = df_press_temp["Temperature"].min()
max_temp = df_press_temp["Temperature"].max()

print(f"Average temperature: {avg_temp} *C, min temperature: {min_temp} *C, max temperature: {max_temp} *C")

# make avg_temp in Kelvin
avg_temp += 273.15

# smooth pressure data
# smooth_press = df_press_temp["Pressure"].to_frame()
df_press_temp["Pressure"] = df_press_temp["Pressure"].ewm(span=3).mean()

# slice_data(df_acc, df_gyro, df_press_temp, 399000, 462000, "schody_p2_1")
# slice_data(df_acc, df_gyro, df_press_temp, 479000, 517000, "schody_p2_2")
# slice_data(df_acc, df_gyro, df_press_temp, 545000, 579000, "chod_p2_1")
# slice_data(df_acc, df_gyro, df_press_temp, 599000, 662000, "chod_p2_2")
# slice_data(df_acc, df_gyro, df_press_temp, 683000, 703000, "chod_p2_3")

# slice_data(df_acc, df_gyro, df_press_temp, 580000, 620000, "schody_p1_1")
# slice_data(df_acc, df_gyro, df_press_temp, 642000, 675000, "schody_p1_2")
# slice_data(df_acc, df_gyro, df_press_temp, 727000, 750000, "chod_p1_1")
# slice_data(df_acc, df_gyro, df_press_temp, 770000, 793000, "chod_p1_2")

# calculate h from pressure using formula h = -29.2718 * avg_temp * ln(pressure/pressure[0])
df_press_temp["Height"] = -29.2718 * avg_temp * np.log(df_press_temp["Pressure"]/df_press_temp["Pressure"].iloc[0])

# make 4 subplots: acc, gyro, press, height of type plot
fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

axs[0].plot(df_acc["Timestamp"], df_acc["AccX"], label="AccX", linewidth=0.5)
axs[0].plot(df_acc["Timestamp"], df_acc["AccY"], label="AccY")
axs[0].plot(df_acc["Timestamp"], df_acc["AccZ"], label="AccZ")
axs[0].set_title("Accelerometer data")
axs[0].set_xlabel("Timestamp")
axs[0].set_ylabel("Acceleration")
axs[0].legend()

axs[1].plot(df_gyro["Timestamp"], df_gyro["GyroX"], label="GyroX")
axs[1].plot(df_gyro["Timestamp"], df_gyro["GyroY"], label="GyroY")
axs[1].plot(df_gyro["Timestamp"], df_gyro["GyroZ"], label="GyroZ")
axs[1].set_title("Gyroscope data")
axs[1].set_xlabel("Timestamp")
axs[1].set_ylabel("Angular velocity")
axs[1].legend()

axs[2].plot(df_press_temp["Timestamp"], df_press_temp["Pressure"], label="Pressure")
axs[2].set_title("Pressure data")
axs[2].set_xlabel("Timestamp")
axs[2].set_ylabel("Pressure")
axs[2].legend()

axs[3].plot(df_press_temp["Timestamp"], df_press_temp["Height"], label="Height")
axs[3].set_title("Height data")
axs[3].set_xlabel("Timestamp")
axs[3].set_ylabel("Height")
axs[3].legend()



# axs[0].scatter(df_acc["Timestamp"], df_acc["AccX"], label="AccX")
# axs[0].scatter(df_acc["Timestamp"], df_acc["AccY"], label="AccY")
# axs[0].scatter(df_acc["Timestamp"], df_acc["AccZ"], label="AccZ")
# axs[0].set_title("Accelerometer data")
# axs[0].set_xlabel("Timestamp")
# axs[0].set_ylabel("Acceleration")
# axs[0].legend()

# axs[1].scatter(df_gyro["Timestamp"], df_gyro["GyroX"], label="GyroX")
# axs[1].scatter(df_gyro["Timestamp"], df_gyro["GyroY"], label="GyroY")
# axs[1].scatter(df_gyro["Timestamp"], df_gyro["GyroZ"], label="GyroZ")
# axs[1].set_title("Gyroscope data")
# axs[1].set_xlabel("Timestamp")
# axs[1].set_ylabel("Angular velocity")
# axs[1].legend()

# axs[2].scatter(df_press_temp["Timestamp"], df_press_temp["Pressure"], label="Pressure")
# axs[2].set_title("Pressure data")
# axs[2].set_xlabel("Timestamp")
# axs[2].set_ylabel("Pressure")
# axs[2].legend()

plt.tight_layout()
plt.show()


