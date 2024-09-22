# Knowledge Base Assistant - Syndicated Research FAQ

## Overview

**Knowledge Assistant** is a tool that simplifies access to the underlying structure and methodology of syndicated market research. It helps users quickly find answers related to:

- **Approach**
- **Methodologies**
- **Sample Coverage**
- **Geographic Coverage**
- **Analysis Types**

This makes it easier for anyone, regardless of their expertise in market research, to understand how a study was conducted and what parameters were used, without needing to sift through complex reports manually.

By providing clear explanations on how the research was performed, **Knowledge Assistant** ensures that users can confidently interpret and apply the data in their work, supporting informed decision-making and effective use of market research insights.


## Dataset

The **Knowledge Assistant** is powered by a comprehensive dataset that includes question-answer pairs related to syndicated market research. These question-answer pairs are categorized into the following sections:

- **General**: Questions related to the overall scope and purpose of the research.
- **Market**: Focused on market definitions, market scope, and geographic coverage.
- **Category**: Addresses specific product or service categories covered in the research.
- **Sample**: Information on the sample size, demographics, and sampling methods used in the research.
- **Analysis**: Questions that dive into the types of analysis performed, including statistical methods, data interpretation, and segmentation approaches.

By structuring the dataset into these categories, **Knowledge Assistant** is able to provide highly relevant and contextualized answers, ensuring users can quickly find the specific information they need about how syndicated research is conducted.

You can access the dataset here : [Dataset Link](https://github.com/sagardampba2022w/Research_Knowledge_base_Assistant/blob/main/Data_prep/data.csv)


## Technologies

The **Knowledge Assistant** utilizes a modern tech stack designed for scalability, performance, and ease of deployment. Key technologies include:

- **Python**: The core programming language for developing the backend logic and handling data processing tasks.
- **Docker & Docker Compose**: For containerization, ensuring a consistent development and production environment, making deployment easier across different platforms.
- **Elasticsearch**: Used for efficient full-text search, enabling rapid retrieval of relevant information from large datasets.
- **Streamlit**: The front-end framework for building an interactive and user-friendly interface where users can ask questions and view results.
- **Grafana**: Employed for monitoring system performance and health, with **PostgreSQL** serving as the backend database to store monitoring data.
- **OpenAI & Groq**: Used as the core large language models (LLMs) to process natural language queries and generate intelligent, contextually accurate responses.


## RAG based LLM Approach

The **Knowledge Assistant** follows a structured approach to ensure accurate and contextually relevant responses:

1. **User Question**: The process begins when a user submits a question through the interface.
2. **Embedding Conversion**: The question is converted into vector embeddings, which represent the semantic meaning of the question.
3. **Vector Search**: These embeddings are then used to search the original dataset through a vector-based search in **Elasticsearch**, retrieving the most relevant sections of the data.
4. **LLM Processing**: The retrieved information is passed to the large language models (**OpenAI** & **Groq**), which process the data and generate a refined, coherent response based on the context of the user’s question.
5. **User Response**: The final response is delivered back to the user in a natural language format.

This combination of vector search and LLM response generation ensures that users receive accurate, relevant answers to their questions, derived from complex market research data.


## Evaluations

### RAG Search Evaluation

Multiple approaches were evaluated using **Elasticsearch** to optimize the retrieval of relevant data. The approaches tested include:

1. **Text Search**: A traditional full-text search using keywords from the user's question.
2. **Vector Search (with matching Question)**: Using vector embeddings of the user's question to retrieve semantically similar content.
3. **Vector Search (with matching Answers)**: Using embeddings of potential answers to retrieve documents that contain semantically related answers.
4. **Vector Search (with matching Question and Answers)**: Combining both question and answer embeddings for a more comprehensive retrieval approach.
5. **Hybrid Search (Vector & Text Search)**: A combined approach that integrates both vector-based and traditional text search for improved accuracy.
6. **Hybrid Search (Vector & Text Search) + RRF Implementation**: Incorporating Rank Reciprocal Fusion (RRF) to merge and rank results from different search methods for optimal relevance.

These approaches were evaluated using the following metrics:
- **Hit Rate**: The percentage of relevant documents retrieved.
- **MRR (Mean Reciprocal Rank)**: A measure of how well the ranking of the relevant results was optimized.

### LLM Response Evaluation

After retrieving relevant data via the RAG search, the **LLMs (OpenAI & Groq)** generate the final user response. The quality of the LLM responses was evaluated based on:

- **Relevance**: Assessed using three categories:
  - **Relevant**: The response fully addresses the query.
  - **Partially Relevant**: The response addresses part of the query but is incomplete.
  - **Not Relevant**: The response does not address the query.
  
These evaluations ensure that both the retrieval mechanism and the LLM-generated responses meet high standards of accuracy and relevance.

## Evaluations

### RAG Search Evaluation

Multiple approaches were evaluated using **Elasticsearch** to optimize the retrieval of relevant data. The approaches tested include:

1. **Text Search**: A traditional full-text search using keywords from the user's question.
2. **Vector Search (with matching Question)**: Using vector embeddings of the user's question to retrieve semantically similar content.
3. **Vector Search (with matching Answers)**: Using embeddings of potential answers to retrieve documents that contain semantically related answers.
4. **Vector Search (with matching Question and Answers)**: Combining both question and answer embeddings for a more comprehensive retrieval approach.
5. **Hybrid Search (Vector & Text Search)**: A combined approach that integrates both vector-based and traditional text search for improved accuracy.
6. **Hybrid Search (Vector & Text Search) + RRF Implementation**: Incorporating Rank Reciprocal Fusion (RRF) to merge and rank results from different search methods for optimal relevance.

These approaches were evaluated using the following metrics:
- **Hit Rate**: The percentage of relevant documents retrieved.
- **MRR (Mean Reciprocal Rank)**: A measure of how well the ranking of the relevant results was optimized.

### LLM Response Evaluation

The LLM responses were evaluated using two methods:

1. **LLM Eval (Cosine Similarity)**: This measured the similarity between the retrieved context and the generated response using cosine similarity to ensure the response aligned with the relevant parts of the data.

The following table shows the evaluation results for different LLMs based on **Mean Cosine**, **Median Cosine**, and **Standard Deviation**:

| Model         | Mean Cosine | Median Cosine | Standard Deviation |
|---------------|-------------|---------------|--------------------|
| GPT-3.5       | 0.773680    | 0.794979      | 0.152885           |
| GPT-4o        | 0.770313    | 0.790879      | 0.136325           |
| GPT-4o-mini   | 0.773590    | 0.790323      | 0.133313           |
| LLaMA-8B      | 0.734798    | 0.751954      | 0.124470           |
| LLaMA-70B     | 0.738416    | 0.757077      | 0.132759           |

These metrics provide insight into how closely the generated responses matched the context retrieved by the RAG search in terms of cosine similarity.


  
2. **LLM as a Judge (Relevance)**: This evaluation method was split into two distinct processes:
   
   - **AQA (Answer + Question Answer)**: In this approach, the original QA pair along with the LLM-generated answer were passed to another LLM (GPT-4o-mini) to evaluate the relevance of the response.
   - **QA (Question + Answer)**: In this approach, only the question and the LLM-generated answer were passed to the judge, without the original answer, for relevance evaluation.

### LLMs Tested

Various LLMs were tested for both approaches:

- **Cosine Similarity (LLM Eval)**:
  - OpenAI GPT-4o
  - GPT-3.5
  - LLaMA 8B
  - LLaMA 70B

- **LLM as a Judge (Relevance)**: GPT-4o-mini was used to evaluate the relevance of the responses generated by:
  - OpenAI GPT-4o
  - GPT-3.5
  - LLaMA 8B
  - LLaMA 70B

### AQA Evaluation (LLM Answer + Original Question Answer)

| LLM Model       | Relevant (%) | Partially Relevant (%) | Non-Relevant (%) |
|-----------------|--------------|------------------------|------------------|
| GPT-4o AQA      | **81.46**    | 18.23                  | 0.31             |
| GPT-3.5 AQA     | **72.69**    | 25.54                  | 1.77             |
| LLaMA-8B AQA    | **75.92**    | 23.46                  | 0.62             |
| LLaMA-70B AQA   | **75.92**    | 23.69                  | 0.38             |

### QA Evaluation (Original Question + LLM Answer)

| LLM Model       | Relevant (%) | Partially Relevant (%) | Non-Relevant (%) |
|-----------------|--------------|------------------------|------------------|
| GPT-4o QA       | **94.85**    | 4.92                   | 0.23             |
| GPT-3.5 QA      | **89.38**    | 10.31                  | 0.31             |
| LLaMA-8B QA     | **92.85**    | 7.08                   | 0.08             |
| LLaMA-70B QA    | **93.46**    | 6.23                   | 0.31             |

These evaluations were used to assess the performance of different LLMs in terms of how well they generate relevant and accurate answers based on the user’s query.
