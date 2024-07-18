def individual_serial(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "shelf": item["shelf"],
        "lab": item["lab"],
        "count": item["count"],
        "category": item["category"],
        "expiration_date": item["expiration_date"] 
    }
    
def list_serial(items) -> list:
    return [individual_serial(item) for item in items]