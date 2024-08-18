import os
from matplotlib.widgets import MultiCursor
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

CATALOG_NAME = "sliced"

FILE_PREFIX = "chod_p2_1"

# próba 2:
# schody 1 od prawej: 399 - 462
# schody 2 od prawej: 479 - 517
# chód 1 od prawej: 545-  579 6 kroków na nogę
# chód 2 od prawej:  599 - 662 8 kroków bardzo wolno
# chód 3: 683 - 703 po 6 kroków normalnie


# próba 1:
# początek wchodzenia: 579652-616400 (580-620)
# od prawej:642143-673000 (642-675)
# chód: 725000-750000 (727-750)
# chód 2: 770000-793000 

# read all files
df_acc = pd.read_csv(f"{CATALOG_NAME}/{FILE_PREFIX}.acc.csv")
df_gyro = pd.read_csv(f"{CATALOG_NAME}/{FILE_PREFIX}.gyro.csv")
df_press_temp = pd.read_csv(f"{CATALOG_NAME}/{FILE_PREFIX}.presstemp.csv")

# calculate avg temperature in Kelvin
avg_temp = df_press_temp["Temperature"].mean() + 273.15

# calculate h from pressure using formula h = -29.2718 * avg_temp * ln(pressure/pressure[0])
df_press_temp["Height"] = -29.2718 * avg_temp * np.log(df_press_temp["Pressure"]/df_press_temp["Pressure"].iloc[0])

# plot with cursor
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
axs[2].set_ylabel('ciśnienie\n[Pa]')
axs[2].ticklabel_format(useOffset=False)
axs[2].grid()

axs[3].plot(df_press_temp["Timestamp"], df_press_temp["Height"], linewidth=1.5)
axs[3].set_ylabel('wysokość\n[m]')
axs[3].ticklabel_format(useOffset=False)
axs[3].grid()

cursor = MultiCursor(fig.canvas, (axs[0], axs[1], axs[2], axs[3]), color='r', lw=1, horizOn=True, vertOn=True)

plt.show()
