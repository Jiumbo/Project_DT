from pydantic import BaseModel


class Table(BaseModel):
    tableId: str | int
    activeEntries: int
    packetsLookedUp: int
    packetsMatched: int
