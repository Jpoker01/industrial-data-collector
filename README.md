# Industrial Data Collector

This project focuses on a IoT telemetry system featuring MQTT and Modbus TCP data pipelines. This fully containerized backend application collects sensor data, stores telemetry in MongoDB, manages device metadata in PostgreSQL, and serves everything through a Django REST API.  

## Quickstart guide

### Running the application

Run from the root of the frontend folder:  
```bash
npm install
npm run build
npm run preview
```

Navigate to `http://localhost:4173` (or the URL shown in your terminal)  

### Running backend application

Run from the backend folder:  
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip setuptools wheel 
pip install -r "requirements.txt"
uvicorn main:app --reload   
```


🔌 API EndpointsThe Django REST API is exposed on http://localhost:8000. Authenticate using Token Auth or Session Auth.  MeasurementsGET /api/measurements/  Returns unified JSON time-series measurements.  Query Params: ?protocol=mqtt|modbus, ?client_id=<id>, ?limit=100, ?refresh=5.  DevicesGET /api/devices/  Lists all registered devices and their metadata (Protocol, Serial Number, Client ID).  GET /api/devices/<id>/  Retrieve details for a specific device.  POST /api/devices/<id>/command/  Send control commands (start, stop) over MQTT to a specific publisher.  Body: {"command": "stop"}.  

## Project structure

The work can be broken into two main parts:
* **Experiments** - All of the Jupyter notebooks where different methods of AI are utilized and experimented with to find the optimal solution
* **Web application** - The web application where a chosen authorship verification model is deployed and where the user can verify the authorship of two texts.

### Experiments (`/experiments`)
Lists all the experiments done for this diploma thesis.

 * **requirements.txt** - The requirements for reproducing the implementation environment
 * **/conf** - Space for configurations
     * **/base** - Shared configuration like parameters
     * **/local** - Local configurations such as credentials
 * **/notebooks** - Jupyter notebooks - naming convention "YYYYMMDD_developerinitials_description"
   * **/dataset** - Notebooks related to dataset processing and analysis
   * **/graph** - Notebooks related to experiments utilizing integrated syntactic graphs
   * **/llm** - Notebooks utilizing LLMs
   * **/traditional** - Notebooks utilizing traditional BOW/TF-IDF representations for experiments 
   * **/transformer** - Notebooks utilizing transformer-based models for experiments
 * **/results** - Final analysis documents
   * **/llm** - Lists all the LLM experiment results (done before utilizing MLFlow)
   * **/prilohaC_MLFlow_all_experiments_export.xlsx** - Lists all the MLFlow results for other experiments than those utilizing LLMs
     
###  Web application (`/webapp`)
Contains the source code for the frontend and backend of the final web application solution

* **/frontend** - Contains the source code for the frontend of the web application
* **/backend** - Contains the source code for the backend of the web application
