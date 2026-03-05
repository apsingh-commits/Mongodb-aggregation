from fastapi import FastAPI
from models import User
from database import collection,address_collection
from random import randint, choice
from faker import Faker

app= FastAPI()

fake = Faker()

@app.post("/users/addresses")
async def addresses():
    cities = [
        {"city": "New York"},
        {"city": "London"},
        {"city": "Paris"},
        {"city": "Berlin"},
        {"city": "Tokyo"},
        {"city": "Sydney"},
        {"city": "Toronto"},
        {"city": "Dubai"},
        {"city": "Singapore"},
        {"city": "Mumbai"}
    ]
     
    result = await address_collection.insert_many(cities)

    return {
        "inserted_count": len(result.inserted_ids)
    }

@app.post("/users")
async def users():
    users = []

    addresses = await address_collection.find().to_list(length=None)

    for _ in range(100):
        address = choice(addresses)
        user = {
            "name": fake.name(),
            "age": randint(18, 60),
            "address_id": address["_id"],
            "salary": randint(30000, 100000)
        }
        users.append(user)

    result = await collection.insert_many(users)

    return {
        "inserted_count": len(result.inserted_ids)
    }

@app.get("/users/users-with-city")
async def get_users( page:int = 1, limit: int=10):
    skip = (page - 1) * limit

    pipeline = [
        {
            "$lookup": {
                "from": "addresses",
                "localField": "address_id",
                "foreignField": "_id",
                "as": "address"
            }
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }
    ]

    users = await collection.aggregate(pipeline).to_list(length=None)

    for user in users:
        user["_id"] = str(user["_id"])
        user["address_id"] = str(user["address_id"])

        for addr in user["address"]:
            addr["_id"] = str(addr["_id"])

    return {"users": users}


@app.get("/users/users_by_city")
async def get_user_by_city(city:str):

    users = await collection.aggregate([
        {
            "$match": {"address_id":city}
        },
        {    
            "$project": {"_id": 1,"name": 1}
        }
    ]).to_list(length=None)

    for user in users:
         user["_id"] = str(user["_id"])

    return {

        "users": users
    }

@app.get("/users")
async def grouping():

    users = await collection.aggregate([
        {
            "$group":{
                "_id":"$city",
                "total_salary":{"$sum":"$salary"}
            }
        }
    ]).to_list(length=None)

    for user in users:
         user["_id"] = str(user["_id"])

    return {

        "users": users
    }


















