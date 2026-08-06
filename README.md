# Industrial Data Collector

This project features a IoT telemetry system utilizing MQTT and Modbus TCP data pipelines. 
This backend application collects sensor data, stores telemetry in MongoDB, manages device metadata in PostgreSQL, and serves everything through a Django REST API. The application is fully containerized using Docker.  
**Built as a technical assignment**

<img width="1536" height="1024" alt="diagram" src="https://github.com/user-attachments/assets/8169a8e7-c41a-4663-827c-2fb00bc5a4d2" />

## Architecture & Tech Stack
*   **Framework:** Django & Django REST Framework
*   **Databases:**
    *   **MongoDB 6+:** Stores high-volume, time-series sensor telemetry.
    *   **PostgreSQL 14+:** Stores relational metadata (users, sessions, device configurations).
*   **Protocols:**
    *   **MQTT:** Mosquitto Broker with TLS encryption and password authentication.
    *   **Modbus TCP:** Simulates industrial registers holding float32 values.
*   **Infrastructure:** Fully orchestrated via Docker & Docker Compose.

## How it works
Two pipelines run side by side and feed the same MongoDB instance:

*   **MQTT pipeline:** Each publisher simulates an IoT client, pulling a live price from the Coinbase API and publishing it to a `telemetry/<client-id>/<category>` topic on the Mosquitto broker. The ingest service is subscribed to `telemetry/#`, so it receives every message, shapes it into a document and inserts it into the `mqtt_measurements` collection. The broker uses TLS encryption, per-client username/password auth and an ACL file that restricts which topics each user can read from or write to. Anonymous access is disabled.
*   **Modbus pipeline:** The Modbus server simulates an industrial device, exposing a small register map that it refreshes every few seconds with a fresh price. The Modbus client polls those registers, decodes the float value and writes it into the `modbus_measurements` collection. Modbus has no authentication of its own, so the server is kept on the internal Docker network only and is never exposed to the host.

The Django REST API reads device metadata from PostgreSQL and measurements back out of MongoDB, and can also push `stop` / `start` commands down to the MQTT publishers. All API endpoints require a token, so measurements and device commands are only accessible to authenticated users.

## Quickstart guide

### Prerequisites
To run the full system, the following components will be required:
- Linux-based Operating System
- Docker and Docker Compose

### Running the application

The following instructions have to explicitly followed to prevent any issues when launching the system.

1. **Clone the repository** 
```bash
git clone https://github.com/Jpoker01/industrial-data-collector.git
cd industrial-data-collector
```

2. **Setup the environment**  
Copy the environment variables file and customize if necessary
```bash
cp .env.example .env
```

3. **Set up security**
This command generates the Mosquitto password file and the TLS certificates.
```bash
bash setup.sh
```

4. **Launch the system**  
```bash
docker-compose up
```

### API endpoints 

*Authentication:* All endpoints require token authentication. Log in via the Django Admin panel at `http://localhost:8000/admin/` using valid login details, or request an API token at `/api/token/`.
The following API endpoints are accessible through the Django API:
*   `GET /api/devices/` - List all registered devices from PostgreSQL.
*   `GET /api/devices/<id>/` - Retrieve a single device by its ID.
*   `GET /api/measurements/` - Retrieve collected sensor data from MongoDB. Supports these query parameters:
    * `?protocol=mqtt` - specify the pipeline to list the data from (`mqtt` or `modbus`; both if omitted)
    * `?client_id=pub-1` - filter by a specific client
    * `?limit=50` - maximum number of entries to get
    * `?refresh=5` - browser auto-refresh interval in seconds (set to `0` to disable)
* `POST /api/devices/<id>/command/` - Send a control command to an MQTT client to either stop or resume its publishing. **Payload** can be either `{"command": "stop"}` or `{"command": "start"}`.

### Running Unit Tests
The Django application is covered by unit tests verifying the REST endpoints and MQTT command dispatch logic. Run using the following command:
```bash
docker-compose exec django python manage.py test
```

## Project structure
 
The project structure is as follows:
 
 * **certs/** - Folder where TLS security files are stored upon set-up
 * **django_app/** - Django API application
   * **config/** - Configuration of the full app
   * **devices/** - Logic for devices and commands functionality
   * **measurements/** - Logic for obtaining measurements
 * **mosquitto/config/** - Stores configuration for Mosquitto and hashed passwords for clients upon setup
 * **services/** - Data pipeline services
   * **common/** - Shared connection code for the clients
   * **mqtt_publisher/** - Codebase for MQTT clients publishing data to Mosquitto
   * **mqtt_ingest/** - Codebase for the MQTT client ingesting data and storing it into MongoDB
   * **modbus_server/** - Modbus code simulating industrial registers
   * **modbus_client/** - Modbus client code for obtaining data from the Modbus server and storing it into MongoDB
