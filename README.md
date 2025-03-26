# IoT Meteorological Data Platform

This repository contains the implementation of an **IoT platform** for real-time collection, storage, and visualization of meteorological data from distributed sensors. The system uses a **microservices architecture** orchestrated with **Docker Swarm** and leverages key technologies for scalability, persistence, and dynamic data analytics.

## Overview

The platform is designed to:

- Collect meteorological data from IoT sensors via **MQTT**.
- Persist time-series data using **InfluxDB** with Docker volumes.
- Visualize and explore data interactively through **Grafana** dashboards.
- Ensure secure and isolated communication between services through custom **Docker Swarm networking**.
- Support modular scaling and easy maintenance via service-oriented design.

## Technologies Used

- **MQTT** – lightweight messaging protocol for IoT.
- **Docker Swarm** – container orchestration for deployment and scaling.
- **InfluxDB** – time-series database for storing sensor data.
- **Grafana** – dashboarding and visualization.
- **Telegraf / Custom Processor** – optional for ingestion/parsing.
- **Loki** - for loggs and solving buggs

## Features

- Real-time data ingestion and storage.
- Persistent volumes for InfluxDB.
- Dynamic visualization with custom Grafana dashboards.
- Secure and modular communication via overlay networks.
- Configurable sensor topics and data processing pipelines.

