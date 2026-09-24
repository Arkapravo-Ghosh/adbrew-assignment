from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Todo:
    id: str
    description: str
    created_at: datetime
