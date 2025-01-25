from pydantic import BaseModel


class QuestionAnswerRequest(BaseModel):
    question: str
