# rag_module.py

from elastic import ElasticsearchModule
from llm import LLMModule
from prompt import build_prompt

class RAGModule:
    def __init__(self, es_module: ElasticsearchModule, llm_module: LLMModule):
        self.es_module = es_module
        self.llm_module = llm_module

    def rag(self, query_text, model='gpt-4o-mini'):
        search_results = self.es_module.question_text_hybrid_rrf(query_text)
        prompt = build_prompt(query_text, search_results)
        answer = self.llm_module.llm(prompt, model=model)
        return answer, search_results
