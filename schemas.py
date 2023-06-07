from pydantic import BaseModel
from uuid import UUID
from typing import List


class Base(BaseModel):
    questions_num: int


class BaseQuestion(BaseModel):
    question_text: str
    question_answer: str
    question_id_from_api: int
    request_id: UUID

    class Config:
        orm_mode = True


class QuestionsList(BaseModel):
    questions: List[BaseQuestion]
