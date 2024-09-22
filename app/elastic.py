# elasticsearch_module.py

from elasticsearch import Elasticsearch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

class ElasticsearchModule:
    def __init__(self, index_name='insights-questions', es_host='http://localhost:9200'):
        self.es_client = Elasticsearch(es_host)
        self.index_name = index_name
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your desired model

        # Check if the index exists; if not, create it
        if not self.es_client.indices.exists(index=self.index_name):
            self.create_index()
            # Load and index documents
            documents = self.load_documents()  # Implement or import this function
            self.index_documents(documents)

    def create_index(self):
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

        # Create the index
        self.es_client.indices.create(index=self.index_name, body=index_settings)

    def index_documents(self, documents):
        for doc in tqdm(documents):
            question = doc['Question']
            text = doc['Answer']
            qt = question + ' ' + text

            doc['question_vector'] = self.model.encode(question).tolist()
            doc['text_vector'] = self.model.encode(text).tolist()
            doc['question_text_vector'] = self.model.encode(qt).tolist()

            self.es_client.index(index=self.index_name, document=doc)

    def compute_rrf(self, rank, k=60):
        """Reciprocal Rank Fusion scoring."""
        return 1 / (k + rank)

    def elastic_search_hybrid_rrf(self, field, query, vector, k=60):
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

        # Execute KNN Search
        knn_results = self.es_client.search(
            index=self.index_name, 
            body={"knn": knn_query, "size": 10}
        )['hits']['hits']

        # Execute Keyword Search
        keyword_results = self.es_client.search(
            index=self.index_name, 
            body={"query": keyword_query, "size": 10}
        )['hits']['hits']

        # RRF Scoring
        rrf_scores = {}
        for rank, hit in enumerate(knn_results):
            doc_id = hit['_id']
            rrf_scores[doc_id] = self.compute_rrf(rank + 1, k)

        for rank, hit in enumerate(keyword_results):
            doc_id = hit['_id']
            if doc_id in rrf_scores:
                rrf_scores[doc_id] += self.compute_rrf(rank + 1, k)
            else:
                rrf_scores[doc_id] = self.compute_rrf(rank + 1, k)

        # Sort and retrieve top results
        reranked_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        final_results = []
        for doc_id, score in reranked_docs[:5]:
            doc = self.es_client.get(index=self.index_name, id=doc_id)
            final_results.append(doc['_source'])

        return final_results

    def question_text_hybrid_rrf(self, query_text):
        vector = self.model.encode(query_text).tolist()
        return self.elastic_search_hybrid_rrf('question_text_vector', query_text, vector)

    def load_documents(self):
        # Implement this method to load your documents
        # For example, read from a JSON file, database, or API
        # Return a list of documents, where each document is a dictionary
        # with keys: 'Question', 'Answer', 'Category', 'doc_id' (optional)
        documents = []
        # Your code to populate the documents list
        return documents
