# Knowledge Base Assistant - Syndicated Research 


## Table of Contents
- [Overview](#overview)
- [Technologies](#technologies)
- [RAG based LLM Approach](#rag-based-llm-approach)
  - [User Question Flow](#user-question-flow)
- [Evaluations](#evaluations)
  - [RAG Search Evaluation](#rag-search-evaluation)
    - [Performance Metrics](#rag-search-evaluation---performance-metrics)
  - [LLM Response Evaluation](#llm-response-evaluation)
    - [Cosine Similarity](#cosine-similarity)
    - [LLM as a Judge](#llm-as-a-judge)
      - [AQA Evaluation (LLM Answer + Original Question Answer)](#aqa-evaluation-llm-answer--original-question-answer)
      - [QA Evaluation (Original Question + LLM Answer)](#qa-evaluation-original-question--llm-answer)
- [How to Test the App in Local Environment Setup](#testing-the-app---local-environment-setup)


## Project Structure

```
.
├── Data_prep                      # Folder for data preparation files
│   ├── data.csv                   # Original Q&A raw data used 
│   ├── final_data.csv             # Final cleaned and processed data in CSV format
│   ├── final_data.json            # Final cleaned and processed data in JSON format
│   ├── ground_truth_data.csv      # Ground truth Q&A data for evaluation
│   └── results.bin                # Serialized binary file storing results 
├── Evaluation                     # Folder containing evaluation scripts and assets
│   ├── LLM Evaluation             # Scripts or data for evaluating the language model
│   └── Search Evaluation          # Scripts or data for evaluating search algorithms or results
├── app                            # Application folder containing the app code and configurations
│   ├── Dockerfile                 # Docker configuration for building the app container
│   ├── Readme.md                  # Steps to test app locally
│   ├── app.py                     # Main application script for Streamlit app
│   ├── assistant.py               # Script for LLM API calling 
│   ├── data_prep.py               # Script for indexing data and initializing the database
│   ├── db.py                      # Postgres database interaction script
│   ├── docker-compose.yaml        # Docker Compose file to define and run multi-container Docker applications
│   ├── env.txt                    # Environment variables configuration notes
│   └── requirements.txt           # List of dependencies required to run the application
├── Assets                         # Miscellaneous files
├── README.md                      # Detailed project overview and documentation
└── .gitignore                     # List of files and directories to ignore in Git

```




## Overview

**Knowledge Assistant** is a tool that simplifies access to the underlying structure and methodology of syndicated market research. The **Knowledge Assistant** is powered by a comprehensive dataset that includes question-answer pairs related to syndicated market research. These question-answer pairs are categorized into the following sections to help users quickly get answers to specific research related queries 

- **General Information**: Questions related to the overall scope and purpose of the research.
- **Data Collection Methodology**: Information about how the data was collected, including sample size, demographics, and methodology.
- **Data Access and Reporting**: Focused on the ways users can access reports and the types of reporting available.
- **Data Usage and Application**: How to apply the data in various contexts for business insights and decision-making.
- **Technical Support**: Queries about resolving technical issues and troubleshooting data tools.
- **Subscription and Pricing**: Questions regarding pricing models and subscription options.
- **Data Segmentation and Custom Queries**: Information on how to segment the data and perform custom queries.
- **Advanced Analytics and Predictive Modeling**: Addressing advanced techniques for analyzing data, including predictive models.
- **Competitive Benchmarking**: Questions focused on comparing data with competitor benchmarks.
- **Consumer Sentiment and Feedback**: How to measure consumer feedback and sentiment analysis through the data.
- **Data Export and Integration**: Methods of exporting data and integrating with other tools or platforms.
- **Reporting and Visualization Tools**: Information on the visualization tools available for data interpretation.


This makes it easier for anyone, regardless of their expertise in market research, to understand how a study was conducted and what parameters were used, without needing to sift through complex reports manually.

By providing clear explanations on how the research was performed, **Knowledge Assistant** ensures that users can confidently interpret and apply the data in their work, supporting informed decision-making and effective use of market research insights.

The **synthentic dataset** for 260 Q&A pairs was generated using CHATGPT model-4o. 

You can access the dataset here: [Dataset Link](https://github.com/sagardampba2022w/Research_Knowledge_base_Assistant/blob/main/Data_prep/data.csv)

---




## Technologies

The **Knowledge Assistant** utilizes a modern tech stack designed for scalability, performance, and ease of deployment. Key technologies include:

- **Python**: The core programming language for developing the backend logic and handling data processing tasks.
- **Docker & Docker Compose**: For containerization, ensuring a consistent development and production environment, making deployment easier across different platforms.
- **Elasticsearch**: Used for efficient full-text search, enabling rapid retrieval of relevant information from large datasets.
- **Streamlit**: The front-end framework for building an interactive and user-friendly interface where users can ask questions and view results.
- **Grafana**: Employed for monitoring system performance and health, with **PostgreSQL** serving as the backend database to store monitoring data.
- **OpenAI & Groq**: API's used to access core large language models (LLMs) gpt 4o, 4o mini, Llama 8b & 70b to process natural language queries and generate intelligent, contextually accurate responses.

 
## Knowledge Assistant Deployment 

The **Knowledge Assistant** follows a structured approach to ensure accurate and contextually relevant responses:

1. **User Question**: The process begins when a user submits a question through the interface.
2. **Embedding Conversion**: The question is converted into vector embeddings, which represent the semantic meaning of the question.
3. **Vector Search**: These embeddings are then used to search the original dataset through a vector-based search in **Elasticsearch**, retrieving the most relevant sections of the data.
4. **LLM Processing**: The retrieved information is passed to the large language models (**OpenAI** & **Groq**), which process the data and generate a refined, coherent response based on the context of the user’s question.
5. **User Response**: The final response is delivered back to the user in a natural language format.

This combination of vector search and LLM response generation ensures that users receive accurate, relevant answers to their questions, derived from complex market research data.

![App Deployment](https://github.com/sagardampba2022w/Research_Knowledge_base_Assistant/blob/main/Assets/deployment.jpg)


## Evaluations

### RAG Search Evaluation

Multiple approaches were evaluated using **Elasticsearch** to optimize the retrieval of relevant data. The approaches tested include:

1. **Text Search**: A traditional full-text search using keywords from the user's question.
2. **Vector Search (with matching Question)**: Using vector embeddings of the user's question to retrieve semantically similar content.
3. **Vector Search (with matching Answers)**: Using embeddings of potential answers to retrieve documents that contain semantically related answers.
4. **Vector Search (with matching Question and Answers)**: Combining both question and answer embeddings for a more comprehensive retrieval approach.
5. **Hybrid Search (Vector  & Text Search)**: A combined approach that integrates both vector-based and traditional text search for improved accuracy.
6. **Hybrid Search (Vector & Text Search) + RRF Implementation**: Incorporating Rank Reciprocal Fusion (RRF) to merge and rank results from different search methods for optimal relevance.

These approaches were evaluated using the following metrics:
- **Hit Rate**: The percentage of relevant documents retrieved.
- **MRR (Mean Reciprocal Rank)**: A measure of how well the ranking of the relevant results was optimized.


### RAG Search Evaluation - Performance Metrics

| Search Method                                         | Hit Rate   | Mean Reciprocal Rank (MRR) |
|-------------------------------------------------------|------------|----------------------------|
| Text Search                                           | 0.7292     | 0.4804                     |
| Question Vector                                       | 0.8154     | 0.6720                     |
| Answer Vector                                         | 0.9000     | 0.7621                     |
| Combined Question + Answer Vector                     | 0.8815     | 0.7473                     |
| Hybrid (Question Vector + Keyword)                    | 0.8631     | 0.6993                     |
| Hybrid (Answer Vector + Keyword)                      | 0.8685     | 0.7042                     |
| Hybrid (Combined QA Vector + Keyword)                 | 0.8608     | 0.6975                     |
| Hybrid (Combined QA Vector + Keyword) + RRF           | **0.9162** | **0.7835**                 |

> **Link to RAG Search Evaluation Code**: [RAG Search Evaluation Notebook](https://github.com/sagardampba2022w/Research_Knowledge_base_Assistant/tree/main/Evaluation/Search%20Evaluation%20)



### LLM Response Evaluation



The LLM responses were evaluated using two methods **Cosine Similarity** & **LLM as a Judge**:

1. **LLM Eval (Cosine Similarity)**: This measured the similarity between the retrieved context and the generated response using cosine similarity to ensure the response aligned with the relevant parts of the data.


- **LLMs Tested**:
  - OpenAI GPT-4o
  - OpenAI GPT-4o-mini
  - OpenAI GPT-3.5
  - LLaMA 8B
  - LLaMA 70B

The following table shows the evaluation stats for different LLMs based on **Mean **, **Median **, and **Standard Deviation** for cosine values:

| Model         | Mean        | Median        | Standard Deviation |
|---------------|-------------|---------------|--------------------|
| GPT-3.5       | 0.773680    | 0.794979      | 0.152885           |
| GPT-4o        | 0.770313    | 0.790879      | 0.136325           |
| GPT-4o-mini   | 0.773590    | 0.790323      | 0.133313           |
| LLaMA-8B      | 0.734798    | 0.751954      | 0.124470           |
| LLaMA-70B     | 0.738416    | 0.757077      | 0.132759           |

![Cosine Similarity Chart](https://github.com/sagardampba2022w/Research_Knowledge_base_Assistant/blob/main/Assets/output.png)

> **Link to Cosine Similarity Code**: [Cosine Similarity Evaluation Notebook](https://github.com/sagardampba2022w/Research_Knowledge_base_Assistant/blob/main/Evaluation/LLM%20Evaluation/Offline_RAG_Eval.ipynb)



These metrics provide insight into how closely the generated responses matched the context retrieved by the RAG search in terms of cosine similarity.


  
2. **LLM as a Judge (Relevance)**: This evaluation method was split into two distinct processes:
   
   - **AQA (Answer + Question Answer)**: In this approach, the original QA pair along with the LLM-generated answer were passed to another LLM (GPT-4o-mini) to evaluate the relevance of the response.
   - **QA (Question + Answer)**: In this approach, only the question and the LLM-generated answer were passed to the judge, without the original answer, for relevance evaluation.

- **LLMs Tested**:
  - OpenAI GPT-4o
  - OpenAI GPT-3.5
  - LLaMA 8B
  - LLaMA 70B


##### AQA Evaluation (LLM Answer + Original Question Answer)

| LLM Model       | Relevant (%) | Partially Relevant (%) | Non-Relevant (%) |
|-----------------|--------------|------------------------|------------------|
| GPT-4o AQA      | **81.46**    | 18.23                  | 0.31             |
| GPT-3.5 AQA     | **72.69**    | 25.54                  | 1.77             |
| LLaMA-8B AQA    | **75.92**    | 23.46                  | 0.62             |
| LLaMA-70B AQA   | **75.92**    | 23.69                  | 0.38             |

##### QA Evaluation (Original Question + LLM Answer)

| LLM Model       | Relevant (%) | Partially Relevant (%) | Non-Relevant (%) |
|-----------------|--------------|------------------------|------------------|
| GPT-4o QA       | **94.85**    | 4.92                   | 0.23             |
| GPT-3.5 QA      | **89.38**    | 10.31                  | 0.31             |
| LLaMA-8B QA     | **92.85**    | 7.08                   | 0.08             |
| LLaMA-70B QA    | **93.46**    | 6.23                   | 0.31             |

These evaluations were used to assess the performance of different LLMs in terms of how well they generate relevant and accurate answers based on the user’s query.

> **Link to QA Evaluation Code**: [QA Evaluation Notebook](https://github.com/sagardampba2022w/Research_Knowledge_base_Assistant/blob/main/Evaluation/LLM%20Evaluation/LLM_judge.ipynb)



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
### 10. Set up grafana dashbord 

Setup dashboard on grafana by 
- visiting [localhost:3000](http://localhost:8501)
- connecting same postgres database with host postgres:5432 to access app stored data
- visualise the stored data in dashboard panels from database


### 11. Additional Notes
Ensure that your .env file is properly configured with necessary API keys and environment variables.
If you encounter errors related to keys or secrets, verify that your API keys are correctly set in the environment or .env file.