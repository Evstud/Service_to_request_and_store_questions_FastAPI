import datetime
import uuid

from sqlalchemy import Column, Table, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, DATE
from sqlalchemy.orm import relationship
from db import Base, engine


class Request(Base):
    __tablename__ = 'request'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    questions_num = Column(Integer)
    question = relationship('Question', back_populates='request', cascade="all, delete")


class Question(Base):
    __tablename__ = 'question'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_text = Column(String, unique=True)
    question_answer = Column(String)
    question_date = Column(DATE, default=datetime.datetime.now())
    question_id_from_api = Column(Integer)
    request_id = Column(UUID(as_uuid=True), ForeignKey('request.id'))
    request = relationship('Request', back_populates='question')


Base.metadata.create_all(bind=engine)
