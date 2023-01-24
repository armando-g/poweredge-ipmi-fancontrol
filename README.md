# PowerEdge IPMI Fan Control

This script uses the `psutil` and `subprocess` libraries to continuously monitor the CPU temperature and adjust the fan speed through the IPMI interface. The script runs a loop that checks the average temperature of all CPU cores and calculates the appropriate fan speed using a linear equation based on pre-defined minimum and maximum temperature and fan speed values. The script also includes a way to set a minimum change in temperature before the fan speed is updated in order to limit unnecessary fan fluctuations. By default, a change of at least 5 degrees is required.

## Prerequisites
* Python 3
* `psutil` library
* `ipmitool` installed on your system and functioning with the command `ipmitool raw 0x30 0x30 0x02 0xff <0x01-0x64>`
## Installation
1. Clone or download the script to your system.
2. Make sure that the `ipmitool` is installed and functioning with the command `ipmitool raw 0x30 0x30 0x02 0xff <0x01-0x64>`
3. Install the `psutil` library by running `pip3 install psutil`
4. Edit the script and update the variables to match your desired values.
5. You can run the script by executing `python3 poweredge-ipmi-fancontrol.py`
## Running as a systemd service
You can run the script as a systemd service by following these steps:

1. Create a new service file in the `/etc/systemd/system` directory. You can name it `poweredge-ipmi-fancontrol.service` for example.
2. Open the file with a text editor and add the following content:

```
[Unit]
Description=PowerEdge IPMI Fan Control Service

[Service]
ExecStart=/usr/bin/python3 /path/to/your/script.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target`
```
3. Replace `/path/to/your/script.py` with the actual path to your script.
4. Save and close the file.
5. Run the following command to reload the systemd daemon and enable the service to start at boot:

```
sudo systemctl daemon-reload
sudo systemctl enable poweredge-ipmi-fancontrol.service
```
6. You can start the service by running the following command:
```
sudo systemctl start poweredge-ipmi-fancontrol.service
```
7. To check the status of the service, use the following command:
```
sudo systemctl status poweredge-ipmi-fancontrol.service
```
8. To stop the service, use the following command:
```
sudo systemctl stop poweredge-ipmi-fancontrol.service
```
You can also use `sudo systemctl restart poweredge-ipmi-fancontrol.service` to restart the service and s`udo systemctl disable ipmi-fancontrol.service` to disable it.

Please make sure that the user running the service has the permissions to execute the command and read the temperature data.
