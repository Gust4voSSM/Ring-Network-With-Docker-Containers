docker build -t gust4vossm/hosts Hosts
docker build -t gust4vossm/auth Authority
docker compose down
docker compose up -d
docker attach ring-network-with-docker-containers-host-A-1