# evaluation_metrics.py

import numpy as np
from sentence_transformers import SentenceTransformer

class EvaluationMetrics:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your desired model

    def hit_rate(self, relevance_total):
        return sum(1 for line in relevance_total if True in line) / len(relevance_total)

    def mrr(self, relevance_total):
        total_score = 0.0
        for line in relevance_total:
            for rank, is_relevant in enumerate(line):
                if is_relevant:
                    total_score += 1 / (rank + 1)
                    break
        return total_score / len(relevance_total)

    def compute_similarity(self, answer_orig, answer_llm):
        v_llm = self.model.encode(answer_llm)
        v_orig = self.model.encode(answer_orig)
        cosine_similarity = np.dot(v_llm, v_orig) / (np.linalg.norm(v_llm) * np.linalg.norm(v_orig))
        return cosine_similarity
