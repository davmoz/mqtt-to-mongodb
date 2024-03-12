# MQTT to MongoDB IoT Data Collector

This repository contains the Docker setup for an IoT Data Collector service. It includes a Python-based agent for collecting data from various sources via MQTT and storing this data in MongoDB for further analysis.

## Features

- **MQTT Integration:** Connects to an MQTT broker to subscribe to topics and collect data.
- **MongoDB Storage:** Stores collected data in a MongoDB database for persistence and easy retrieval.
- **Dockerized Services:** Includes Docker Compose setup for easy deployment of both the MQTT agent and MongoDB database.

## Prerequisites

- Docker and Docker Compose installed on your system.
- Basic knowledge of Docker, MQTT, and MongoDB.

## Configuration

Before running the application, you need to set up your environment variables:

1. Copy the `.env.example` file to a new file named `.env`:

   ```
   cp .env.example .env
   ```

2. Open the `.env` file in your text editor of choice.

3. Replace the example values with your actual environment-specific values. This includes setting up the MongoDB credentials, MQTT broker details, etc.

4. Save the `.env` file. The application will read this file to configure itself upon startup.

## Installation

To deploy the IoT Data Collector, follow these steps:

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/davmoz/mqtt-to-mongodb.git
   ```
2. Navigate to the cloned repository directory:
   ```
   cd mqtt-to-mongodb
   ```
3. Run the Docker Compose up command to build and start the services:
   ```
   docker-compose up --build
   ```
   or run the services in the background:
   ```
    docker-compose up -d --build
   ```

## Usage

After deploying the services, the agent service will automatically start collecting data from the configured MQTT topics and store this data in the MongoDB database.

You can interact with the MongoDB database using MongoDB's CLI or GUI tools to query and manage the collected data.

## Contributing

We welcome contributions to improve the IoT Data Collector project! If you have suggestions or improvements, please fork the repository and submit a pull request.

For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
