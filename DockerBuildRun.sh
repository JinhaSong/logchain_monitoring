docker build -t logchain:monitoring .
docker run --privileged --device /dev/gpiomem --name logchain -it logchain:monitoring /bin/bash
docker start logchain