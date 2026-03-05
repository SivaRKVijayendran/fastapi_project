from fastapi import FastAPI, Depends, status, Query
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from database import  get_db
from model import Book
from schema import Bookstore , Book_update



app = FastAPI()


@app.get("/getallbooks")
def get_all_books(db : Session = Depends(get_db)):
    return db.query(Book).all();


@app.get("/getbyid/{id}")
def get_by_id(id : int, db : Session = Depends(get_db)):
    exiting_book = db.query(Book).filter(Book.id == id).first()
    if exiting_book:
        return exiting_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book id id not found")

@app.get("/getbyid")
def get_by_id(
        id : int = Query(1 , description = "Plaese enter the ID")
              , db : Session = Depends(get_db)):
    exiting_book = db.query(Book).filter(Book.id == id).first()
    if exiting_book:
        return exiting_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Default id also not found")


@app.post("/createbook")
def create_book(bk: Bookstore, db: Session = Depends(get_db)):

    existing_book = db.query(Book).filter(Book.id == bk.id).first()

    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ID already exists"
        )

    new_book = Book(
        id=bk.id,
        title=bk.title,
        author=bk.author,
        publish_date=bk.publish_date
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@app.put("/modifybyid/{bid}")
def modify_by_id(bid : int ,  bk : Book_update,  db : Session =Depends(get_db)):
    exiting_book = db.query(Book).filter(Book.id == bid).first()

    if not exiting_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Book is not found")

    exiting_book.title = bk.title
    exiting_book.author = bk.author
    exiting_book.publish_date = bk.publish_date

    db.commit()
    db.refresh(exiting_book)

    exiting_book_new = db.query(Book).filter(Book.id == bid).first()

    return exiting_book_new

@app.delete("/deletebyid/{bid}")
def delete_by_id(bid: int, db: Session = Depends(get_db)):

    existing_book = db.query(Book).filter(Book.id == bid).first()

    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book ID not found"
        )

    db.delete(existing_book)
    db.commit()

    return {"message": "Deleted successfully"}