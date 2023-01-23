import psutil
import time
import os
import sys

min_temp = 35
max_temp = 70

min_speed = 10
max_speed = 80

prev_speed = 0

def get_cpu_temp():
    temp = psutil.sensors_temperatures()
    core_temps = [temp['coretemp'][i].current for i in range(len(temp['coretemp']))]
    avg_temp = sum(core_temps) / len(core_temps)
    return avg_temp

def calculate_fan_speed(temp, min_temp, max_temp, min_speed, max_speed, prev_speed):
    if temp < min_temp:
        return min_speed
    if temp > max_temp:
        return max_speed
    temp_range = max_temp - min_temp
    speed_range = max_speed - min_speed
    temp_percentage = (temp - min_temp) / temp_range
    fan_speed = min_speed + (temp_percentage * speed_range)
    delta = abs(fan_speed - prev_speed)
    if delta < 5:
        return prev_speed
    else:
        return fan_speed

while True:
    avg_temp = get_cpu_temp()
    fan_speed = calculate_fan_speed(avg_temp, min_temp, max_temp, min_speed, max_speed, prev_speed)
    if fan_speed != prev_speed:
        prev_speed = fan_speed
        print(f"Requesting fans run @ {format(fan_speed, '.0f')}%")
        sys.stdout.flush()
        os.system(f"ipmitool raw 0x30 0x30 0x02 0xff {hex(int(fan_speed*2.56))}")
    else:
         print("Fan speeds unchanged.")
         sys.stdout.flush()
    time.sleep(1)
