import os
import time
import json
import logging

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from groq import Groq  # Assuming there's a 'groq' Python package available

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


# Path to Docker secrets
openai_api_key_path = '/run/secrets/openai_api_key'
groq_api_key_path = '/run/secrets/groq_api_key'

# Initialize OpenAI and Groq API keys from Docker secrets or environment variables
try:
    with open(openai_api_key_path, 'r') as file:
        OPENAI_API_KEY = file.read().strip()
    logger.info("Loaded OpenAI API key from Docker secret.")
except FileNotFoundError:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
    logger.warning("OpenAI API key file not found. Using environment variable instead.")

try:
    with open(groq_api_key_path, 'r') as file:
        GROQ_API_KEY = file.read().strip()
    logger.info("Loaded Groq API key from Docker secret.")
except FileNotFoundError:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key")
    logger.warning("Groq API key file not found. Using environment variable instead.")


# Constants
COST_RATES = {
    'gpt-4o-mini': {'prompt': 0.03, 'completion': 0.06},
    'gpt-3.5-turbo': {'prompt': 0.0015, 'completion': 0.002},
    # Add other OpenAI models and their rates here
}

ELASTIC_URL = os.getenv("ELASTIC_URL", "http://localhost:9200")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key")

# Initialize Elasticsearch client
es_client = Elasticsearch(ELASTIC_URL)

# Initialize OpenAI client
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
openai_client = OpenAI()

# Initialize Groq client
client_groq = Groq(api_key=GROQ_API_KEY)

# Load the SentenceTransformer model
model_name = 'multi-qa-MiniLM-L6-cos-v1'
model = SentenceTransformer(model_name)

# Elasticsearch index name
INDEX_NAME = "insights-questions"

def llm(prompt, model_choice):
    start_time = time.time()
    if model_choice in ['gpt-4o-mini']:  # OpenAI models
        response = openai_client.chat.completions.create(
            model=model_choice,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        tokens = {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
            'total_tokens': response.usage.total_tokens
        }
    else:  # Use Groq client for other models
        response = client_groq.chat.completions.create(
            model=model_choice,  # e.g., 'llama3-70b-8192'
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        # Assuming Groq API provides token usage information
        tokens = {
            'prompt_tokens': response.usage.get('prompt_tokens', 0),
            'completion_tokens': response.usage.get('completion_tokens', 0),
            'total_tokens': response.usage.get('total_tokens', 0)
        }
    end_time = time.time()
    response_time = end_time - start_time
    return answer, tokens, response_time

def build_prompt(query, search_results):
    context = "\n\n".join(
        f"Category: {doc.get('Category', '')}\nQuestion: {doc.get('Question', '')}\nAnswer: {doc.get('Answer', '')}"
        for doc in search_results
    )
    prompt = f"""
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {query}

CONTEXT:
{context}
""".strip()
    return prompt

def compute_rrf(rank, k=60):
    """Compute Reciprocal Rank Fusion score."""
    return 1 / (k + rank)

def elastic_search_hybrid_rrf(field, query, vector, k=60):
    # KNN Query
    knn_query = {
        "field": field,
        "query_vector": vector,
        "k": 10,
        "num_candidates": 10000,
        "boost": 0.5
    }

    # Keyword Query
    keyword_query = {
        "bool": {
            "must": {
                "multi_match": {
                    "query": query,
                    "fields": ["Question", "Answer", "Category"],
                    "type": "best_fields",
                    "boost": 0.5
                }
            }
        }
    }

    # KNN Search
    knn_results = es_client.search(
        index=INDEX_NAME,
        body={
            "knn": knn_query,
            "size": 10
        }
    )['hits']['hits']

    # Keyword Search
    keyword_results = es_client.search(
        index=INDEX_NAME,
        body={
            "query": keyword_query,
            "size": 10
        }
    )['hits']['hits']

    # Reciprocal Rank Fusion (RRF) scoring
    rrf_scores = {}

    # Calculate RRF scores for KNN results
    for rank, hit in enumerate(knn_results):
        doc_id = hit['_id']
        rrf_scores[doc_id] = compute_rrf(rank + 1, k)

    # Calculate RRF scores for keyword results
    for rank, hit in enumerate(keyword_results):
        doc_id = hit['_id']
        if doc_id in rrf_scores:
            rrf_scores[doc_id] += compute_rrf(rank + 1, k)
        else:
            rrf_scores[doc_id] = compute_rrf(rank + 1, k)

    # Sort RRF scores in descending order
    reranked_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    # Get top-K documents by the score
    final_results = []
    for doc_id, score in reranked_docs[:5]:
        doc = es_client.get(index=INDEX_NAME, id=doc_id)
        final_results.append(doc['_source'])

    return final_results

def search_elasticsearch(query, search_type):
    if search_type == 'Vector':
        vector = model.encode(query)
        search_results = elastic_search_hybrid_rrf('question_text_vector', query, vector)
    else:
        # For 'Text' search, use keyword search only
        keyword_query = {
            "size": 5,
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": query,
                            "fields": ["Question^3", "Answer", "Category"],
                            "type": "best_fields",
                        }
                    }
                },
            }
        }
        response = es_client.search(index=INDEX_NAME, body=keyword_query)
        search_results = [hit["_source"] for hit in response["hits"]["hits"]]
    return search_results

def evaluate_relevance(question, answer):
    prompt = f"""
You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()
    # Using OpenAI's GPT-4o-mini for evaluation
    evaluation, tokens, _ = llm(prompt, 'gpt-4o-mini')
    try:
        json_eval = json.loads(evaluation)
        relevance = json_eval.get('Relevance', 'UNKNOWN')
        explanation = json_eval.get('Explanation', 'No explanation provided.')
    except json.JSONDecodeError:
        relevance = "UNKNOWN"
        explanation = "Failed to parse evaluation"
    return relevance, explanation, tokens

def calculate_openai_cost(model_choice, tokens):
    cost = 0
    rates = COST_RATES.get(model_choice)
    if rates:
        cost = (tokens['prompt_tokens'] * rates['prompt'] + tokens['completion_tokens'] * rates['completion']) / 1000
    return cost

def get_answer(query, model_choice, search_type):
    search_results = search_elasticsearch(query, search_type)
    prompt = build_prompt(query, search_results)
    answer, tokens, response_time = llm(prompt, model_choice)
    relevance, explanation, eval_tokens = evaluate_relevance(query, answer)
    openai_cost = calculate_openai_cost(model_choice, tokens)
    return {
        'answer': answer,
        'response_time': response_time,
        'relevance': relevance,
        'relevance_explanation': explanation,
        'model_used': model_choice,
        'prompt_tokens': tokens.get('prompt_tokens', 0),
        'completion_tokens': tokens.get('completion_tokens', 0),
        'total_tokens': tokens.get('total_tokens', 0),
        'eval_prompt_tokens': eval_tokens.get('prompt_tokens', 0),
        'eval_completion_tokens': eval_tokens.get('completion_tokens', 0),
        'eval_total_tokens': eval_tokens.get('total_tokens', 0),
        'openai_cost': openai_cost
    }
