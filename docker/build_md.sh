SHORT_SHA=$(git rev-parse --short HEAD)
docker build ../.. -f md/Dockerfile -t 192.168.20.204:30000/wdl/ctpMd:dev.$SHORT_SHA
