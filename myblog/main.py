from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pytz import timezone
from sqlalchemy.orm import Session

# from . import crud, models, schemas

import crud
import models
import schemas
from database import SessionLocal, engine
from crud import CustomException

models.Base.metadata.create_all(bind=engine, checkfirst=True)

jst = timezone("Asia/Tokyo")
app = FastAPI()


# 例外をフックすると呼ばれる
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=500,
        content={"error_code": exc.error_code, "message": exc.message, "log": exc.log},
    )


# origins = {"*"} # all allow
origins = {"http://localhost:3000"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return {"message": "Success"}


# Read
@app.get("/posts", response_model=list[schemas.Post])
async def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_posts(db, skip=skip, limit=limit)
    return users


@app.get("/posts/{id}", response_model=schemas.Post)
async def read_post(id: str, db: Session = Depends(get_db)):
    users = crud.get_post(db, id)
    return users


# Create
@app.post("/posts", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)


# Delete
@app.delete("/posts/{id}", response_model=[])
async def delete_post(id: str, db: Session = Depends(get_db)):
    return crud.delete_post(db=db, id=id)
