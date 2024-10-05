## Testing the app - Local Environment Setup

This guide provides instructions to set up and test the Research Knowledge Base Assistant locally using Docker, PostgreSQL, Streamlit & Grafana.

### Prerequisites

Make sure you have the following installed on your system:

- Docker
- Docker Compose
- Python


### Steps 

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
Ensure the environment variables are set, particularly for PostgreSQL as the we are testing in local environment:
bash
```
export POSTGRES_HOST=localhost
```

### 5. Initialize the Database and Index Documents
Run the following Python script in the terminal to initialize the database and index documents in Elasticsearch:
```
python data_prep.py
```
### 6. Verify Database Connection
Use pgcli to verify that the PostgreSQL database is running and connected properly:

```
pgcli -h localhost -p 5432 -U your_username -d research_assistant
enter your password : your_password
```

You can run SQL queries to check if the tables are created correctly:
Start by running below commands after entering password
```
 
\dt 
SELECT * FROM conversations LIMIT 10;
SELECT * FROM feedback LIMIT 10;
\q
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

First initiate the database from terminal
```
pgcli -h localhost -p 5432 -U your_username -d research_assistant
enter your password : your_password
```

Then querying the database
```
SELECT * FROM conversations LIMIT 10;
SELECT * FROM feedback LIMIT 10;
```

### 10. Set up Grafana Dashboard 

To set up the Grafana dashboard, follow these steps:

a. **Visit the Grafana Portal**:
   - Open [localhost:3000](http://localhost:8501) in your browser.

b. **Login**:
   - Enter the login credentials:
     - **Username**: `admin` (as set in `docker-compose`)
     - **Password**: `admin` (as set in `docker-compose`)
   - Optional: You can skip setting a new password since this is for local testing.

c. **Connect PostgreSQL Data Source**:
   - After logging in, you will need to connect to the PostgreSQL data source:
     - **Name**: Set a source name (choose a descriptive name).
     - **Host URL**: `postgres:5432` (as specified in the environment file).
     - **Database Name**: `research_assistant` (as specified in the environment file).
     - **Username**: `your_assistant`.
     - **Password**: `your_password`.
     - **TLS/SSL Mode**: Set to `disable`.
     - Click **Save and Test** to verify the connection.

d. **Visualize Data**:
   - Use SQL queries to visualize the stored data in dashboard panels. Here are some example queries:

     **Example 1: Response Time Query**
     ```sql
     SELECT
       timestamp AS time,
       response_time
     FROM conversations
     ORDER BY timestamp
     ```

     **Example 2: Relevance Distribution Query**
     ```sql
     SELECT
       relevance,
       COUNT(*) as count
     FROM conversations
     GROUP BY relevance
     ```

e. **Additional SQL Queries**:
   - For a detailed list of SQL queries to use in Grafana dashboard panels, refer to the following link:
     - [SQL Queries for Grafana Dashboard](https://github.com/sagardampba2022w/Knowledge_Assistant/blob/main/app/grafana_sql_queries.md)


### 11. Additional Notes
- Ensure that your .env file is properly configured with necessary API keys and environment variables. Refer to list of env variables to be set
[List of enivronment variables](https://github.com/sagardampba2022w/Knowledge_Assistant/blob/main/app/environment_variables.md)
- If you encounter errors related to keys or secrets, verify that your API keys are correctly set in the environment or .env file.
- Currently elastic search memory usage is fixed to 512mb as "ES_JAVA_OPTS=-Xms512m -Xmx512m", feel free to change or remove this from docker-compose file in case datasize increases.