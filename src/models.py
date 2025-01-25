from pydantic import BaseModel


class QuestionAnswerRequest(BaseModel):
    """Checks request payload for later processing

    Args:
        BaseModel (BaseModel): Pydantic's BaseModel class.
    """
    question: str
