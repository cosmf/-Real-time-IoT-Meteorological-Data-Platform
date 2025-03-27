#!/bin/sh

while [ 1 ]; do
	nc -z scd3_mqtt-broker 1883 2> /dev/null \
	&& nc -z scd3_influxdb 8086 2> /dev/null \
	&& break;

	sleep 1;
done

python3 -u adaptor.py