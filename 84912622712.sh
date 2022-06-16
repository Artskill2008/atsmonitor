#!/bin/bash

VAR1=$(grep -w "84912622712" /etc/zabbix/ast/report.txt | cut -b 28-)
#echo $VAR1
VAR2=ANSWERED
#echo $VAR2

if [ "$VAR1" = "$VAR2" ]; then
    echo 1
else
    echo 0
fi
