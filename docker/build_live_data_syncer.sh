SHORT_SHA=$(git rev-parse --short HEAD)
docker build ../.. -f live_data_syncer/Dockerfile -t 192.168.1.50:29006/zhtangsh/live-data-syncer:dev.$SHORT_SHA
docker push 192.168.1.50:29006/zhtangsh/live-data-syncer:dev.$SHORT_SHA