import requests

"""
# Add a new item
print(requests.post("http://127.0.0.1:8000/", json={
  "name": "Mehthanol",
  "shelf": 3,
  "lab": "chemistry",
  "count": 10,
  "category": "equipment",
  "expiration_date": "04.21.2027"
}).json())
"""
# Get all items
print(requests.get("http://127.0.0.1:8000/items/?name=beaker").json())

"""
# Delete an item
delete_id="6624e04a00244f181a536b25"
print(requests.delete(f"http://127.0.0.1:8000/{delete_id}").json())
"""
"""
# Update an item
update_id="6624e24000244f181a536b27"
print(requests.put(f"http://127.0.0.1:8000/{update_id}", json={
  "name": "Beaker",
  "shelf": 5,
  "lab": "Physics",
  "count": 1,
  "category": "equipment",
  "expiration_date": "04.21.2024"
}).json())
"""