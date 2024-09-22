# database_module.py

from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
import os
DATABASE_URI = os.getenv('DATABASE_URI')  # Use environment variable for security

engine = create_engine(DATABASE_URI)
Base = declarative_base()

class UserInteraction(Base):
    __tablename__ = 'user_interactions'
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    llm_response = Column(Text)
    model_used = Column(String)
    feedback = Column(Boolean)  # True for positive, False for negative

def initialize_database():
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def save_interaction(question, llm_response, model_used):
    session = Session()
    interaction = UserInteraction(
        question=question,
        llm_response=llm_response,
        model_used=model_used
    )
    session.add(interaction)
    session.commit()
    interaction_id = interaction.id
    session.close()
    return interaction_id

def update_feedback(interaction_id, feedback):
    session = Session()
    interaction = session.query(UserInteraction).get(interaction_id)
    interaction.feedback = feedback
    session.commit()
    session.close()
