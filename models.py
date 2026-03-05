from pydantic import BaseModel
# import json

class User(BaseModel):
    user_id:int
    name:str
    email:str

