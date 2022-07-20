# storebox-rgb-led
My own rgb led notifications for storebox

## Autostart with systemd
Copy the contents of this project to `/usr/local/lib/storebox-rgb-led` and 
make sure that the `start.py` script has execute rights (`sudo chmod +x start.py`). 

Create the file `/etc/systemd/system/storebox-rgb-led.service` and copy the following content
into the file.

```
[Unit]
Description=Storebox RGB LED
 
[Service]
# Path to the Python entrypoint script
ExecStart=/usr/local/lib/storebox-rgb-led/start.py
# To make log messages appear, before the buffer is full
Environment=PYTHONUNBUFFERED=1
# Restart service, if it crashes
Restart=always
RestartSec=30
 
[Install]
# No dependent services; start whenever (default)
WantedBy=default.target
```

Enable the service, to make it start on system start: `sudo systemctl enable storebox-rgb-led.service`.

### Logs
Systemctl uses journald to write log messages. To view log messages for this service, type the command
`journalctl -e -f -u storebox-rgb-led.service`

## Google Calendar Cron Job
Open crontab config with `sudo nano /etc/crontab` and add the following line at the end
`50 10 * * mon,tue,wed,thu,fri   root    /usr/local/lib/storebox-rgb-led/gcal.py`# RGB_LED_Animations
