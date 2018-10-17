#!/bin/bash
if [ $# -eq 0 ]
    then
        echo "Please input request url"
    else
        url=$1
        interval=$2
        echo "Press [CTRL+C] to stop."
        while :
        do
            python demo/demo_savetx/demo_once.py "http://"$url":5000/tx/save"
            sleep $interval"m"
        done
fi
