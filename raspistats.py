#!/usr/bin/env python3

import paho.mqtt.publish as publish
import json
import os
from subprocess import check_output
from re import findall
from datetime import datetime

jsonData = {}

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return float(findall("\d+\.\d+",temp)[0])

def publish_message(topic, message):
    print("Publishing to MQTT topic: " + topic)
    print("Message: " + message)
    publish.single(topic, message, 0, False, hostname="nodered.local")

hostname = os.popen("hostname").read().strip()
loadavg = check_output(["cat","/proc/loadavg"]).decode("UTF-8").split()
ipaddr = check_output(["/sbin/ifconfig","eth0"]).decode("UTF-8").split()[5]
free = os.popen("free -w | grep Mem").read().split()

now = datetime.now()
date = now.strftime("%d.%m.%Y")
time = now.strftime("%H:%M:%S")

jsonData['cpu_temp'] = get_temp()
jsonData['load_1m'] = float(loadavg[0])
jsonData['load_5m'] = float(loadavg[1])
jsonData['load_15m'] = float(loadavg[2])
jsonData['eth0'] = ipaddr
jsonData['mem_total'] = int(free[1])
jsonData['mem_used'] = int(free[2])
jsonData['date_now'] = date
jsonData['time_now'] = time

publish_message("pi/" + hostname, json.dumps(jsonData))
