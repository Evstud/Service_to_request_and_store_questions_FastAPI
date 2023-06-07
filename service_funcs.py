import aiohttp

from db import SessionLocal
from models import Question, Request
from schemas import BaseQuestion, Base, QuestionsList
from sqlalchemy.orm import Session
from uuid import UUID


# Create a session to access the db
def get_db():
    """This function creates a session to access the db."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create_request
async def create_request(
        request: Base,
        db: Session):
    """This function creates an instance in Request table."""

    db_request = Request(
        questions_num=request.questions_num
    )
    db.add(db_request)
    db.commit()
    return db_request


# Get_request
async def get_requests_list(
        db: Session):
    """This function requests and returns all requests from db."""
    db_requests = db.query(Request).all()
    return db_requests


# Delete_request
async def delete_request(
        request_id: UUID,
        db: Session):
    """This function deletes some instance of Request table by request id."""
    request_to_delete = db.query(Request).filter(Request.id == request_id).first()
    db.delete(request_to_delete)
    db.commit()
    return f"Request '{request_id}' deleted."


# Create question
async def create_question(
        question: BaseQuestion,
        db: Session):
    """This function creates and returns an instance of Question table."""
    db_question = Question(
        question_text=question.question_text,
        question_answer=question.question_answer,
        question_id_from_api=question.question_id_from_api,
        request_id=question.request_id
    )
    db.add(db_question)
    db.commit()
    # print(db_question)
    return db_question


# Create questions
async def create_questions(
        questions: QuestionsList,
        db: Session):
    """This function creates and returns several intances of Question table simultaneously."""
    db_questions = [Question(
        question_text=question.question_text,
        question_answer=question.question_answer,
        question_id_from_api=question.question_id_from_api,
        request_id=question.request_id
    ) for question in questions.questions]
    db.add_all(db_questions)
    db.commit()
    return db_questions


# Get questions
async def get_questions_list(
        db: Session):
    """This function requests and returns all instances of Question table from db."""
    db_questions = db.query(Question).all()
    return db_questions


# Get questions by request_id
async def get_questions_by_request_id(
        request_id: UUID,
        db: Session):
    """This function requests and returns instances of Question table which are binded
    with a Request instance. Arguments: request id and db."""
    db_questions = db.query(Question).filter(Question.request_id == request_id).all()
    return db_questions


async def get_questions_ids_from_api(
        db: Session):
    """This function returns all values from field ids_from_api of Question table instances."""
    db_questions_from_api = db.query(Question).all()
    id_list = [it.question_id_from_api for it in db_questions_from_api]
    return id_list


# Delete question
async def delete_question(
        question_id: UUID,
        db: Session):
    """This function deletes a Question table instance by id"""
    question_to_delete = db.query(Question).filter(Question.id == question_id).first()
    db.delete(question_to_delete)
    db.commit()
    return f"Question '{question_id}' deleted"


async def send_post(questions_num):
    """This function sends a request to public API ('https://jservice.io/api/') and returns questions"""
    url = f'https://jservice.io/api/random?count={questions_num}'
    # url = f'http://127.0.0.1:8002/give_me_questions/{questions_num}/'
    headers = {'Content-Type': 'applicaction/json'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            return await response.json()

