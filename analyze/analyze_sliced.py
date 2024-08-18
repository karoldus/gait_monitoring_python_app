import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

CATALOG_NAME = "sliced"

#list of all files
all_files = os.listdir(CATALOG_NAME)

# divide files into groups by their name
exercises = {}

for file in all_files:
    # file name has format name_sth.acc.csv, name_sth.gyro.csv, name_sth.presstemp.csv
    name = file.split(".")[0]
    if name not in exercises:
        exercises[name] = {}

    if "acc" in file:
        exercises[name]["acc"] = file
    elif "gyro" in file:
        exercises[name]["gyro"] = file
    elif "presstemp" in file:
        exercises[name]["presstemp"] = file


for exercise_name in exercises:
    print(exercise_name)
    # read all files
    df_acc = pd.read_csv(f"{CATALOG_NAME}/{exercises[exercise_name]['acc']}")
    df_gyro = pd.read_csv(f"{CATALOG_NAME}/{exercises[exercise_name]['gyro']}")
    df_press_temp = pd.read_csv(f"{CATALOG_NAME}/{exercises[exercise_name]['presstemp']}")

    # calculate avg temperature in Kelvin
    avg_temp = df_press_temp["Temperature"].mean() + 273.15

    # calculate h from pressure using formula h = -29.2718 * avg_temp * ln(pressure/pressure[0])
    df_press_temp["Height"] = -29.2718 * avg_temp * np.log(df_press_temp["Pressure"]/df_press_temp["Pressure"].iloc[0])

    # plot
    fig, axs = plt.subplots(4, 1, sharex=True)

    axs[0].plot(df_acc["Timestamp"], df_acc["AccX"], label="x", linewidth=0.9)
    axs[0].plot(df_acc["Timestamp"], df_acc["AccY"], label="y", linewidth=0.9)
    axs[0].plot(df_acc["Timestamp"], df_acc["AccZ"], label="z", linewidth=0.9)
    axs[0].set_ylabel("przyspieszenie\n[m/s^2]")
    axs[0].legend()
    axs[0].locator_params(axis = 'y', nbins = 6)
    axs[0].grid()

    axs[1].plot(df_gyro["Timestamp"], df_gyro["GyroX"], label="x", linewidth=0.9)
    axs[1].plot(df_gyro["Timestamp"], df_gyro["GyroY"], label="y", linewidth=0.9)
    axs[1].plot(df_gyro["Timestamp"], df_gyro["GyroZ"], label="z", linewidth=0.9)
    axs[1].set_ylabel('prędkość\nkątowa\n[rad/s]')
    axs[1].legend()
    axs[1].locator_params(axis = 'y', nbins = 6)
    axs[1].grid()

    axs[2].plot(df_press_temp["Timestamp"], df_press_temp["Pressure"], linewidth=1.5)
    axs[2].set_ylabel('ciśnienie [hPa]')
    axs[2].ticklabel_format(useOffset=False)
    axs[2].locator_params(axis = 'y', nbins = 6)
    axs[2].grid()

    axs[3].plot(df_press_temp["Timestamp"], df_press_temp["Height"], linewidth=1.5)
    axs[3].set_ylabel('wysokość [m]')
    axs[2].ticklabel_format(useOffset=False)
    axs[3].locator_params(axis = 'y', nbins = 6)
    axs[3].grid()

    plt.gcf().set_size_inches(8, 7)
    plt.xlabel('czas [ms]')
    # plt.show()
    plt.savefig(f"{CATALOG_NAME}/{exercise_name}.png")