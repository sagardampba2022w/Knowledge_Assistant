# Research Knowledge Base Assistant - Local Environment Setup

This guide provides instructions to set up and test the Research Knowledge Base Assistant locally using Docker and PostgreSQL.

## Prerequisites

Make sure you have the following installed on your system:

- Docker
- Docker Compose
- Python


## Steps to Set Up and Test the App

### 1. Clone the Repository


```
git clone https://github.com/sagardampba2022w/Research_Knowledge_base_Assistant.git
cd Research_Knowledge_base_Assistant
```

### 2. Build the Docker Containers
Build the application containers using Docker Compose:
```
docker-compose build
```

### 3. Start the Containers
Start all services, including PostgreSQL, Elasticsearch, Streamlit, and Grafana:
```
docker-compose up
```
### 4. Set Environment Variables
Ensure the environment variables are set, particularly for PostgreSQL:
bash
```
export POSTGRES_HOST=localhost
```

### 5. Initialize the Database and Index Documents
Run the following Python script to initialize the database and index documents in Elasticsearch:
```
python data_prep.py
```
### 6. Verify Database Connection
Use pgcli to verify that the PostgreSQL database is running and connected properly:

```
pgcli -h localhost -p 5432 -U your_username -d research_assistant
```

You can run SQL queries to check if the tables are created correctly, such as:
```
SELECT * FROM conversations LIMIT 10;
SELECT * FROM feedback LIMIT 10;
```
### 7. Restart Streamlit Service
If the database or Elasticsearch is not connected properly, you may need to restart the Streamlit container:
```
docker-compose stop streamlit
docker-compose up streamlit
```
### 8. Access the Application
Once everything is set up and the services are running, you can access the Streamlit app in your browser by navigating to:
http://localhost:8501

### 9. Verify Feedback and Conversations Are Stored
You can verify if the feedback and conversations are being stored correctly in PostgreSQL by querying the database:
```
SELECT * FROM conversations LIMIT 10;
SELECT * FROM feedback LIMIT 10;
```

### 10. Additional Notes
Ensure that your .env file is properly configured with necessary API keys and environment variables.
If you encounter errors related to keys or secrets, verify that your API keys are correctly set in the environment or .env file.