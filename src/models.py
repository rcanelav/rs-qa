from pydantic import BaseModel, Field, field_validator


class QuestionAnswerRequest(BaseModel):
    """Checks request payload for later processing

    Args:
        BaseModel (BaseModel): Pydantic's BaseModel class.
    """
    question: str = Field(..., title="Question",
                          description="Question to be answered")

    @field_validator("question")
    def check_question(cls, value):
        if not value.strip():
            raise ValueError("Question cannot be empty")
        return value
