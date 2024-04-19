from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(description="Name of the item.")
    shelf: int = Field(description="Availability of the item.")
    lab: str = Field(description="Lab this item belongs to.")
    count: int = Field(description="Amount of instances of this item in stock.")
    category: str = Field(description="Category this item belongs to.")
    expiration_date: str = Field(description="Expiration date of this item.")
 