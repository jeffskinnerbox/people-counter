#!/bin/bash
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.4.1
#
# Purpose: Display the ARM CPU and GPU temperature of Raspberry Pi 2/3 


cpu=$(</sys/class/thermal/thermal_zone0/temp)
echo "$(date) @ $(hostname)"
echo "-------------------------------------------"
while true; do
    echo "GPU: $(/opt/vc/bin/vcgencmd measure_temp)"
    echo "CPU: temp=$(($(</sys/class/thermal/thermal_zone0/temp) / 1000))'C"
    sleep 2
done


