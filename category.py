import uuid
from uuid import UUID

class Category:
    def __init__(
            self,
            name: str,
            description: str = "",
            is_active: bool = True,
            id = "",
    ):
        self.id = id or uuid.uuid4()
        self.name = name
        self.description = description
        self.is_active = is_active

    def __str__(self):
        return f"Category(id={self.id}, name={self.name}, description={self.description}, is_active={self.is_active})"
    
    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, description={self.description}, is_active={self.is_active})"