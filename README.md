# Industrial Data Collector

This project features a IoT telemetry system utilizing MQTT and Modbus TCP data pipelines. 
This backend application collects sensor data, stores telemetry in MongoDB, manages device metadata in PostgreSQL, and serves everything through a Django REST API. The application is fully containerized using Docker.  
**Built as a technical assignment**

## Architecture & Tech Stack
*   **Framework:** Django & Django REST Framework
*   **Databases:** 
    *   **MongoDB 6+:** Stores high-volume, time-series sensor telemetry.
    *   **PostgreSQL 14+:** Stores relational metadata (users, sessions, device configurations).
*   **Protocols:** 
    *   **MQTT:** Mosquitto Broker with TLS authentication.
    *   **Modbus TCP:** Simulates industrial registers holding float32 values.
*   **Infrastructure:** Fully orchestrated via Docker & Docker Compose.

## System Components
*   **Mosquitto MQTT Broker:** Secure broker handling client telemetry and remote commands.
*   **MQTT Publisher (Clients):** Simulates IoT clients fetching live public API data on prices from Coinbase API and publishing to the broker.
*   **MQTT Ingest Service:** Subscribes to the broker and routes incoming data to MongoDB.
*   **Modbus Server & Client:** Simulates industrial registers and periodically obtains data to store in MongoDB.
*   **Django REST API:** Provides an interface to display collected data and dispatch remote commands.

## Quickstart guide

### Prerequisites
To run the full system, the following components will be required:
- Linux-based Operating System
- Docker and Docker Compose

### Running the application

The following instructions have to explicitly followed to prevent any issues when launching the system.

1. **Clone the repository** 
```bash
git clone [https://github.com/Jpoker01/industrial-data-collector.git](https://github.com/Jpoker01/industrial-data-collector.git)
cd industrial-data-collector
```

2. **Setup the environment**  
Copy the environment variables file and customize if necessary
```bash
cp .env.example .env
```

3. **Set up security**  
```bash
bash setup.sh
```

4. **Launch the system**  
```bash
docker-compose up
```

### API endpoints 

*Authentication:* All endpoints require token authentication. Log in via the Django Admin using valid logon details panel at `http://localhost:8000/admin/` or request an API token at `/api/token/`.  
The following API endpoints are accessible through the Django API:
*   `GET /api/devices/` - List all registered devices (from PostgreSQL).
*   `GET /api/measurements/` - Retrieve collected sensor data (from MongoDB). Supports query parameters:
    * `?protocol=mqtt` - to specify the pipeline from which we want to list the data
    * `?limit=50` - maximum number of entries to get
* `POST /api/devices/<id>/command/` - Send a control command to MQTT client to either stop or resume their publishing. **Payload** can be either `{"command": "stop"}` or `{"command": "start"}`.

### Running Unit Tests
The Django application is covered by unit tests verifying the REST endpoints and MQTT command dispatch logic. Run using the following command:
```bash
docker-compose exec django python manage.py test
```

## Project structure

The work can be broken into two main parts:
* **Experiments** - All of the Jupyter notebooks where different methods of AI are utilized and experimented with to find the optimal solution
* **Web application** - The web application where a chosen authorship verification model is deployed and where the user can verify the authorship of two texts.

### Experiments (`/experiments`)
Lists all the experiments done for this diploma thesis.

 * **certs** - Folder where TLS security files are stored upon set-up
 * **/django** - Django API application
   * **/config** - Config of the full app
   * **/devices** - Logic for devices and commands functionality
   * **measurements** - Logic for obtaining measurements
 * **mosquitto/conf** - Stores configuration for Mosquitto and hashed passwords for clients upon setup
 * **/services** - Final analysis documents
   * **/common** - Shared connection code for mqtt clients
  * **/mqtt_publisher** - Codebase for MQTT clients publishing data to Mosquitto
   * **/mqtt_ingest** - Codebase for MQTT clients ingesting data and storing it into MongoDB
   * **/modbus_server** - Modbus code simulating industrial registers
   * **/modbus_client** - Modbus client code for obtaning data from the modbus server and storing it into MongoDB
