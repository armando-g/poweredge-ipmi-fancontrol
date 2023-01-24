import psutil
import time
import subprocess
import sys

# Define minimum and maximum temperatures and fan speeds.
min_temp = 30
max_temp = 75
min_speed = 10
max_speed = 75

# Minimum temperature change before updating fan speed
temp_delta = 5

# Change how often you want this script to loop in seconds
sleep_time = 1

# You don't need to set these
prev_temp = 0
prev_speed = 0

def get_cpu_temp():
    temp = psutil.sensors_temperatures()
    core_temps = [temp['coretemp'][i].current for i in range(len(temp['coretemp']))]
    avg_temp = sum(core_temps) / len(core_temps)
    return avg_temp

def calculate_fan_speed(temp):
    delta = abs(temp - prev_temp)
    if delta < temp_delta:
        return prev_speed
    else:
        if temp < min_temp:
            return min_speed
        if temp > max_temp:
            return max_speed
        temp_range = max_temp - min_temp
        speed_range = max_speed - min_speed
        temp_percentage = (temp - min_temp) / temp_range
        fan_speed = min_speed + (temp_percentage * speed_range)
        return fan_speed

while True:
    avg_temp = get_cpu_temp()
    fan_speed = calculate_fan_speed(avg_temp)

    if fan_speed != prev_speed:
        prev_temp = avg_temp
        prev_speed = fan_speed
        print(f"Average temperature: {format(avg_temp, '.0f')}°C, setting fans to {format(fan_speed, '.0f')}%")
        sys.stdout.flush()

        command = f"ipmitool raw 0x30 0x30 0x02 0xff {hex(int(fan_speed*2.56))}"
        subprocess.run(command, shell=True)
    time.sleep(sleep_time)
