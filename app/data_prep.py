import os
import logging
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm
from dotenv import load_dotenv

from db import init_db

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ELASTIC_URL = os.getenv("ELASTIC_URL_LOCAL", "http://localhost:9200")
MODEL_NAME = os.getenv("MODEL_NAME", "multi-qa-MiniLM-L6-cos-v1")
INDEX_NAME = "insights-questions"  # Updated index name

def fetch_documents():
    logger.info("Fetching documents...")
    # Replace this with your actual document loading logic
    documents = []  # Load your documents here
    logger.info(f"Fetched {len(documents)} documents")
    return documents

def load_model():
    logger.info(f"Loading model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)

def setup_elasticsearch():
    logger.info("Setting up Elasticsearch...")
    es_client = Elasticsearch(ELASTIC_URL)

    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "Answer": {"type": "text"},
                "Category": {"type": "text"},
                "Question": {"type": "text"},
                "doc_id": {"type": "keyword"},
                "question_vector": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
                "text_vector": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
                "question_text_vector": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
            }
        }
    }

    es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    es_client.indices.create(index=INDEX_NAME, body=index_settings)
    logger.info(f"Elasticsearch index '{INDEX_NAME}' created")
    return es_client

def index_documents(es_client, documents, model):
    logger.info("Indexing documents...")
    for doc in tqdm(documents):
        question = doc['Question']
        text = doc['Answer']
        qt = question + ' ' + text

        doc['question_vector'] = model.encode(question).tolist()
        doc['text_vector'] = model.encode(text).tolist()
        doc['question_text_vector'] = model.encode(qt).tolist()
        es_client.index(index=INDEX_NAME, document=doc)
    logger.info(f"Indexed {len(documents)} documents")

def main():
    logger.info("Starting the indexing process...")

    documents = fetch_documents()
    if not documents:
        logger.error("No documents fetched. Exiting.")
        return

    model = load_model()
    es_client = setup_elasticsearch()
    index_documents(es_client, documents, model)

    logger.info("Initializing database...")
    init_db()

    logger.info("Indexing process completed successfully!")

if __name__ == "__main__":
    main()
