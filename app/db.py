import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from psycopg2 import pool
from psycopg2.extras import DictCursor

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Timezone
tz = ZoneInfo("Europe/Berlin")

# Database connection pool
db_pool = pool.SimpleConnectionPool(
    1, 20,
    host=os.getenv("POSTGRES_HOST", "postgres"),
    database=os.getenv("POSTGRES_DB", "research_assistant"),
    user=os.getenv("POSTGRES_USER", "your_username"),
    password=os.getenv("POSTGRES_PASSWORD", "your_password"),
)

def get_db_connection():
    return db_pool.getconn()

def release_db_connection(conn):
    db_pool.putconn(conn)

def init_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS feedback")
            cur.execute("DROP TABLE IF EXISTS conversations")
            cur.execute("""
                CREATE TABLE conversations (
                    id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    model_used TEXT NOT NULL,
                    response_time FLOAT NOT NULL,
                    relevance TEXT NOT NULL,
                    relevance_explanation TEXT NOT NULL,
                    prompt_tokens INTEGER NOT NULL,
                    completion_tokens INTEGER NOT NULL,
                    total_tokens INTEGER NOT NULL,
                    eval_prompt_tokens INTEGER NOT NULL,
                    eval_completion_tokens INTEGER NOT NULL,
                    eval_total_tokens INTEGER NOT NULL,
                    openai_cost FLOAT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE feedback (
                    id SERIAL PRIMARY KEY,
                    conversation_id TEXT REFERENCES conversations(id),
                    feedback INTEGER NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        release_db_connection(conn)

def save_conversation(conversation_id, question, answer_data, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(tz)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO conversations 
                (id, question, answer, model_used, response_time, relevance, 
                relevance_explanation, prompt_tokens, completion_tokens, total_tokens, 
                eval_prompt_tokens, eval_completion_tokens, eval_total_tokens, openai_cost, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    conversation_id,
                    question,
                    answer_data["answer"],
                    answer_data["model_used"],
                    answer_data["response_time"],
                    answer_data["relevance"],
                    answer_data["relevance_explanation"],
                    answer_data["prompt_tokens"],
                    answer_data["completion_tokens"],
                    answer_data["total_tokens"],
                    answer_data["eval_prompt_tokens"],
                    answer_data["eval_completion_tokens"],
                    answer_data["eval_total_tokens"],
                    answer_data["openai_cost"],
                    timestamp,
                ),
            )
        conn.commit()
    except Exception as e:
        logger.error(f"Error saving conversation: {e}")
    finally:
        release_db_connection(conn)

# def save_feedback(conversation_id, feedback, timestamp=None):
#     if timestamp is None:
#         timestamp = datetime.now(tz)
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cur:
#             cur.execute(
#                 """
#                 INSERT INTO feedback (conversation_id, feedback, timestamp)
#                 VALUES (%s, %s, %s)
#                 """,
#                 (conversation_id, feedback, timestamp),
#             )
#         conn.commit()
#     except Exception as e:
#         logger.error(f"Error saving feedback: {e}")
#     finally:
#         release_db_connection(conn)


def save_feedback(conversation_id, feedback, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(tz)
    conn = get_db_connection()
    try:
        logger.info(f"Checking if conversation {conversation_id} exists before saving feedback.")
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT EXISTS (
                    SELECT 1 
                    FROM conversations 
                    WHERE id = %s
                )
                """, (conversation_id,)
            )
            exists = cur.fetchone()[0]
            if exists:
                cur.execute(
                    """
                    INSERT INTO feedback (conversation_id, feedback, timestamp)
                    VALUES (%s, %s, %s)
                    """,
                    (conversation_id, feedback, timestamp),
                )
                conn.commit()
                logger.info(f"Feedback saved successfully for conversation {conversation_id}")
            else:
                logger.error(f"Conversation ID {conversation_id} does not exist. Feedback not saved.")
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
    finally:
        release_db_connection(conn)


def get_recent_conversations(limit=5, relevance=None):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            query = """
                SELECT c.*, f.feedback
                FROM conversations c
                LEFT JOIN feedback f ON c.id = f.conversation_id
            """
            params = []
            if relevance:
                query += " WHERE c.relevance = %s"
                params.append(relevance)
            query += " ORDER BY c.timestamp DESC LIMIT %s"
            params.append(limit)
            cur.execute(query, params)
            return cur.fetchall()
    except Exception as e:
        logger.error(f"Error fetching recent conversations: {e}")
        return []
    finally:
        release_db_connection(conn)

def get_feedback_stats():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT 
                    SUM(CASE WHEN feedback > 0 THEN 1 ELSE 0 END) as thumbs_up,
                    SUM(CASE WHEN feedback < 0 THEN 1 ELSE 0 END) as thumbs_down
                FROM feedback
            """)
            result = cur.fetchone()
            return {
                'thumbs_up': result['thumbs_up'] or 0,
                'thumbs_down': result['thumbs_down'] or 0
            }
    except Exception as e:
        logger.error(f"Error fetching feedback stats: {e}")
        return {'thumbs_up': 0, 'thumbs_down': 0}
    finally:
        release_db_connection(conn)
