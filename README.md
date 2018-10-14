# logchain for monitoring
_Blockchain platform for IoT_

## Features
- Provides the light-weight consensus for IoT 
- Run on Raspberry Pi platform

## Requirements
- PyQt5
- flask
- netifaces

## Launch Logchain in Docker

```
# Modify the peerconnector.json file to match the peer information
vi peerconnector.json

# Docker build
docker build -t logchain:latest .

# Docker Run
docker run --privileged --device /dev/gpiomem --name logchain-test \
  -p 5000:5000 \
  -p 8000:8000 \
  -p 8888:8888 \
  -p 9999:9999 \
  -p 10101:10101 \
  -p 10654:10654 \
  -it logchain:latest /bin/bash
  
# Launch Logchain
docker ps -a

CONTAINER ID        IMAGE                 COMMAND             CREATED             STATUS                      PORTS               NAMES
c0244c899c4a        logchain:latest       "/bin/bash"         23 minutes ago      Exited (0) 20 minutes ago                       logchain

docker exec -it c0244c899c4a /bin/bash /workspace/run_generic.sh

# Generate transactions(URL: http://192.168.0.1:5000/tx/save/ | Interval: 5sec)
docker exec -it c0244c899c4a /bin/bash /workspace/run_demo_loop.sh http://192.168.0.1:5000/tx/save/ 5
```
