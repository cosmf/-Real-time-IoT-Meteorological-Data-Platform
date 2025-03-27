#!/bin/bash

# python3 ./adaptor/adaptor.py > adaptor.log 2>&1 &

# export SCD_DVP=${SCD_DVP:-/var/lib/docker/volumes}


# Create necessary directories for volumes
# mkdir -p $SCD_DVP/mosquitto_data $SCD_DVP/mosquitto_logs $SCD_DVP/influxdb_data $SCD_DVP/grafana_data

# Initialize Docker Swarm if not already initialized
docker swarm leave --force 2>/dev/null || echo "No swarm to leave"

docker swarm init 2>/dev/null || echo "Swarm already initialized"

# Build Docker images
docker compose -f stack.yml up --build --force-recreate -d

# Deploy the stack
docker stack deploy -c stack.yml scd3 --detach=false

echo "Deployment complete. Access Grafana at http://localhost:3000"