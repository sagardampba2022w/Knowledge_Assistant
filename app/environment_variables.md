
# Environment Variables for Research Assistant Application

This document explains the purpose of the environment variables used in the Research Assistant Application. These variables configure various services such as Elasticsearch, PostgreSQL, Streamlit, and API keys required for the application to function properly.

## List of Environment Variables

### 1. **ELASTIC_PORT**
- **Default Value**: `9200`
- **Description**: The port number for accessing the Elasticsearch instance. This is used for indexing and searching through the data stored in the Elasticsearch server.

### 2. **POSTGRES_PORT**
- **Default Value**: `5432`
- **Description**: The port number for connecting to the PostgreSQL database. The application uses this database for storing structured data such as questions, answers, and performance metrics.

### 3. **STREAMLIT_PORT**
- **Default Value**: `8501`
- **Description**: The port where the Streamlit application runs. This is the web interface where users interact with the application.

### 4. **POSTGRES_HOST**
- **Default Value**: `postgres`
- **Description**: The hostname of the PostgreSQL database. In a Dockerized environment, this is often the service name of the PostgreSQL container.

### 5. **POSTGRES_DB**
- **Default Value**: `research_assistant`
- **Description**: The name of the PostgreSQL database that stores the application's data.

### 6. **POSTGRES_USER**
- **Default Value**: `your_username`
- **Description**: The username for authenticating with the PostgreSQL database.

### 7. **POSTGRES_PASSWORD**
- **Default Value**: `your_password`
- **Description**: The password for authenticating with the PostgreSQL database.

### 8. **MODEL_NAME**
- **Default Value**: `multi-qa-MiniLM-L6-cos-v1`
- **Description**: The name of the model used for the question-answering task. This model is used to process and answer user queries.

### 9. **INDEX_NAME**
- **Default Value**: `insights-questions`
- **Description**: The name of the Elasticsearch index where questions and insights are stored for retrieval and search.

### 10. **GRAFANA_ADMIN_PASSWORD**
- **Default Value**: `admin`
- **Description**: The admin password for the Grafana dashboard. This is used to secure access to the Grafana instance.

### 11. **OPENAI_API_KEY**
- **Default Value**: `enter your key`
- **Description**: The API key for accessing OpenAI's API. This key is required to make calls to OpenAI's GPT models.

### 12. **GROQ_API_KEY**
- **Default Value**: `enter your key`
- **Description**: The API key for accessing Groq's API. This is needed for any interaction with Groq services.

---

## How to Set Environment Variables

To set the environment variables, you can either:

- Add them to a `.env` file in your project's root directory. Example:
  ```
  ELASTIC_PORT=9200
  POSTGRES_PORT=5432
  STREAMLIT_PORT=8501
  POSTGRES_HOST=postgres
  POSTGRES_DB=research_assistant
  POSTGRES_USER=your_username
  POSTGRES_PASSWORD=your_password
  MODEL_NAME=multi-qa-MiniLM-L6-cos-v1
  INDEX_NAME=insights-questions
  GRAFANA_ADMIN_PASSWORD=admin
  OPENAI_API_KEY="enter your key"
  GROQ_API_KEY="enter your key"
  ```

- Alternatively, you can set them directly in your environment using the export command (for Linux/MacOS) or set command (for Windows).

Example (Linux/MacOS):
```bash
export ELASTIC_PORT=9200
export POSTGRES_PORT=5432
export STREAMLIT_PORT=8501
export POSTGRES_HOST=postgres
export POSTGRES_DB=research_assistant
export POSTGRES_USER=your_username
export POSTGRES_PASSWORD=your_password
export MODEL_NAME=multi-qa-MiniLM-L6-cos-v1
export INDEX_NAME=insights-questions
export GRAFANA_ADMIN_PASSWORD=admin
export OPENAI_API_KEY="enter your key"
export GROQ_API_KEY="enter your key"
```

---

## Notes
- Make sure to replace `your_username`, `your_password`, and the API keys with the actual credentials and keys you have.
- Keep sensitive information like API keys and database passwords secure and do not share them publicly.
