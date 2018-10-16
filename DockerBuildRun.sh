docker build -t logchain:monitoring .
docker run --privileged --device /dev/gpiomem --name logchain-test \
  -p 5000:5000 \
  -p 8000:8000 \
  -p 8888:8888 \
  -p 9999:9999 \
  -p 10101:10101 \
  -p 10654:10654 \
  -it logchain:latest /bin/bash
docker start logchain