from sqlalchemy import Column, Integer, ForeignKey, String
from models import Base


class ExtrasTopics(Base):
    __tablename__ = 'extras_topics'
    id = Column(Integer, primary_key=True)
    extras_id = Column(Integer, ForeignKey('extras.id'), nullable=False)
    topic_name = Column(String, ForeignKey('topics.name'), nullable=False)


