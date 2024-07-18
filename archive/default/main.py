# to run "uvicorn main:app --reload"

from enum import Enum

from pydantic import BaseModel, Field

from fastapi import FastAPI, HTTPException, Path, Query

# You can give your API a title and add additional metadata such as a description, version number, etc.
# The description also supports markdown formatting.
app = FastAPI(
    title="LabTrack",
    description="LabTrack helps you keep track of **lab equipments and chemicals.**",
    version="0.1.0",
)

# Docstrings of classes will be reflected in the API documentation in the 'Schemas' section
class Category(Enum):
    """Category of an item"""

    EQUIPMENTS = "equipments"
    CHEMICALS = "chemicals"


# You can add metadata to attributes using the Field class.
# This information will also be shown in the auto-generated documentation.
class Item(BaseModel):
    """Representation of an item in the system."""

    name: str = Field(description="Name of the item.")
    shelf: int = Field(description="Availability of the item.")
    lab: str = Field(description="Lab this item belongs to.")
    count: int = Field(description="Amount of instances of this item in stock.")
    id: int = Field(description="Unique integer that specifies this item.")
    category: Category = Field(description="Category this item belongs to.")
    expiration_date: str = Field(description="Expiration date of this item.")
    
    


items = {
    0: Item(name="Beaker", shelf=9, count=20, id=0, category=Category.EQUIPMENTS, expiration_date="2022-10-10", lab="Lab 1"),
    1: Item(name="Test Tube", shelf=5, count=20, id=1, category=Category.EQUIPMENTS, expiration_date="2022-10-10", lab="Lab 2"),
    2: Item(name="Ethanol", shelf=1, count=100, id=2, category=Category.CHEMICALS, expiration_date="2022-10-10", lab="Lab 3"),
}


@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}

@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")

    return items[item_id]


Selection = dict[
    str, str | int | int | Category | None
]  # dictionary containing the user's query arguments


@app.get("/items/")
def query_item_by_parameters(
    name: str | None = None,
    shelf: int | None = None,
    count: int | None = None,
    category: Category | None = None,
) -> dict[str, Selection | list[Item]]:
    def check_item(item: Item):
        """Check if the item matches the query arguments from the outer scope."""
        return all(
            (
                name is None or item.name == name,
                shelf is None or item.shelf == shelf,
                count is None or item.count != count,
                category is None or item.category is category,
            )
        )

    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "shelf": shelf, "count": count, "category": category},
        "selection": selection,
    }


@app.post("/")
def add_item(item: Item) -> dict[str, Item]:
    if item.id in items:
        HTTPException(status_code=400, detail=f"Item with {item.id=} already exists.")

    items[item.id] = item
    return {"added": item}


# The 'responses' keyword allows you to specify which responses a user can expect from this endpoint.
@app.put(
    "/update/{item_id}",
    responses={
        404: {"description": "Item not found"},
        400: {"description": "No arguments specified"},
    },
)
# The Query and Path classes also allow us to add documentation to query and path parameters.
def update(
    item_id: int = Path(
        title="Item ID", description="Unique integer that specifies an item.", ge=0
    ),
    name: str
    | None = Query(
        title="Name",
        description="New name of the item.",
        default=None,
        min_length=1,
        max_length=8,
    ),
    shelf: int
    | None = Query(
        title="Availability",
        description="New shelf of the item.",
        default=None,
        gt=0.0,
    ),
    count: int
    | None = Query(
        title="Count",
        description="New amount of instances of this item in stock.",
        default=None,
        ge=0,
    ),
):
    if item_id not in items:
        HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")
    if all(info is None for info in (name, shelf, count)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )

    item = items[item_id]
    if name is not None:
        item.name = name
    if shelf is not None:
        item.shelf = shelf
    if count is not None:
        item.count = count

    return {"updated": item}


@app.delete("/delete/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:

    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exist."
        )

    item = items.pop(item_id)
    return {"deleted": item}