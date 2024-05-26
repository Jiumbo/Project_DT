from pydantic import BaseModel


class Thread(BaseModel):
    live: int
    daemon: int
    peak: int
