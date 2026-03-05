from motor.motor_asyncio import AsyncIOMotorClient

#mongodb server address
Mongo_url = "mongodb://localhost:27017"

#async mongodb client
client = AsyncIOMotorClient(Mongo_url)

#connect fastapi with mongodb
database = client.users_db

#users - collection name
collection = database.users

#addresses-collection name
address_collection = database.addresses

