SHORT_SHA=$(git rev-parse --short HEAD)
docker build ../.. -f md/Dockerfile -t 192.168.1.50:29006/wdl/ctpmd:dev.$SHORT_SHA
docker push 192.168.1.50:29006/wdl/ctpmd:dev.$SHORT_SHA
