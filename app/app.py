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
    "gpt-4o-mini",
    "llama3-70b-8192",
    "llama3-8b-8192"
    #"llama-3.1-70b-versatile",
    #"mixtral-8x7b-32768"	
]

def initialize_session_state():
    if 'current_conversation_id' not in st.session_state:
        st.session_state['current_conversation_id'] = str(uuid.uuid4())
        logger.info(f"Initialized current_conversation_id: {st.session_state['current_conversation_id']}")
    if 'last_conversation_id' not in st.session_state:
        st.session_state['last_conversation_id'] = None
        logger.info("Initialized last_conversation_id to None")
    if 'feedback_given' not in st.session_state:
        st.session_state['feedback_given'] = {}  # Track feedback per conversation
        logger.info("Initialized feedback_given as empty dictionary")
    if 'last_question' not in st.session_state:
        st.session_state['last_question'] = ""
    if 'last_answer' not in st.session_state:
        st.session_state['last_answer'] = None

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
    if conversation_id and not st.session_state['feedback_given'].get(conversation_id):
        st.subheader("Provide Feedback")
        feedback_button_col1, feedback_button_col2 = st.columns(2)

        with feedback_button_col1:
            if st.button("👍", key=f"thumbsup_{conversation_id}"):
                try:
                    save_feedback(conversation_id, 1)
                    st.session_state['feedback_given'][conversation_id] = True
                    st.success("Thank you for your positive feedback!")
                    logger.info(f"Positive feedback saved for conversation {conversation_id}")
                except Exception as e:
                    logger.error(f"Error saving positive feedback: {e}")
                    st.error("An error occurred while saving your feedback.")

        with feedback_button_col2:
            if st.button("👎", key=f"thumbsdown_{conversation_id}"):
                try:
                    save_feedback(conversation_id, -1)
                    st.session_state['feedback_given'][conversation_id] = True
                    st.warning("Thank you for your feedback!")
                    logger.info(f"Negative feedback saved for conversation {conversation_id}")
                except Exception as e:
                    logger.error(f"Error saving negative feedback: {e}")
                    st.error("An error occurred while saving your feedback.")
    elif conversation_id:
        st.write("Feedback already submitted. Thank you!")

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
    logger.info("Starting the application")
    st.title("Research Knowledge Assistant")

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
                
                # Display answer
                display_answer(answer_data)
                
                # Save conversation to database
                conversation_id = st.session_state['current_conversation_id']
                logger.info(f"Saving conversation {conversation_id} to database")
                save_conversation(conversation_id, user_input, answer_data)
                st.session_state['last_question'] = user_input
                st.session_state['last_answer'] = answer_data
                st.session_state['last_conversation_id'] = conversation_id
                logger.info("Conversation saved successfully")

                # Prompt feedback immediately after displaying the answer
                handle_feedback(st.session_state['last_conversation_id'])

                # Prepare for the next conversation
                st.session_state['current_conversation_id'] = str(uuid.uuid4())
                logger.info(f"Generated new current_conversation_id: {st.session_state['current_conversation_id']}")

            except Exception as e:
                logger.error(f"Error getting answer: {e}")
                st.error("An error occurred while processing your request.")
                return

    # Display feedback for the last conversation if available
    if st.session_state.get('last_conversation_id') and not submit_button:
        st.subheader("Last Question:")
        st.write(st.session_state['last_question'])
        st.subheader("Answer:")
        display_answer(st.session_state['last_answer'])

        # Handle feedback for the last conversation
        handle_feedback(st.session_state['last_conversation_id'])

    # Display recent conversations
    display_recent_conversations()

    # Display feedback statistics
    display_feedback_stats()

if __name__ == "__main__":
    main()
