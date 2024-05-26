from pydantic import BaseModel


class Criteria(BaseModel):
    type: str
    ethType: str
