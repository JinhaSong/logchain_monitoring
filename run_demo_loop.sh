#!/bin/bash
if [ $# -eq 0 ]
    then
        echo "Please input request url"
    else
        url=$1
        echo "Press [CTRL+C] to stop."
        while :
        do
            python demo/demo_savetx/demo_once.py $url
            sleep 5
        done
fi
