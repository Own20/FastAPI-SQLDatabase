from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

#Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#Create a dependency
#Now use the SessionLocal/ class we created in the /sql_app/database.py/ file to create a dependency.
#We need to have an independent database session/connection (/SessionLocal/) per request, use the same session through all the request and then close it after the request is finished.
#For that, we will create a new dependency with /yield/, as explained before in the section about Dependencies with yield.
#Our dependency will create a new SQLAlchemy /SessionLocal/ that will be used in a single request, and then close it once the request is finished.
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Create your FastAPI path operations
@app.post("/users/", response_model=schemas.User)
#And then, when using the dependency in a path operation function, we declare it with the type Session we imported directly from SQLAlchemy.
#This will then give us better editor support inside the path operation function, because the editor will know that the db parameter is of type Session
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items