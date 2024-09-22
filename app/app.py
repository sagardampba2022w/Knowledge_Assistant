import uuid
import time
import logging

import streamlit as st

from assistant import get_answer
from db import (
    save_conversation,
    save_feedback,
    get_recent_conversations,
    get_feedback_stats,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MODEL_OPTIONS = [
    "gpt-3.5-turbo",
    "gpt-4o-mini",
    "llama3-70b-8192",
    # Add other models if needed
]

def initialize_session_state():
    st.session_state.setdefault('conversation_id', str(uuid.uuid4()))
    st.session_state.setdefault('count', 0)

def get_user_input():
    with st.form(key='question_form'):
        model_choice = st.selectbox("Select a model:", MODEL_OPTIONS)
        search_type = st.radio("Select search type:", ["Text", "Vector"])
        user_input = st.text_input("Enter your question:")
        submit_button = st.form_submit_button(label='Ask')
    return model_choice, search_type, user_input, submit_button

def display_answer(answer_data):
    st.success("Completed!")
    st.write(answer_data["answer"])
    # Display monitoring information
    st.write(f"Response time: {answer_data['response_time']:.2f} seconds")
    st.write(f"Relevance: {answer_data['relevance']}")
    st.write(f"Model used: {answer_data['model_used']}")
    st.write(f"Total tokens: {answer_data['total_tokens']}")
    if answer_data["openai_cost"] > 0:
        st.write(f"OpenAI cost: ${answer_data['openai_cost']:.4f}")

def handle_feedback(conversation_id):
    feedback = st.radio("Was this answer helpful?", ("Yes", "No"))
    if feedback:
        feedback_value = 1 if feedback == "Yes" else -1
        save_feedback(conversation_id, feedback_value)
        st.success("Thank you for your feedback!")

def display_recent_conversations():
    with st.expander("Recent Conversations"):
        relevance_filter = st.selectbox(
            "Filter by relevance:", ["All", "RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"]
        )
        recent_conversations = get_recent_conversations(
            limit=5, relevance=relevance_filter if relevance_filter != "All" else None
        )
        for conv in recent_conversations:
            st.write(f"Q: {conv['question']}")
            st.write(f"A: {conv['answer']}")
            st.write(f"Relevance: {conv['relevance']}")
            st.write(f"Model: {conv['model_used']}")
            st.write("---")

def display_feedback_stats():
    feedback_stats = get_feedback_stats()
    st.subheader("Feedback Statistics")
    st.write(f"Thumbs up: {feedback_stats['thumbs_up']}")
    st.write(f"Thumbs down: {feedback_stats['thumbs_down']}")

def main():
    logger.info("Starting the Course Assistant application")
    st.title("Course Assistant")

    # Initialize session state
    initialize_session_state()

    # Get user input
    model_choice, search_type, user_input, submit_button = get_user_input()

    if submit_button and user_input:
        logger.info(f"User asked: '{user_input}'")
        with st.spinner("Processing..."):
            try:
                logger.info(f"Getting answer from assistant using {model_choice} model and {search_type} search")
                start_time = time.time()
                answer_data = get_answer(user_input, model_choice, search_type)
                end_time = time.time()
                logger.info(f"Answer received in {end_time - start_time:.2f} seconds")
                display_answer(answer_data)
                # Save conversation to database
                logger.info("Saving conversation to database")
                save_conversation(
                    st.session_state.conversation_id, user_input, answer_data
                )
                logger.info("Conversation saved successfully")
                # Generate a new conversation ID for next question
                st.session_state.conversation_id = str(uuid.uuid4())
            except Exception as e:
                logger.error(f"Error getting answer: {e}")
                st.error("An error occurred while processing your request.")
                return

        # Handle feedback
        handle_feedback(st.session_state.conversation_id)

    # Display recent conversations
    display_recent_conversations()

    # Display feedback statistics
    display_feedback_stats()

if __name__ == "__main__":
    main()
