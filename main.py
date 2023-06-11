import json
import copy
import logging

from uuid import UUID
from schemas import BaseQuestion, Base, QuestionsList
from service_funcs import get_db, create_question, get_questions_list, delete_question, create_request, send_post, \
    get_questions_ids_from_api, create_questions, get_requests_list, delete_request, get_questions_by_request_id
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends


app = FastAPI(title='Questions_handler')


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=u'[%(asctime)s] - %(message)s')
logger.info("Start service")


@app.post(
    "/questions_num/",
    tags=['Question'],
    description='Main endpoint. Put a number of questions to get. It will store all questions in db and return them as '
                'response.')
async def main(model: Base, db: Session = Depends(get_db)):
    """Main function, receives an incoming request, requests questions from public API, stores and returns questions.

    Arguments: model (incoming data), db (db connetion)
    Incoming request contains data, which form is "{'questions_num': Integer}". Function saves this request
     in db PostgreSQL. According to questions_num function requests a number of questions from public API (f'https://jservice.io/api/random?count={questions_num}').
    In response it receives question/questions, saves it/them in db and returns it/them. Only unique questions can be
    saved in db.
    """
    msg_value = model.questions_num
    new_request = await create_request(
        request=model,
        db=db
    )
    response_json = await send_post(questions_num=msg_value)
    questions_ids_from_api = await get_questions_ids_from_api(db=db)
    if msg_value < 1:
        logger.info("Number of questions is less then 1.")
        return "Number of questions is less then 1."

    elif msg_value == 1:
        # response_json = json.loads(response_json)  # Раскомментировать в случае запуска тестового модуля
        # response_json = json.loads(response_json)  # Раскомментировать в случае запуска тестового модуля
        question_id_from_api = response_json[0]['id']
        if question_id_from_api in questions_ids_from_api:
            while question_id_from_api in questions_ids_from_api:
                response_json = (await send_post(questions_num=msg_value))
                # response_json = json.loads(response_json)  # Раскомментировать в случае запуска тестового модуля
                # response_json = json.loads(response_json)  # Раскомментировать в случае запуска тестового модуля
                question_id_from_api = response_json[0]['id']
        new_question = await create_question(
            db=db,
            question=BaseQuestion(
                question_text=response_json[0]['question'],
                question_answer=response_json[0]['answer'],
                question_id_from_api=question_id_from_api,
                request_id=new_request.id
            )
        )
        json_to_send = {
            'id': str(new_question.question_id_from_api),
            'question_text': new_question.question_text,
            'question_answer': new_question.question_answer,
            'question_date': new_question.question_date.strftime('%Y-%d-%m')
        }
        logger.info(f"1 question is added to db")
        return json.dumps(json_to_send)
    elif msg_value > 1:
        # response_json = json.loads(response_json)  # Раскомментировать в случае запуска тестового модуля
        # response_json = json.loads(response_json)  # Раскомментировать в случае запуска тестового модуля

        final_json_list = copy.deepcopy(response_json)
        response_questions_ids = [i['id'] for i in response_json]
        clones = set(questions_ids_from_api).intersection(set(response_questions_ids))
        if clones:
            # print(len(response_json))
            for i in response_json:
                if i['id'] in questions_ids_from_api:
                    final_json_list.remove(i)
                else:
                    questions_ids_from_api.append(i['id'])
            while clones:
                logger.info(f"len{clones} clones detected")
                new_response_json = await send_post(questions_num=len(clones))
                # new_response_json = json.loads(new_response_json)  # Раскомментировать в случае запуска тестового модуля
                # new_response_json = json.loads(new_response_json)  # Раскомментировать в случае запуска тестового модуля
                new_response_questions_ids = [i['id'] for i in new_response_json]
                clones = set(questions_ids_from_api).intersection(set(new_response_questions_ids))
                if clones:
                    for i in new_response_json:
                        if i['id'] not in questions_ids_from_api:
                            final_json_list.append(i)
                            questions_ids_from_api.append(i['id'])
                else:
                    for i in new_response_json:
                        final_json_list.append(i)
        questions_to_add = [BaseQuestion(
            question_text=item['question'],
            question_answer=item['answer'],
            question_id_from_api=item['id'],
            request_id=new_request.id
        ) for item in final_json_list]
        db_questions = await create_questions(questions=QuestionsList(questions=questions_to_add), db=db)
        json_to_send = [{
            'id': str(new_question.question_id_from_api),
            'question_text': new_question.question_text,
            'question_answer': new_question.question_answer,
            'question_date': new_question.question_date.strftime('%Y-%d-%m')
        } for new_question in db_questions]
        logger.info(f"{len(json_to_send)} questions are added to db")
        # return json.dumps(json_to_send)
        return json_to_send


@app.get(
    "/request/",
    tags=['Request'],
    description='Endpoint to get all requests.')
async def get_requests(db: Session = Depends(get_db)):
    """This function requests and returns all instances of request table from db. It receives a db connection."""
    return await get_requests_list(db=db)


@app.delete(
    "/request/{request_id}/",
    tags=['Request'],
    description='Endpoint to delete some request by id.')
async def delete_request_by_id(request_id: UUID, db: Session = Depends(get_db)):
    """This function deletes request from db. Arguments: request id, db. It returns a confirmation string."""
    return await delete_request(
        request_id=request_id,
        db=db)


@app.get(
    "/questions/",
    tags=['Question'],
    description='Endpoint to get questions.')
async def get_questions(db: Session = Depends(get_db)):
    """This function requests and returns all instances of question table from db. It receives a db connection"""
    return await get_questions_list(db=db)


@app.get(
    "/questions_by_request/{request_id}/",
    tags=['Question'],
    description='Endpoint to get questions by request id.')
async def get_questions_by_request(request_id: UUID, db: Session = Depends(get_db)):
    """This function requests and returns instances of question table according to request.
    It receives a request id and db connection."""
    return await get_questions_by_request_id(
        request_id=request_id,
        db=db)


@app.delete(
    "/question/{question_id}/",
    tags=['Question'],
    description='Endpoint to delete some question by id.')
async def delete_question_by_id(question_id: UUID, db: Session = Depends(get_db)):
    """This function deletes questions from db. It receives question id and db connection,
     it returns a confirmation string."""
    return await delete_question(
        question_id=question_id,
        db=db)
