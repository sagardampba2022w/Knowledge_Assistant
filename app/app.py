# app.py

import streamlit as st
from elasticsearch_module import ElasticsearchModule
from llm_module import LLMModule
from rag_module import RAGModule
from database_module import initialize_database, save_interaction, update_feedback, Session, UserInteraction
from evaluation_metrics import EvaluationMetrics

# Load environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the database
initialize_database()

# Initialize modules
es_module = ElasticsearchModule()

# Get API keys from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')  # Ensure this is set
groq_api_key = os.getenv('GROQ_API_KEY')      # Ensure this is set

llm_module = LLMModule(openai_api_key=openai_api_key, groq_api_key=groq_api_key)
rag_module = RAGModule(es_module, llm_module)
eval_metrics = EvaluationMetrics()

# Streamlit app
st.title("LLM-based RAG Streamlit App")

# User Input
question = st.text_input("Enter your question:")
model_selected = st.selectbox(
    "Choose an LLM model:",
    ("gpt-4o-mini", "llama70b")  # Updated model options
)

if st.button("Submit"):
    if question:
        with st.spinner('Generating answer...'):
            # Get the answer from the RAG system
            answer, search_results = rag_module.rag(question, model=model_selected)
            st.write("### Answer:")
            st.write(answer)

            # Save the interaction
            interaction_id = save_interaction(question, answer, model_selected)

            # Store interaction ID in session state for feedback
            st.session_state['interaction_id'] = interaction_id
            st.session_state['answer'] = answer
            st.session_state['question'] = question

            # Optionally display retrieved documents
            if st.checkbox("Show retrieved context"):
                for idx, doc in enumerate(search_results):
                    st.write(f"**Document {idx+1}:**")
                    st.write(f"Category: {doc['Category']}")
                    st.write(f"Question: {doc['Question']}")
                    st.write(f"Answer: {doc['Answer']}\n")
    else:
        st.error("Please enter a question.")

# Feedback Mechanism
if 'answer' in st.session_state:
    st.write("### Was this answer helpful?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Yes"):
            update_feedback(st.session_state['interaction_id'], True)
            st.success("Thank you for your feedback!")
            # Clean up session state
            for key in ['interaction_id', 'answer', 'question']:
                st.session_state.pop(key, None)
    with col2:
        if st.button("👎 No"):
            update_feedback(st.session_state['interaction_id'], False)
            st.success("Thank you for your feedback!")
            # Clean up session state
            for key in ['interaction_id', 'answer', 'question']:
                st.session_state.pop(key, None)

# Evaluation Metrics (Admin Section)
if st.sidebar.checkbox("Show Evaluation Metrics"):
    session = Session()
    interactions = session.query(UserInteraction).filter(UserInteraction.feedback != None).all()
    session.close()

    # Prepare relevance data
    relevance_total = [[interaction.feedback] for interaction in interactions]

    # Compute metrics
    hr = eval_metrics.hit_rate(relevance_total)
    mrr_score = eval_metrics.mrr(relevance_total)

    st.sidebar.write(f"**Hit Rate:** {hr:.2f}")
    st.sidebar.write(f"**MRR:** {mrr_score:.2f}")

# Cosine Similarity Evaluation
if st.sidebar.checkbox("Compute Cosine Similarity"):
    # Retrieve ground truth answer from your data source
    # Implement get_ground_truth_answer function
    def get_ground_truth_answer(question):
        # This function should return the ground truth answer for the given question
        # Implement this according to your data source
        return None  # Placeholder

    ground_truth_answer = get_ground_truth_answer(st.session_state.get('question', ''))

    if ground_truth_answer and 'answer' in st.session_state:
        similarity = eval_metrics.compute_similarity(ground_truth_answer, st.session_state['answer'])
        st.sidebar.write(f"**Cosine Similarity:** {similarity:.2f}")
    else:
        st.sidebar.write("Ground truth answer not available or no answer generated yet.")
