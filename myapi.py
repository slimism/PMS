from os import stat
from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Optional,List
from database import SessionLocal
import models

app=FastAPI(title='Password Management System - API', description='API to query the password management system', version='0.1')

class complexity(BaseModel): #serializer
    complexity_id:int
    uppercase:int
    lowercase: int
    symbols: int
    numbers: int

    class Config:
        orm_mode=True

db=SessionLocal()

@app.get('/complexity',response_model=List[complexity],status_code=200)
def get_complexity():
    complexity=db.query(models.complexity).all()
    return complexity
