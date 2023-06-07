import json
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title='question_base_module')


class Base(BaseModel):
    questions_num: int


@app.get("/give_me_questions/{num}/")
async def main(num: int):
    data_to_send = input(f"Give me {num} questions.\n")
    return json.dumps(data_to_send)
