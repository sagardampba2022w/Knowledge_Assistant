# llm_module.py

import openai
# Import the Groq client
from groq import Groq  # Replace with the correct import if different

class LLMModule:
    def __init__(self, openai_api_key=None, groq_api_key=None):
        # Initialize OpenAI client if API key is provided
        if openai_api_key:
            openai.api_key = openai_api_key
            self.openai_client_initialized = True
        else:
            self.openai_client_initialized = False

        # Initialize Groq client if API key is provided
        if groq_api_key:
            self.groq_client = Groq(api_key=groq_api_key)
            self.groq_client_initialized = True
        else:
            self.groq_client_initialized = False

    def llm_openai(self, prompt, model='gpt-4o-mini'):
        if not self.openai_client_initialized:
            raise ValueError("OpenAI API key not provided.")

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except openai.error.OpenAIError as e:
            # Handle specific OpenAI errors if needed
            return f"OpenAI API Error: {str(e)}"

    def llm_groq(self, prompt, model='llama70b'):
        if not self.groq_client_initialized:
            raise ValueError("Groq API key not provided.")

        try:
            response = self.groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            # Replace with specific Groq client exceptions if available
            return f"Groq API Error: {str(e)}"

    def llm(self, prompt, model='gpt-4o-mini'):
        # Logic to select LLM based on the model parameter
        if model in ['gpt-3.5-turbo', 'gpt-4', 'gpt-4o-mini']:
            return self.llm_openai(prompt, model=model)
        elif model == 'llama70b':
            return self.llm_groq(prompt, model=model)
        else:
            raise ValueError(f"Model {model} not supported.")
